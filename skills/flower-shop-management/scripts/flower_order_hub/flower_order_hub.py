#!/usr/bin/env python3
"""
Flower Order Hub

AI-assisted order capture for flower shops:
- Paste WeChat/chat text and extract a structured order.
- Store orders in a local SQLite database.
- Expose simple HTTP endpoints for third-party webhooks.
- Print delivery slips for local printers and filter orders by region.

This MVP uses only Python standard library modules.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import mimetypes
import os
import re
import sqlite3
import sys
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import asdict, dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


DB_PATH = os.getenv("FLOWER_ORDER_DB", "flower_orders.db")
APP_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(APP_DIR, "index.html")

ORDER_FIELDS = [
    "id",
    "source",
    "raw_text",
    "region",
    "customer_name",
    "receiver_name",
    "receiver_phone",
    "delivery_address",
    "delivery_date",
    "delivery_time_range",
    "product_name",
    "style",
    "budget",
    "paid_amount",
    "product_image",
    "card_message",
    "notes",
    "status",
    "missing_fields",
    "risk_flags",
    "created_at",
    "updated_at",
    "dispatched_at",
    "dispatch_response",
]

REQUIRED_FIELDS = [
    "receiver_phone",
    "delivery_address",
    "delivery_date",
    "delivery_time_range",
]


@dataclass
class Order:
    id: str = field(default_factory=lambda: "F" + dt.datetime.now().strftime("%Y%m%d") + uuid.uuid4().hex[:6].upper())
    source: str = "wechat_text"
    raw_text: str = ""
    region: str = ""
    customer_name: str = ""
    receiver_name: str = ""
    receiver_phone: str = ""
    delivery_address: str = ""
    delivery_date: str = ""
    delivery_time_range: str = ""
    product_name: str = ""
    style: str = ""
    budget: str = ""
    paid_amount: str = ""
    product_image: str = ""
    card_message: str = ""
    notes: str = ""
    status: str = "draft"
    missing_fields: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: now_iso())
    updated_at: str = field(default_factory=lambda: now_iso())
    dispatched_at: str = ""
    dispatch_response: str = ""


def now_iso() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat()


def today() -> dt.date:
    configured = os.getenv("FLOWER_ORDER_TODAY", "").strip()
    if configured:
        return dt.date.fromisoformat(configured)
    return dt.date.today()


def init_db(db_path: str = DB_PATH) -> None:
    conn = sqlite3.connect(db_path)
    try:
        columns = ", ".join([f"{field} TEXT" for field in ORDER_FIELDS])
        conn.execute(f"CREATE TABLE IF NOT EXISTS orders ({columns}, PRIMARY KEY(id))")
        existing_columns = {
            row[1] for row in conn.execute("PRAGMA table_info(orders)").fetchall()
        }
        for field in ORDER_FIELDS:
            if field not in existing_columns:
                conn.execute(f"ALTER TABLE orders ADD COLUMN {field} TEXT")
        conn.commit()
    finally:
        conn.close()


def backfill_regions(db_path: str = DB_PATH) -> None:
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("SELECT id, delivery_address, raw_text, region FROM orders WHERE region IS NULL OR region = ''").fetchall()
        for row in rows:
            region = extract_region(row["delivery_address"] or "", row["raw_text"] or "")
            if region:
                conn.execute("UPDATE orders SET region = ?, updated_at = ? WHERE id = ?", (region, now_iso(), row["id"]))
        conn.commit()
    finally:
        conn.close()


def normalize_order(data: dict[str, Any], raw_text: str = "", source: str = "wechat_text") -> Order:
    order = Order(raw_text=raw_text, source=source)
    for key in ORDER_FIELDS:
        if key in data and hasattr(order, key):
            value = data[key]
            if isinstance(value, list):
                value = json.dumps(value, ensure_ascii=False)
            setattr(order, key, str(value or ""))

    if not order.region:
        order.region = extract_region(order.delivery_address, raw_text)
    order.missing_fields = compute_missing(order)
    order.risk_flags = compute_risks(order)
    order.status = "ready_to_dispatch" if not order.missing_fields else "needs_review"
    order.updated_at = now_iso()
    return order


def compute_missing(order: Order) -> list[str]:
    labels = {
        "receiver_phone": "收花人电话",
        "delivery_address": "配送地址",
        "delivery_date": "配送日期",
        "delivery_time_range": "配送时间段",
    }
    return [labels[field] for field in REQUIRED_FIELDS if not getattr(order, field)]


def compute_risks(order: Order) -> list[str]:
    risks = []
    text = order.raw_text + " " + order.notes
    if re.search(r"加急|马上|尽快|立刻|现在|越快越好", text):
        risks.append("加急订单")
    if re.search(r"不要|忌讳|过敏|不能|避开", text):
        risks.append("有忌讳/特殊要求")
    if order.delivery_address and len(order.delivery_address) < 8:
        risks.append("地址可能不完整")
    if not order.paid_amount and re.search(r"未付|还没付|到付", text):
        risks.append("可能未付款")
    return risks


def save_order(order: Order, db_path: str = DB_PATH) -> None:
    init_db(db_path)
    data = asdict(order)
    data["missing_fields"] = json.dumps(order.missing_fields, ensure_ascii=False)
    data["risk_flags"] = json.dumps(order.risk_flags, ensure_ascii=False)
    placeholders = ", ".join(["?"] * len(ORDER_FIELDS))
    assignments = ", ".join([f"{field}=excluded.{field}" for field in ORDER_FIELDS if field != "id"])
    values = [data.get(field, "") for field in ORDER_FIELDS]
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            f"""
            INSERT INTO orders ({", ".join(ORDER_FIELDS)})
            VALUES ({placeholders})
            ON CONFLICT(id) DO UPDATE SET {assignments}
            """,
            values,
        )
        conn.commit()
    finally:
        conn.close()


def get_order(order_id: str, db_path: str = DB_PATH) -> Order | None:
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if not row:
            return None
        data = dict(row)
        data["missing_fields"] = json.loads(data.get("missing_fields") or "[]")
        data["risk_flags"] = json.loads(data.get("risk_flags") or "[]")
        return Order(**data)
    finally:
        conn.close()


def delete_order(order_id: str, db_path: str = DB_PATH) -> bool:
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def list_orders(limit: int = 200, region: str = "", db_path: str = DB_PATH) -> list[dict[str, Any]]:
    init_db(db_path)
    backfill_regions(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        if region:
            rows = conn.execute("SELECT * FROM orders WHERE region = ?", (region,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM orders").fetchall()
        result = []
        for row in rows:
            item = dict(row)
            item["missing_fields"] = json.loads(item.get("missing_fields") or "[]")
            item["risk_flags"] = json.loads(item.get("risk_flags") or "[]")
            result.append(item)
        result.sort(key=order_sort_key)
        return result[:limit]
    finally:
        conn.close()


def list_regions(db_path: str = DB_PATH) -> list[str]:
    init_db(db_path)
    backfill_regions(db_path)
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute("SELECT DISTINCT region FROM orders WHERE region IS NOT NULL AND region != '' ORDER BY region").fetchall()
        return [row[0] for row in rows]
    finally:
        conn.close()


def order_sort_key(order: dict[str, Any]) -> tuple[str, str, str]:
    date_value = order.get("delivery_date") or "9999-12-31"
    time_value = time_sort_value(order.get("delivery_time_range") or "")
    created_value = order.get("created_at") or ""
    return (date_value, time_value, created_value)


def time_sort_value(value: str) -> str:
    value = normalize_time_range(value)
    match = re.search(r"(\d{1,2})(?::|点)(\d{1,2})?", value)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        if ("下午" in value or "晚上" in value) and hour < 12:
            hour += 12
        if "中午" in value and hour < 11:
            hour += 12
        return f"{hour:02d}:{minute:02d}"
    if "早上" in value or "上午" in value:
        return "09:00"
    if "中午" in value:
        return "12:00"
    if "下午" in value:
        return "15:00"
    if "晚上" in value:
        return "19:00"
    return "99:99"


def update_order(order_id: str, data: dict[str, Any], db_path: str = DB_PATH) -> Order | None:
    order = get_order(order_id, db_path)
    if not order:
        return None
    editable_fields = [
        "source",
        "raw_text",
        "region",
        "customer_name",
        "receiver_name",
        "receiver_phone",
        "delivery_address",
        "delivery_date",
        "delivery_time_range",
        "product_name",
        "style",
        "budget",
        "paid_amount",
        "product_image",
        "card_message",
        "notes",
        "status",
    ]
    for field_name in editable_fields:
        if field_name in data:
            setattr(order, field_name, str(data.get(field_name) or ""))
    if not order.region:
        order.region = extract_region(order.delivery_address, order.raw_text)
    order.missing_fields = compute_missing(order)
    order.risk_flags = compute_risks(order)
    if order.status in {"draft", "needs_review", "ready_to_dispatch"}:
        order.status = "ready_to_dispatch" if not order.missing_fields else "needs_review"
    order.updated_at = now_iso()
    save_order(order, db_path)
    return order


def reparse_order(order_id: str, db_path: str = DB_PATH) -> Order | None:
    existing = get_order(order_id, db_path)
    if not existing:
        return None
    reparsed = parse_order_text(existing.raw_text, source=existing.source)
    reparsed.id = existing.id
    reparsed.created_at = existing.created_at
    reparsed.region = existing.region or reparsed.region
    reparsed.product_image = existing.product_image or ""
    reparsed.dispatched_at = existing.dispatched_at
    reparsed.dispatch_response = existing.dispatch_response
    if existing.status == "dispatched":
        reparsed.status = "dispatched"
    reparsed.updated_at = now_iso()
    save_order(reparsed, db_path)
    return reparsed


def order_print_text(order: Order) -> str:
    text = "\n".join(
        [
            f"订单号：{order.id}",
            f"地区/门店：{order.region}" if order.region else "",
            f"收花人：{order.receiver_name}",
            f"电话：{order.receiver_phone}",
            f"地址：{order.delivery_address}",
            f"配送日期：{order.delivery_date}",
            f"配送时间：{order.delivery_time_range}",
            f"祝福语：{order.card_message}" if order.card_message else "",
            f"备注：{order.notes}" if order.notes else "",
            "商品图：已上传" if order.product_image else "商品图：未上传",
        ]
    )
    return "\n".join([line for line in text.splitlines() if line.strip()])


def order_preview(order: Order) -> dict[str, Any]:
    return {
        "payload": as_response(order),
        "text": order_print_text(order),
    }


def print_page(orders: list[dict[str, Any]], title: str = "花店配送单") -> str:
    cards = []
    for item in orders:
        image_html = ""
        if item.get("product_image"):
            image_html = f'<div class="image"><img src="{html.escape(item["product_image"])}" alt="商品图"></div>'
        cards.append(
            f"""
            <section class="ticket">
              <div class="ticket-head">
                <h2>{html.escape(item.get("receiver_name") or item.get("receiver_phone") or "未命名订单")}</h2>
                <span>{html.escape(item.get("id") or "")}</span>
              </div>
              <dl>
                <dt>地区/门店</dt><dd>{html.escape(item.get("region") or "")}</dd>
                <dt>电话</dt><dd>{html.escape(item.get("receiver_phone") or "")}</dd>
                <dt>地址</dt><dd>{html.escape(item.get("delivery_address") or "")}</dd>
                <dt>配送时间</dt><dd>{html.escape((item.get("delivery_date") or "") + " " + (item.get("delivery_time_range") or ""))}</dd>
                <dt>祝福语</dt><dd>{html.escape(item.get("card_message") or "")}</dd>
                <dt>备注</dt><dd>{html.escape(item.get("notes") or "")}</dd>
              </dl>
              {image_html}
            </section>
            """
        )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; color: #111; background: #f6f7f4; }}
    header {{ display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #fff; border-bottom: 1px solid #ddd; }}
    h1 {{ margin: 0; font-size: 20px; }}
    button {{ border: 0; border-radius: 8px; padding: 10px 16px; background: #0f766e; color: #fff; font-size: 15px; cursor: pointer; }}
    main {{ padding: 16px; display: grid; gap: 14px; }}
    .ticket {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 16px; page-break-inside: avoid; }}
    .ticket-head {{ display: flex; justify-content: space-between; gap: 12px; border-bottom: 1px solid #ddd; padding-bottom: 8px; margin-bottom: 10px; }}
    h2 {{ margin: 0; font-size: 20px; }}
    dl {{ display: grid; grid-template-columns: 86px 1fr; gap: 8px 12px; margin: 0; }}
    dt {{ color: #555; }}
    dd {{ margin: 0; font-weight: 600; white-space: pre-wrap; overflow-wrap: anywhere; }}
    .image {{ margin-top: 12px; border-top: 1px solid #ddd; padding-top: 12px; }}
    .image img {{ max-width: 240px; max-height: 240px; object-fit: contain; }}
    @media print {{
      body {{ background: #fff; }}
      header {{ display: none; }}
      main {{ padding: 0; }}
      .ticket {{ border: 0; border-bottom: 1px dashed #999; border-radius: 0; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(title)}</h1>
    <button onclick="window.print()">选择打印机打印</button>
  </header>
  <main>
    {''.join(cards) or '<section class="ticket">没有可打印订单</section>'}
  </main>
</body>
</html>"""


