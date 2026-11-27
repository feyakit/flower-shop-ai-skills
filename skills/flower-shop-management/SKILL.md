---
name: flower-shop-management
description: Manage flower-shop operations workflows including order capture, WeChat/chat-to-order extraction, delivery scheduling, multi-region order filtering, delivery-slip printing, customer follow-up, after-sales handling, and daily shop review. Use when the user asks for 花店管理, 订单管理, 录单, 排单, 配送单, 打印订单, 多门店/多地区订单, 客户跟进, 售后复盘, or wants to run or improve a flower-shop order management tool.
---

# Flower Shop Management

## Core Outcome

Help the flower shop turn scattered chat messages and manual notes into clear, low-risk daily operations:

- Extract customer chats into structured flower orders.
- Identify missing fields and delivery risks before production.
- Organize orders by region/store, delivery date, and delivery time.
- Prepare printable delivery slips and handoff notes.
- Summarize daily issues, after-sales follow-up, and repeat-customer opportunities.

Default to Chinese when the user writes Chinese.

## Order Workflow

1. **Capture the order source.**
   - Read WeChat/Xiaohongshu/private-domain chat text or screenshots.
   - Preserve the original customer wording when it affects promise, budget, taboo, card content, or delivery time.

2. **Normalize required fields.**
   - 收花人姓名
   - 收花人电话
   - 配送地址 or 自取门店
   - 配送日期 and 时间段
   - 产品/花束类型
   - 预算 or 已付金额
   - 贺卡内容
   - 特殊备注: 忌讳、保密、过敏、加急、指定花材、色系

3. **Flag risks before confirming.**
   - 地址过短或不完整
   - 电话缺失
   - 加急/马上送/越快越好
   - 一模一样复刻要求
   - 指定花材但库存未知
   - 节日高峰排单
   - 未付款或金额不清楚

4. **Move through statuses.**
   - `needs_review`: missing fields or risky promise.
   - `ready_to_dispatch`: fields complete and payment/stock/delivery are acceptable.
   - `in_production`: florist has started making the order.
   - `dispatched`: driver/store has accepted the delivery.
   - `done`: delivery completed and after-sales window closed.

5. **Review the day.**
   - List delayed/risky orders.
   - List customers needing follow-up.
   - Capture repeatable issues into rules, not memory alone.

## Flower Order Hub Tool

This skill includes a local standard-library Python order tool:

`scripts/flower_order_hub/flower_order_hub.py`

Use it when the user wants a simple local flower order system, batch order capture, region filtering, or printable delivery slips.

Recommended setup keeps customer data outside the skill folder:

```bash
mkdir -p "$HOME/Documents/flower-shop-data"
cd ~/.codex/skills/flower-shop-management/scripts/flower_order_hub
FLOWER_ORDER_DB="$HOME/Documents/flower-shop-data/flower_orders.db" python3 flower_order_hub.py init-db
FLOWER_ORDER_DB="$HOME/Documents/flower-shop-data/flower_orders.db" python3 flower_order_hub.py serve --host 127.0.0.1 --port 8787
```

Then open:

```text
http://127.0.0.1:8787/
```

If the skill is being used from a copied repository before installation, run the same commands from that repository's `skills/flower-shop-management/scripts/flower_order_hub` directory.

## Management Replies

When the user needs customer-facing wording, use `flower-shop-chat-replies` if available. For management tasks, keep wording operational:

- Confirm what is known.
- Ask only for missing fields that block production or delivery.
- Avoid promising inventory, exact arrival time, or compensation until verified.
- Use check-back times: "我先确认花材和配送距离，10分钟内回复你。"

## References

Read `references/order-management-playbook.md` when the user asks for SOPs, table fields, daily review, multi-store rules, or after-sales management.

## Safety

- Do not commit customer databases, phone numbers, addresses, screenshots, or chat exports into a skill repository.
- Do not store live order data inside `~/.codex/skills`; use a separate data folder.
- Do not invent stock, courier availability, delivery fees, or refund amounts.
- If editing Feishu docs, preserve visible revision traces according to the user's preference: deleted/replaced source text should remain with strikethrough and new text should be purple where supported.
