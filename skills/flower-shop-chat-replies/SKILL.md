---
name: flower-shop-chat-replies
description: Generate high-conversion Chinese customer-service replies for flower-shop chats. Use when the user asks how to reply to a flower-shop customer, shares a chat screenshot or customer message, asks for 小红书/微信/私域花店私信回复, pricing objections, delivery timing, bouquet customization, order confirmation, complaints, after-sales, or wants a warm sales reply that follows flower-shop客服话术.
---

# Flower Shop Chat Replies

## Core Outcome

Produce the exact next reply the flower-shop客服 can send, in natural Chinese, with a warm but bounded tone. Prefer ready-to-copy wording first, then add a short explanation only when useful.

## Input Handling

- If the user shares a screenshot, read the visible customer messages and infer the immediate customer intent.
- If critical facts are missing, do not block. Write a reply that asks only the necessary next question.
- If a promise depends on store capacity, inventory, delivery distance, or time, avoid hard commitment. Use "我帮您确认一下" or "我看下距离/花材/排单".
- If the user provides the actual price, time, address, style, or shop rule, use it. Otherwise use placeholders like `XX元`, `XX公里`, `几点到店`.
- Do not invent inventory, discounts, exact delivery feasibility, or compensation amounts.

## Reply Formula

Use this default structure unless the context clearly needs something else:

1. Acknowledge warmly: "可以的宝宝", "理解的哈", "好嘟".
2. Answer the direct question.
3. Add one value or risk-control point: flower freshness,返图确认,预算可调,配送规则,节日排单.
4. Ask the next conversion question: budget, use time, recipient, card content, phone, address, style preference.

Keep customer-facing replies concise: usually 2-6 short lines. For urgent chats, make it even shorter.

## Tone Rules

- Use the shop's soft, friendly voice: "宝宝", "亲亲", "花花", "好嘟", "咱们".
- Be polite without sounding robotic.
- Do not argue with customers who compare price. Acknowledge, explain value, then offer a budget version.
- Do not over-apologize unless there is a service issue.
- Do not say "做不到" bluntly. For custom bouquets, say "可以参考色系和感觉来做，鲜花自然形态会有一点差异".
- Avoid excessive emojis unless the user asks for a more playful style.

## Fast Decision Map

- Customer asks "多少钱": quote if known; if not, ask budget and explain price tiers.
- Customer asks "能几点送到吗": confirm address/time, then say you will check delivery distance and排单 before promising.
- Customer says "贵": validate feeling, explain flower grade/size/packaging/service, offer same-style budget adjustment.
- Customer asks "能不能一模一样": manage expectations, mention seasonal/natural differences, promise photo confirmation before delivery.
- Customer asks "可以到店包花/包娃娃吗": say yes only if known; otherwise ask arrival time, flower count, doll size, and budget.
- Customer is unsure or silent: ask whether the hesitation is style, price, or delivery time; offer 2-3 options.
- Customer has chosen and is ready: collect order confirmation fields.
- Customer complains: empathize, ask for photos/details, give a clear check-back time, then offer a solution after verification.

## Order Fields

When moving to order confirmation, collect:

- 配送地址 or 自取
- 配送/自取时间
- 收花人姓名
- 收花人电话
- 订花人电话
- 贺卡内容, if any
- 特别备注, such as color, no strong fragrance, delivery secrecy, or ring/gift placement

## References

Read `references/scene-playbook.md` when the user needs more than a one-off reply, asks for multiple wording options, or the situation matches pricing objection, custom bouquet, delivery, order confirmation, complaint, private-domain follow-up, or in-store bouquet wrapping.