def parse_order_text(raw_text: str, source: str = "wechat_text") -> Order:
    ai_data = parse_with_ai(raw_text)
    if ai_data:
        return normalize_order(ai_data, raw_text=raw_text, source=source)
    return parse_with_rules(raw_text, source=source)


def parse_with_ai(raw_text: str) -> dict[str, Any] | None:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AI_API_KEY")
    if not api_key:
        return None

    base_url = os.getenv("AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("AI_MODEL", "gpt-4.1-mini")
    url = base_url + "/chat/completions"
    system_prompt = """
你是花店订单录入助手。把聊天内容提取成 JSON，不要编造。
字段：
customer_name, receiver_name, receiver_phone, delivery_address,
delivery_date, delivery_time_range, product_image, card_message, notes。
日期必须输出 YYYY-MM-DD；如果只说今天/明天/后天，按当前日期换算。
缺失字段留空字符串。
只返回 JSON。
""".strip()
    payload = {
        "model": model,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": system_prompt + f"\n当前日期：{today().isoformat()}"},
            {"role": "user", "content": raw_text},
        ],
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        content = body["choices"][0]["message"]["content"].strip()
        content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(content)
    except (urllib.error.URLError, KeyError, json.JSONDecodeError, TimeoutError) as exc:
        print(f"AI parse failed, falling back to rules: {exc}", file=sys.stderr)
        return None


def parse_with_rules(raw_text: str, source: str = "wechat_text") -> Order:
    text = raw_text.replace("\r", "\n")
    address = extract_address(text)
    data: dict[str, Any] = {
        "region": extract_region(address, text),
        "receiver_name": extract_receiver_name(text),
        "receiver_phone": first_match(r"(?<!\d)(1[3-9]\d{9})(?!\d)", text),
        "budget": extract_budget(text),
        "paid_amount": first_match(r"(?:已付|付款|实收|收款)\s*[:：]?\s*([1-9]\d{1,5})", text),
        "card_message": extract_card_message(text),
        "delivery_address": address,
        "delivery_date": extract_date(text),
        "delivery_time_range": extract_time_range(text),
        "product_name": extract_product(text),
        "style": extract_style(text),
        "notes": extract_notes(text),
    }
    return normalize_order(data, raw_text=raw_text, source=source)


def first_match(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.I)
    return match.group(1).strip() if match else ""


def extract_address(text: str) -> str:
    explicit = first_match(r"(?:配送地址|收货地址|收花地址|地址|配送到|送去|地点)\s*[:：]?\s*([^\n]+)", text)
    if explicit:
        return stop_at_next_field(explicit).strip(" ，,。")
    explicit = first_match(r"(?:送到|送至)\s*(?!时间)\s*[:：]?\s*([^\n]+)", text)
    if explicit:
        return stop_at_next_field(explicit).strip(" ，,。")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        if re.search(r"时间|电话|手机|祝福|贺卡|卡片", line):
            continue
        if re.search(r"省|市|区|县|路|街|弄|号|楼|室|园|中心|广场|大厦|小区|餐厅|前台|店", line):
            return line.strip(" ，,。")
    return ""


def extract_region(address: str, raw_text: str = "") -> str:
    explicit = first_match(r"(?:地区|区域|门店|城市|分店)\s*[:：]\s*([^\n，,。；;]+)", raw_text)
    if explicit:
        return explicit

    source = address or raw_text
    municipality = first_match(r"(北京|上海|天津|重庆)市?", source)
    if municipality:
        district = first_match(rf"{municipality}市?([^市区县]{0,12}?[区县])", source)
        return municipality + (district or "")

    province_city = first_match(r"([\u4e00-\u9fa5]{2,12}省[\u4e00-\u9fa5]{2,12}市)", source)
    if province_city:
        return province_city

    city = first_match(r"([\u4e00-\u9fa5]{2,12}市)", source)
    if city:
        return city

    district = first_match(r"([\u4e00-\u9fa5]{2,12}[区县])", source)
    return district


def stop_at_next_field(value: str) -> str:
    return re.split(r"[，,。；;]\s*(?:电话|手机|卡片|贺卡|小卡|备注|预算|已付|付款|配送时间|配送时间段|订花人|收花人|祝福语)|(?:电话|手机|卡片|贺卡|小卡|备注|预算|已付|付款|配送时间|配送时间段|订花人|收花人|祝福语)\s*[:：]?", value, maxsplit=1)[0]


def extract_receiver_name(text: str) -> str:
    return first_match(r"(?:收花人姓名|收花人名字|收花人|收件人|收货人|联系人)\s*[:：]\s*([^\n，,。；;]+)", text)


def extract_date(text: str) -> str:
    base = today()
    if "后天" in text:
        return (base + dt.timedelta(days=2)).isoformat()
    if "明天" in text or "明日" in text:
        return (base + dt.timedelta(days=1)).isoformat()
    if "今天" in text or "今日" in text:
        return base.isoformat()
    explicit = first_match(r"(?:送到时间|配送时间段|配送时间|送达时间|时间段|时间)\s*[:：]\s*([^\n]+)", text)
    date_source = explicit or text
    match = re.search(r"(\d{1,2})[月/-](\d{1,2})[日号]?", date_source)
    if match:
        month, day = int(match.group(1)), int(match.group(2))
        year = base.year
        candidate = dt.date(year, month, day)
        if candidate < base - dt.timedelta(days=30):
            candidate = dt.date(year + 1, month, day)
        return candidate.isoformat()
    return ""


def extract_budget(text: str) -> str:
    explicit = first_match(r"(?:预算|价位|价格|做|要|来个)\s*[:：]?\s*([1-9]\d{1,5})\s*(?:元|块|左右)?", text)
    if explicit:
        return explicit
    money = first_match(r"(?<!\d)([1-9]\d{1,5})\s*(?:元|块|左右)(?!\d)", text)
    return money


def extract_time_range(text: str) -> str:
    explicit = first_match(r"(?:送到时间|配送时间段|配送时间|送达时间|时间段|时间)\s*[:：]\s*([^\n]+)", text)
    if explicit:
        return normalize_time_range(stop_at_next_field(explicit).strip(" ，,。"))
    range_match = first_match(r"(\d{1,2}[:：点]?\d{0,2}\s*[-到至]\s*\d{1,2}[:：点]?\d{0,2})", text)
    if range_match:
        return normalize_time_range(range_match)
    for word in ["上午", "中午", "下午", "晚上", "早上"]:
        if word in text:
            time_match = first_match(rf"({word}\s*\d{{0,2}}[:：点]?\d{{0,2}})", text)
            return time_match or word
    single = first_match(r"(\d{1,2}[:：点]\d{0,2}\s*(?:前|后|左右)?)", text)
    return normalize_time_range(single)


def normalize_time_range(value: str) -> str:
    value = (value or "").strip()
    value = re.sub(r"^\d{1,2}\s*月\s*\d{1,2}\s*[日号]?\s*", "", value)
    value = re.sub(r"^\d{1,2}\s*/\s*\d{1,2}\s*", "", value)
    value = re.sub(r"^\d{1,2}\s*-\s*\d{1,2}\s*", "", value)
    value = value.replace("时", "点")
    value = re.sub(r"\s+", "", value)
    return value


def extract_card_message(text: str) -> str:
    patterns = [
        r"(?:祝福语|祝福|贺词)\s*[:：]\s*([^\n]+)",
        r"(?:卡片|贺卡|小卡)\s*(?:写|内容|内容写)?\s*[:：]?\s*[“\"']?([^\n，,。；;]+)",
        r"(?:写)\s*[“\"']?([^\n，,。；;]+)",
    ]
    for pattern in patterns:
        value = first_match(pattern, text)
        if value:
            return stop_at_next_field(value).strip("”\"' ，,。")
    return ""


def extract_product(text: str) -> str:
    keywords = ["花束", "鲜花", "玫瑰", "康乃馨", "百合", "向日葵", "开业花篮", "花篮", "桌花", "抱抱桶"]
    found = [word for word in keywords if word in text and not is_negated_keyword(text, word)]
    return "、".join(found[:3]) if found else ""


def is_negated_keyword(text: str, keyword: str) -> bool:
    for match in re.finditer(re.escape(keyword), text):
        prefix = text[max(0, match.start() - 6) : match.start()]
        if re.search(r"不要|不能|忌讳|避开|过敏", prefix):
            return True
    return False


def extract_style(text: str) -> str:
    colors = ["粉色", "白绿", "白色", "红色", "香槟", "紫色", "蓝色", "黄色", "橙色"]
    moods = ["高级", "温柔", "可爱", "韩式", "法式", "自然", "开业", "生日", "表白", "纪念日"]
    found = [word for word in colors + moods if word in text]
    return "、".join(found)


def extract_notes(text: str) -> str:
    explicit = first_match(r"(?:备注|特殊要求)\s*[:：]?\s*([^\n]+)", text)
    if explicit:
        return explicit.strip(" ，,。")
    lines = []
    for line in text.splitlines():
        if re.search(r"不要|忌讳|过敏|送达前|保密|惊喜|加急", line):
            lines.append(line.strip())
    return "；".join(lines)


class AppHandler(BaseHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def _json(self, status: int, payload: dict[str, Any] | list[Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path: str) -> None:
        if not os.path.exists(path):
            self._json(404, {"error": "not found"})
            return
        with open(path, "rb") as file:
            body = file.read()
        content_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type + ("; charset=utf-8" if content_type.startswith("text/") else ""))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        return json.loads(raw or "{}")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path in {"/", "/index.html"}:
            self._file(INDEX_PATH)
            return
        if path == "/health":
            self._json(200, {"ok": True, "time": now_iso()})
            return
        if path == "/api/regions":
            self._json(200, list_regions())
            return
        print_order_match = re.match(r"^/print/order/([^/]+)$", path)
        if print_order_match:
            order = get_order(urllib.parse.unquote(print_order_match.group(1)))
            if not order:
                self._json(404, {"error": "order not found"})
                return
            body = print_page([as_response(order)], title="花店配送单")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
            return
        if path == "/print/orders":
            region = query.get("region", [""])[0]
            orders = list_orders(region=region)
            title = f"{region}配送单" if region else "全部地区配送单"
            body = print_page(orders, title=title)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
            return
        if path.startswith("/api/orders"):
            preview_match = re.match(r"^/api/orders/([^/]+)/print-preview$", path)
            if preview_match:
                order = get_order(preview_match.group(1))
                if not order:
                    self._json(404, {"error": "order not found"})
                    return
                self._json(200, order_preview(order))
                return
            region = query.get("region", [""])[0]
            self._json(200, list_orders(region=region))
            return
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        try:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path
            data = self._read_json()
            if path == "/api/ingest/text":
                text = data.get("text", "")
                source = data.get("source", "wechat_text")
                if not text:
                    self._json(400, {"error": "text is required"})
                    return
                order = parse_order_text(text, source=source)
                if data.get("region") and not order.region:
                    order.region = str(data.get("region") or "").strip()
                save_order(order)
                self._json(200, {"order": as_response(order)})
                return

            if path == "/api/ingest/order":
                order = normalize_order(data, raw_text=data.get("raw_text", ""), source=data.get("source", "third_party"))
                save_order(order)
                self._json(200, {"order": as_response(order)})
                return

            update_match = re.match(r"^/api/orders/([^/]+)$", path)
            if update_match:
                order = update_order(update_match.group(1), data)
                if not order:
                    self._json(404, {"error": "order not found"})
                    return
                self._json(200, {"order": as_response(order)})
                return

            reparse_match = re.match(r"^/api/orders/([^/]+)/reparse$", path)
            if reparse_match:
                order = reparse_order(reparse_match.group(1))
                if not order:
                    self._json(404, {"error": "order not found"})
                    return
                self._json(200, {"order": as_response(order)})
                return

            self._json(404, {"error": "not found"})
        except Exception as exc:
            self._json(500, {"error": str(exc)})

    def do_DELETE(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        delete_match = re.match(r"^/api/orders/([^/]+)$", parsed.path)
        if not delete_match:
            self._json(404, {"error": "not found"})
            return
        if delete_order(delete_match.group(1)):
            self._json(200, {"ok": True})
            return
        self._json(404, {"error": "order not found"})


def as_response(order: Order) -> dict[str, Any]:
    data = asdict(order)
    return data


def run_server(host: str, port: int) -> None:
    init_db()
    server = ThreadingHTTPServer((host, port), AppHandler)
    print(f"Flower Order Hub listening on http://{host}:{port}")
    print("Open the frontend in your browser:")
    print(f"  http://{host}:{port}/")
    print("POST /api/ingest/text  {\"text\":\"...\", \"source\":\"wechat_text\"}")
    print("Open /print/order/{order_id} or /print/orders to print delivery slips")
    server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(description="Flower shop AI order capture, regional order book, and print hub.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db", help="Create the SQLite order database.")

    parse_cmd = sub.add_parser("parse", help="Parse pasted chat text into an order and save it.")
    parse_cmd.add_argument("--source", default="wechat_text")
    parse_cmd.add_argument("text", nargs="*", help="Chat text. If omitted, read stdin.")

    list_cmd = sub.add_parser("list", help="List recent orders.")
    list_cmd.add_argument("--limit", type=int, default=20)

    serve_cmd = sub.add_parser("serve", help="Run HTTP server for webhooks and integrations.")
    serve_cmd.add_argument("--host", default="127.0.0.1")
    serve_cmd.add_argument("--port", type=int, default=8787)

    args = parser.parse_args()
    if args.command == "init-db":
        init_db()
        print(f"Database ready: {DB_PATH}")
    elif args.command == "parse":
        raw_text = " ".join(args.text).strip() or sys.stdin.read().strip()
        order = parse_order_text(raw_text, source=args.source)
        save_order(order)
        print(json.dumps(as_response(order), ensure_ascii=False, indent=2))
    elif args.command == "list":
        print(json.dumps(list_orders(args.limit), ensure_ascii=False, indent=2))
    elif args.command == "serve":
        run_server(args.host, args.port)


if __name__ == "__main__":
    main()
