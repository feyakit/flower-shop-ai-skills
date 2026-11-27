---
name: flower-shop-juguang
description: Diagnose, report, and optimize Xiaohongshu/Juguang ads for flower shops, including single-account and multi-account spend analysis, token refresh workflows, open-message and lead-cost diagnosis, creative scoring, budget/bid recommendations, Feishu sales feedback interpretation, and safe execution previews. Use when the user asks 看聚光数据, 花店聚光投放, 多账号聚光管理, 刷新授权, 开口成本, 线索成本, 预算/出价调整, 创意筛选, or 聚光优化建议.
---

# Flower Shop Juguang

## Core Outcome

Help flower shops manage Xiaohongshu Juguang ads with a practical operator mindset:

- Pull and summarize spend, impressions, clicks, CTR, CPC, private-message users, leads, and lead cost.
- Compare API lead data with real sales feedback when available.
- Diagnose accounts into protect, observe, control-cost, cold-start, and authorization-issue buckets.
- Recommend bid, budget, keyword, placement, and creative actions.
- Execute live changes only after clear user confirmation.

Default to Chinese when the user writes Chinese.

## Privacy And Local Credentials

Real credentials must stay on the local machine:

- `app_id`
- `app_secret`
- `advertiser_id`
- `access_token`
- `refresh_token`
- OAuth callback URLs containing `auth_code`

Never expose those values in final answers, reports, screenshots, commits, or copied skill packages. Use `references/xiaohongshu_config.example.json` only as a placeholder template.

## Common Workflows

### Multi-Account Report

Use this when the user says "看一下所有账号", "今天聚光怎么样", "给每个账号优化建议", or provides a workspace with account registry files.

Expected workspace files:

- `work/xiaohongshu_accounts.json`
- per-account config/token files referenced by the registry
- optional Feishu sales feedback exports or config

Commands:

```bash
python3 ~/.codex/skills/flower-shop-juguang/scripts/xhs_multi_account.py report --workspace /path/to/workspace
python3 ~/.codex/skills/flower-shop-juguang/scripts/xhs_multi_account.py report --workspace /path/to/workspace --refresh
python3 ~/.codex/skills/flower-shop-juguang/scripts/xhs_multi_account.py refresh --workspace /path/to/workspace
```

Outputs are written under the chosen workspace:

- `work/xhs_multi_account_report_YYYYMMDD.json`
- `outputs/xhs_multi_account_report_YYYYMMDD.md`

### Single-Account Diagnosis

Use the SDK and analysis scripts when the user works with one account or asks for deeper campaign, creative, or keyword diagnosis:

- `scripts/xiaohongshu_juguang_sdk.py`: API access and token handling.
- `scripts/xiaohongshu_creative_analyzer.py`: creative judgment.
- `scripts/xiaohongshu_reports.py`: report helpers.
- `scripts/xiaohongshu_smart_optimizer.py`: optimization helper logic.

Read `references/optimization_rules.md` before giving threshold-based optimization advice.

### First-Time Setup

When the user has not connected Juguang yet:

1. Ask whether they already have a Juguang advertiser account.
2. Tell them where to find AppID/AppSecret in Juguang developer tools.
3. Create a local config from `references/xiaohongshu_config.example.json`.
4. Keep token files outside Git-tracked folders.
5. Verify connection with read-only report calls before proposing changes.

## Diagnosis Rules

Use these default buckets:

- **Protect**: spend and lead quality are acceptable; avoid unnecessary changes.
- **Observe**: data volume is small or cost is slightly high; wait or make one small test.
- **Control cost**: lead/open-message cost is high with enough spend; reduce bid/budget or prune poor creatives.
- **Cold-start**: new campaigns need impressions and creative learning; avoid repeated bid cuts.
- **Authorization issue**: token/config failure; fix access before interpreting performance.

When Feishu or sales feedback exists, prefer effective business cost:

```text
effective cost = spend / add-WeChat or deal-positive feedback
```

Do not optimize only for cheap API leads if sales quality is poor.

## Execution Safety

- Show a preview before live bid, budget, pause, create, keyword, or creative changes.
- Execute only when the user explicitly says to proceed, such as "直接执行" or "按你的建议执行".
- Keep bid/target-cost changes light, usually within 5%-10%.
- Avoid multiple changes to the same campaign/unit within 2 hours.
- Do not change budgets after 16:00 unless the user explicitly requests it.
- Do not operate on accounts with invalid or unverified token state.
- Do not raise a poor-quality account just to spend faster.

## Response Shape

For reports:

```text
已拉取今天数据。

| 账号 | 消耗 | 曝光 | 点击 | CTR | CPC | 私信开口 | 线索 | 线索成本 |
...

重点判断：
- 保护：...
- 控成本：...
- 冷启动：...
- 授权异常：...

下一步建议：
...
```

For execution:

```text
已执行并验证：
- 账号/计划/单元
- 目标成本 from -> to
- 关键词/预算/创意变化
- 为什么这样做
```

## References

- `references/optimization_rules.md`: diagnosis thresholds and account action rules.
- `references/best_practices.json`: compact learned operating heuristics.
- `references/xiaohongshu_config.example.json`: placeholder local config template.

## Feishu Document Edits

If editing Feishu docs, preserve visible revision traces according to the user's preference: deleted/replaced source text should remain with strikethrough and new text should be purple where supported.
