# Order Management Playbook

## Standard Order Table

Use these fields when creating a spreadsheet, database schema, form, or printed delivery slip:

- 订单编号
- 来源渠道: 微信、小红书、电话、到店、转介绍
- 地区/门店
- 订花人姓名和电话
- 收花人姓名和电话
- 配送地址 or 自取门店
- 配送日期
- 配送时间段
- 产品名称/花束类型
- 色系/风格
- 预算
- 已付金额
- 付款状态
- 贺卡内容
- 特殊备注
- 风险标签
- 订单状态
- 制作人
- 配送人
- 返图状态
- 售后状态

## Chat-To-Order Extraction

When parsing chat text, extract facts conservatively:

- Treat explicit customer wording as stronger than inference.
- Convert relative dates only when the current date is known. If uncertain, ask.
- Keep card text exactly as written.
- Do not infer payment completion from "我转你了" unless amount or screenshot is provided.
- If the address contains only a venue name, mark "地址可能不完整".
- If the customer says "照图做", add "需返图确认，鲜花自然形态会有差异".

## Region And Dispatch Rules

For multi-region shops:

- Derive region from explicit "地区/门店" first.
- If not present, derive from address city, district, mall, or landmark.
- If the region is ambiguous, keep it empty and ask for manual confirmation.
- Sort production by delivery date, then time range, then urgency.
- Keep high-risk same-day orders visible even if their time is later.

## Daily Review

At end of day, summarize:

- 新增订单数、完成数、未完成数
- 加急订单 and whether they were profitable
- Missing-field patterns that slowed down production
- Customer objections: price, delivery, style, exact-match requests
- After-sales cases and root cause
- Repeatable template improvements for customer replies
- Tomorrow's known orders and peak delivery windows

## After-Sales Handling

Use a calm verification-first flow:

1. Acknowledge the issue.
2. Ask for photos, delivery time, and order number if missing.
3. Verify whether it is flower quality, packaging damage, delivery delay, card error, or expectation mismatch.
4. Give a check-back time.
5. Offer a proportionate solution after verification.

Never promise refund/replacement amounts before checking the order facts and shop policy.
