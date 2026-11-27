#!/usr/bin/env python3
import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path


CN_TZ = timezone(timedelta(hours=8))
DEFAULT_WORKSPACE = Path(os.environ.get("XHS_JUGUANG_WORKSPACE", "xhs-juguang-workspace"))


def now_cn():
    return datetime.now(CN_TZ)


def today():
    return now_cn().date().isoformat()


def safe_float(value, default=0.0):
    if value in (None, ""):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).replace("%", "").replace(",", ""))
    except Exception:
        return default


def safe_int(value, default=0):
    return int(round(safe_float(value, default)))


def request_json(url, payload, headers=None, timeout=45):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            obj = json.loads(resp.read().decode("utf-8"))
        if obj.get("code") == 0:
            return {"success": True, "data": obj.get("data", {}), "raw": obj}
        return {
            "success": False,
            "code": obj.get("code"),
            "message": obj.get("msg") or obj.get("message") or "接口返回失败",
            "raw": obj,
        }
    except urllib.error.HTTPError as exc:
        return {
            "success": False,
            "http_error": exc.code,
            "message": exc.read().decode("utf-8", errors="replace")[:1200],
        }
    except Exception as exc:
        return {"success": False, "message": f"{type(exc).__name__}: {exc}"}


def post_jg(config, token, path, payload, timeout=45):
    return request_json(
        config["api_base_url"] + path,
        payload,
        headers={
            "Access-Token": token["access_token"],
            "Timestamp": str(int(time.time())),
        },
        timeout=timeout,
    )


def registry_path(workspace):
    return workspace / "work" / "xiaohongshu_accounts.json"


