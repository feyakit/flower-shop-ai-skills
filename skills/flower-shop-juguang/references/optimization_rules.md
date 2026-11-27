# Optimization Rules

Use these rules for flower-shop Xiaohongshu Juguang multi-account decisions.

## Core Metrics

- Private-message open cost: `spend / message_user`.
- Lead cost: `spend / msg_leads`.
- Sales-adjusted effective cost, when Feishu data exists: `spend / add_wechat_count` and `spend / deal_count`.
- CTR and CPC are process metrics; they explain why cost changes, but do not override lead quality.

## Account States

**Protect**

- Lead cost <= 30 yuan and at least 2 leads.
- Or lead cost <= 35 yuan with rising open-message volume.
- Action: do not lower target cost; consider future small budget expansion only before 16:00.

**Observe**

- Spend < 50 yuan and no lead yet.
- Or newly adjusted within the last 2 hours.
- Action: do not panic-adjust; wait for more signal.

**Control Cost**

- Spend >= 100 yuan and 0 leads.
- Or lead cost > 50 yuan after at least 2 leads.
- Action: lower target cost 5%-10%, tighten keywords, avoid budget increase.

**Cold Start**

- Spend < 5 yuan, impressions < 100, active campaign exists.
- Action: check creative audit/eligibility first. If audit normal and still no exposure, raise target cost 5%-10%; do not raise repeatedly in the same hour.

**Authorization Issue**

- API returns `access_token已过期`, `access_token错误`, or refresh fails.
- Action: refresh token automatically once; if refresh_token fails, ask for OAuth callback again.

## Account-Specific Lessons From This Workspace

- 晓作: volume can be large and CPC low, but lead conversion can weaken. If spend crosses 150 yuan with 0 leads, lower target cost lightly.
- 希子: has shown good lead cost after keyword tightening. Protect when lead cost is around 25-35 yuan.
- 知巷: performs well after precise search and target-cost lift. If cost is <35 but volume low, small lift is acceptable.
- 野木: CPC improved after keyword cleanup; avoid repeated lowering before enough spend.
- 初见: open-message to lead quality is sensitive. Light target-cost control works better than hard cuts.
- 栖木: cold-start issue; first check audit and exposure before judging conversion.
- 植笙/屿笙: often strong cost performers; protect stable campaigns unless sales feedback says quality is poor.

## Keyword Hygiene

Prefer city + intent:

- `城市花店`
- `城市送花`
- `城市同城送花`
- `城市生日花束`
- `城市开业花篮`
- `城市花束定制`
- district-level flower-shop terms
- brand terms

Avoid or downweight broad seasonal/gift terms when quality is poor:

- `520送花`
- `七夕送花`
- `教师节送花`
- `纪念日送什么`
- `女朋友生日送什么`
- broad aesthetic-only flower terms

## Execution Cadence

- Target-cost change: usually 5%-10%.
- Wait at least 2 hours after a target-cost change before judging.
- Avoid more than 3 operations per account per day unless there is a severe spend leak.
- Never pause old plans unless replacement plans are verified and the user has confirmed.
