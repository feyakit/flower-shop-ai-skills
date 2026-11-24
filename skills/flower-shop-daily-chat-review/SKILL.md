---
name: flower-shop-daily-chat-review
description: Read and analyze a date's customer conversations from the signed-in WeChat desktop using Codex Computer Use. Use when a flower-shop user asks to batch review daily WeChat chats, customer inquiries, orders, service quality, or shop operations. 中文触发：看今天的聊天、整理客户对话、读微信聊天记录、出聊天复盘、今天客户都问了什么、哪些单没成、售后情况怎么样、把今天私信整理一下、客户聊天日报。用户直接说上面任意一句时，就按本技能执行，不要先反问要用什么工具。
---

# Flower Shop Daily Chat Review

Use WeChat's visible desktop interface through Codex Computer Use to collect same-day customer conversation text and produce an evidence-based flower-shop operations review. Run only when the user asks. This is an on-demand foreground workflow; it does not run as a background monitor.

## Privacy and side-effect limits

- Read only the signed-in WeChat account and date range the user requested.
- Do not send messages, edit chats, delete records, change account settings, or transmit chat content to external services.
- Do not use LLDB, memory scanners, `find_key*.py`, or other methods to discover/decrypt WeChat database keys. Do not query original `db_storage` files.
- A chat opened in the UI may change its unread state. Before opening candidate chats, inspect the session list for unread badges. Skip unread one-to-one chats by default and ask before opening them; tell the user which candidates were excluded.
- Exclude group chats, official accounts, service accounts, family/personal conversations, and internal staff chats from customer metrics unless the user explicitly includes them.
- Treat names as uncertain. Classify a one-to-one chat as a customer only when its messages show flower-shop purchase, delivery, product, price, after-sales, or event intent.
- Redact phone numbers, street/building addresses, payment credentials, verification codes, and private links from reports. Do not include raw sensitive identifiers in output.
- Do not infer paid orders or revenue from intent alone. Count an order or amount only when the conversation explicitly confirms it.

## Collection workflow

1. Determine the analysis date. Use the date the user named; otherwise use today's date in Asia/Shanghai. State the date and timezone in the report.
2. Bind the WeChat app and read a fresh accessibility tree:
   ```js
   let wechat = await cua.getApp("com.tencent.xinWeChat");
   let state = await wechat.getAXState({ disableDiffing: true });
   ```
3. Inspect the visible session list. Build a candidate list of one-to-one conversations with activity on the target date. Use the timestamp/preview only to find candidates; verify the actual message dates in chat history.
4. Before opening a candidate, check for an unread badge. Skip unread conversations unless the user approves opening them. Exclude obvious group, official, service, self, and personal chats.
5. Open each eligible candidate by clicking its current element index. After every UI action, call `getAXState()` and derive fresh indices; never reuse indices from an older tree.
6. Open that chat's **聊天记录** view. The history list exposes dated messages (for example, `2026年11月23日 18:16`). Collect only messages within the target day's local-time window, from 00:00 through 23:59:59.
7. If the target day is not fully visible, scroll the chat-history message list in the direction that reveals older messages, re-read the tree, and continue until the list crosses the start of the target day. Stop at that boundary. Do not claim complete coverage unless both ends of the day are accounted for.
8. Keep each conversation separate while collecting. Preserve sender and timestamp when visible. Represent images, voice notes, videos, and files as placeholders unless their contents are available in the UI; never invent their contents.
9. Restore the WeChat window to its original chat/history view when possible. Do not send or edit anything.

## Operations analysis

Use only messages from eligible customer conversations and the requested date. Deduplicate repeated previews and overlapping history pages.

Report:
- Coverage: date/timezone, candidate chats reviewed, customer chats included, chats excluded and why, unread chats skipped, and any incomplete history.
- Funnel: inquiries, qualified purchase intents, confirmed orders, cancellations, and after-sales cases. Distinguish explicit counts from estimates; do not estimate when the sample is incomplete.
- Confirmed revenue and order value only when explicitly stated in messages. Separate paid, unpaid, and unknown status.
- Demand signals: occasions, flower types/colors, budget bands, delivery zones/time windows, and packaging requests.
- Service quality: response delays only when timestamps support the calculation, unanswered questions, quote clarity, fulfillment promises, and follow-up gaps.
- Action list: concrete improvements for product/price explanation, availability, delivery promises, follow-up, and content ideas tied to observed demand.
- Data limits and confidence.

Use a compact table for aggregate counts and a short narrative for themes. Clearly label simulated/test content if any appears. Never mix unrelated personal messages into business metrics.

## When the UI cannot provide enough data

If WeChat is closed, signed out, the requested date cannot be reached, UI history does not expose message text, or unread-state effects would exceed the user's approval, stop and explain the specific limit. Offer a user-controlled export or an already-authorized local database key file as a fallback. Do not attempt to obtain keys yourself.