def load_registry(workspace):
    path = registry_path(workspace)
    if not path.exists():
        raise FileNotFoundError(f"Cannot find account registry: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_account(account):
    config = json.loads(Path(account["config_file"]).read_text(encoding="utf-8"))
    token = json.loads(Path(account["token_file"]).read_text(encoding="utf-8"))
    return config, token


def refresh_account(account):
    config, token = load_account(account)
    if not token.get("refresh_token"):
        return {"success": False, "message": "缺少 refresh_token"}

    result = request_json(
        "https://adapi.xiaohongshu.com/api/open/oauth2/refresh_token",
        {
            "app_id": int(config["app_id"]),
            "secret": config["app_secret"],
            "refresh_token": token["refresh_token"],
        },
        timeout=20,
    )
    if not result.get("success"):
        return {
            "success": False,
            "message": result.get("message"),
            "code": result.get("code"),
        }

    data = result["data"]
    new_token = {
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token") or token.get("refresh_token"),
        "expires_at": int(time.time()) + int(data.get("access_token_expires_in") or 86400),
        "refresh_token_expires_in": data.get("refresh_token_expires_in"),
        "advertiser_id": str(config.get("advertiser_id")),
        "advertiser_name": token.get("advertiser_name", ""),
        "refresh_time": int(time.time()),
    }
    Path(account["token_file"]).write_text(
        json.dumps(new_token, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    verify = post_jg(
        config,
        new_token,
        "/campaign/list",
        {
            "advertiser_id": int(config["advertiser_id"]),
            "page": {"page_index": 1, "page_size": 5},
        },
        timeout=20,
    )
    return {
        "success": bool(verify.get("success")),
        "verify_message": verify.get("message"),
        "campaign_count_seen": len((verify.get("data") or {}).get("base_campaign_dtos") or []),
    }


def refresh_all(workspace):
    registry = load_registry(workspace)
    ops = []
    for account in registry.get("accounts", []):
        if account.get("status") != "active":
            continue
        op = {
            "key": account.get("key"),
            "name": account.get("name"),
            "advertiser_id": account.get("advertiser_id"),
        }
        try:
            op.update(refresh_account(account))
        except Exception as exc:
            op.update({"success": False, "message": f"{type(exc).__name__}: {exc}"})
        ops.append(op)
    return {"generated_at": now_cn().isoformat(timespec="seconds"), "ops": ops}


def campaign_list(config, token):
    return post_jg(
        config,
        token,
        "/campaign/list",
        {
            "advertiser_id": int(config["advertiser_id"]),
            "page": {"page_index": 1, "page_size": 100},
        },
    )


def realtime_account(config, token, date_text):
    return post_jg(
        config,
        token,
        "/data/report/realtime/account",
        {
            "advertiser_id": int(config["advertiser_id"]),
            "start_date": date_text,
            "end_date": date_text,
        },
    )


def summarize(account, calls):
    realtime = calls.get("realtime_account", {})
    data = realtime.get("data") if realtime.get("success") else {}
    if not isinstance(data, dict):
        data = {}
    campaigns_result = calls.get("campaign_list", {})
    campaigns = []
    if campaigns_result.get("success"):
        campaigns = (campaigns_result.get("data") or {}).get("base_campaign_dtos") or []
    active_campaigns = [c for c in campaigns if c.get("campaign_enable") == 1]

    fee = safe_float(data.get("fee"))
    impression = safe_int(data.get("impression"))
    click = safe_int(data.get("click"))
    message_user = safe_int(data.get("message_user"))
    initiative_message = safe_int(data.get("initiative_message"))
    msg_leads = safe_int(data.get("msg_leads_num"))

    return {
        "key": account.get("key"),
        "name": account.get("name"),
        "advertiser_id": account.get("advertiser_id"),
        "success": bool(realtime.get("success")),
        "error": realtime.get("message"),
        "fee": fee,
        "impression": impression,
        "click": click,
        "ctr": safe_float(data.get("ctr")),
        "cpc": fee / click if click else 0.0,
        "message_user": message_user,
        "message_consult": safe_int(data.get("message_consult")),
        "initiative_message": initiative_message,
        "msg_leads": msg_leads,
        "message_user_cost": fee / message_user if message_user else 0.0,
        "msg_leads_cost": fee / msg_leads if msg_leads else 0.0,
        "active_campaign_count": len(active_campaigns),
        "sample_active_campaigns": [
            {
                "campaign_id": c.get("campaign_id"),
                "campaign_name": c.get("campaign_name"),
                "placement": c.get("placement"),
                "budget_yuan": (c.get("campaign_day_budget") or 0) / 100,
                "target_cost_yuan": (c.get("constraint_value") or 0) / 100,
            }
            for c in active_campaigns[:5]
        ],
    }


def classify(summary):
    if not summary.get("success"):
        return "授权异常"
    fee = summary["fee"]
    msg = summary["message_user"]
    leads = summary["msg_leads"]
    lead_cost = summary["msg_leads_cost"]
    if fee < 5 and summary["impression"] < 100:
        return "冷启动"
    if leads >= 2 and lead_cost <= 30:
        return "保护"
    if leads > 0 and lead_cost <= 40:
        return "可接受"
    if fee >= 100 and leads == 0:
        return "控成本"
    if fee < 50 and leads == 0:
        return "观察"
    if msg > 0 and leads == 0:
        return "承接弱"
    return "观察"


def recommendation(summary):
    state = classify(summary)
    if state == "授权异常":
        return "授权失效，先刷新 token；若 refresh_token 也失败，需要重新 OAuth。"
    if state == "保护":
        return "线索成本优秀，保持当前目标成本和关键词，今天不要乱动。"
    if state == "可接受":
        return "成本可接受，继续观察；若连续两轮稳定，可考虑小幅扩量。"
    if state == "控成本":
        return "消耗已高且无线索，建议目标成本轻降 5%-10%，同时检查素材是否能引导加微。"
    if state == "承接弱":
        return "有私信但无线索，先优化私信首句和销售承接，不要急着加预算。"
    if state == "冷启动":
        return "曝光太少，先查创意审核；审核正常但仍不起量时再小幅提目标成本。"
    return "样本还不够，继续观察到 50 元以上或至少 1 个开口再判断。"


def render_markdown(output):
    summaries = output["summaries"]
    ok = [s for s in summaries if s.get("success")]
    total_fee = sum(s["fee"] for s in ok)
    total_impression = sum(s["impression"] for s in ok)
    total_click = sum(s["click"] for s in ok)
    total_msg = sum(s["message_user"] for s in ok)
    total_leads = sum(s["msg_leads"] for s in ok)
    total_ctr = total_click / total_impression * 100 if total_impression else 0.0
    total_cpc = total_fee / total_click if total_click else 0.0
    total_lead_cost = total_fee / total_leads if total_leads else 0.0

    lines = [
        "# 小红书聚光多账号今日数据",
        "",
        f"生成时间：{output['generated_at']}",
        f"统计日期：{output['date']}",
        "",
        "## 总览",
        "",
        f"已拉通账号：{len(ok)}/{len(summaries)}",
        f"总消耗：{total_fee:.2f} 元",
        f"总曝光：{total_impression:,}",
        f"总点击：{total_click:,}",
        f"综合 CTR：{total_ctr:.2f}%",
        f"综合 CPC：{total_cpc:.2f} 元",
        f"私信开口：{total_msg}",
        f"线索：{total_leads}",
        f"线索成本：{total_lead_cost:.2f} 元" if total_leads else "线索成本：暂无线索",
        "",
        "## 分账号",
        "",
        "| 账号 | 状态 | 消耗 | 曝光 | 点击 | CTR | CPC | 私信开口 | 线索 | 线索成本 | 建议 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for s in summaries:
        if not s.get("success"):
            lines.append(f"| {s['name']} | 授权异常 | - | - | - | - | - | - | - | - | {s.get('error') or '拉取失败'} |")
            continue
        lines.append(
            f"| {s['name']} | {classify(s)} | {s['fee']:.2f} | {s['impression']:,} | {s['click']:,} | "
            f"{s['ctr']:.2f}% | {s['cpc']:.2f} | {s['message_user']} | {s['msg_leads']} | "
            f"{s['msg_leads_cost']:.2f} | {recommendation(s)} |"
        )
    return "\n".join(lines)


def report(workspace, date_text, refresh_first=False):
    if refresh_first:
        refresh_all(workspace)

    registry = load_registry(workspace)
    output = {
        "generated_at": now_cn().isoformat(timespec="seconds"),
        "date": date_text,
        "summaries": [],
    }
    for account in registry.get("accounts", []):
        if account.get("status") != "active":
            continue
        try:
            config, token = load_account(account)
            calls = {
                "realtime_account": realtime_account(config, token, date_text),
                "campaign_list": campaign_list(config, token),
            }
            summary = summarize(account, calls)
        except Exception as exc:
            summary = {
                "key": account.get("key"),
                "name": account.get("name"),
                "advertiser_id": account.get("advertiser_id"),
                "success": False,
                "error": f"{type(exc).__name__}: {exc}",
            }
        output["summaries"].append(summary)

    work_dir = workspace / "work"
    out_dir = workspace / "outputs"
    work_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = date_text.replace("-", "")
    json_path = work_dir / f"xhs_multi_account_report_{stamp}.json"
    md_path = out_dir / f"xhs_multi_account_report_{stamp}.md"
    json_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(output), encoding="utf-8")
    return {"success": True, "result_path": str(json_path), "report_path": str(md_path), **output}


def main():
    parser = argparse.ArgumentParser(description="XHS Juguang multi-account helper")
    parser.add_argument("command", choices=["refresh", "report"])
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    parser.add_argument("--date", default=today())
    parser.add_argument("--refresh", action="store_true", help="Refresh tokens before report")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    if args.command == "refresh":
        result = refresh_all(workspace)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if all(op.get("success") for op in result["ops"]) else 1

    result = report(workspace, args.date, refresh_first=args.refresh)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    raise SystemExit(main())
