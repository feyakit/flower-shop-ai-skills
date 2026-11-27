---
name: flower-shop-account-optimization
description: Diagnose and optimize Xiaohongshu/小红书 accounts for local flower shops, including profile positioning, content matrix, pinned notes, conversion path, Juguang/聚光 candidate selection, and HTML/Word/Obsidian report output. Use when the user asks to 看花店账号, 花店账号诊断, 小红书账号优化, 聚光推广建议, 哪些笔记适合投聚光, 生成账号优化报告, or 沉淀到 Obsidian.
---

# Flower Shop Account Optimization

## Core Goal

Turn a Xiaohongshu account review into repeatable deliverables:

- Account identity check and current-state diagnosis.
- Note-level Juguang candidate ranking.
- Concrete profile, pinned-note, content, title, and conversion-path optimizations.
- HTML report, Word report, and Obsidian Markdown note.

Default to Chinese when the user writes Chinese.

## Related Skills

Use the minimal related skills needed for the request:

- Use `agent-reach` / OpenCLI for Xiaohongshu search, account, note detail, and comment data when available.
- Use `flower-shop-chat-replies` for conversion-path wording and customer-service voice judgment.
- Use `flower-shop-juguang` for Juguang delivery diagnosis and campaign strategy.
- Use `documents` when creating or verifying `.docx` output.

## Standard Workflow

1. **Confirm the account identity.**
   - Compare the user-provided account name with screenshots, Xiaohongshu ID, profile URL, and public search results.
   - If the user name and screenshots conflict, state the conflict and analyze the account shown by evidence.

2. **Collect public evidence.**
   - Use screenshots supplied by the user.
   - Search Xiaohongshu for the account name and likely local keywords.
   - Fetch public account notes when possible.
   - Fetch note details and comments for likely candidates.
   - Respect access limits. If login, captcha, or permissions block access, report the limit and continue with screenshot/manual evidence.

3. **Normalize account facts.**
   - Account name, Xiaohongshu ID, location, bio, follower count, likes/collects if visible.
   - Service categories, local market, delivery promise, product lines, and visible pinned notes.
   - Screenshot asset paths copied into the local report asset folder.

4. **Score notes for Juguang.**
   - Prioritize buyer-intent comments over likes alone.
   - Separate flower-gift, event-decoration, trust/avoidance, and pure-case content.
   - Rank candidates as S / A / A- / B / not recommended.
   - Use `references/report-checklist.md` for the scoring table and report sections.

5. **Write actionable optimizations.**
   - Homepage: nickname, bio, location keywords, service scope, DM format.
   - Pinned notes: ordering guide, price bands, delivery range, event-process case collection.
   - Content matrix: product line, scenario line, trust line, conversion line.
   - Title rewrites: keep local search terms while adding platform-native hooks.
   - Juguang plan: budget, objective, placement/search keywords, evaluation metrics, stop rules.

6. **Generate deliverables.**
   - Create an HTML report in the current workspace.
   - Create a Word report using the `documents` skill and render/verify it.
   - Create an Obsidian Markdown note in the user's account-diagnosis folder.
   - Update the Obsidian diagnosis index without duplicating links.

7. **Verify and summarize.**
   - Verify all output files exist.
   - For Word, render to PNG/PDF and inspect pages for clipping, overlap, and unreadable tables.
   - For HTML, parse/check local image references at minimum; browser screenshot when layout risk is high.
   - In the final answer, include clickable absolute file links and state that no live ad changes were made unless actually performed.

## Default Paths

Use the current workspace for reports unless the user gives another path.

Suggested report folder when the user wants a stable local location:

`$HOME/Documents/花店小红书账号优化报告`

Suggested Obsidian account diagnosis folder:

`$HOME/Documents/花店小红书运营文件/Obsidian知识库/30-账号诊断`

Suggested Obsidian index:

`$HOME/Documents/花店小红书运营文件/Obsidian知识库/30-账号诊断/账号诊断资料清单.md`

## Helper Script

To create standard local folders and suggested output names:

```bash
python3 ~/.codex/skills/flower-shop-account-optimization/scripts/init_account_report.py \
  --account "晚风里的花" \
  --date 2026-07-03
```

The script only creates folders and prints paths. It does not fetch Xiaohongshu data or write the final report.

## Output Contract

The final report should include:

- One-page executive summary.
- Evidence base and data limitations.
- Current advantages and core issues.
- Juguang candidate table with rank, note title, data, judgment, and next action.
- Not-recommended note categories.
- Homepage and pinned-note optimization.
- Content matrix and title rewrite examples.
- First-round Juguang plan.
- 7-day action plan.
- Source links and screenshot references.

## Safety

- Do not publish, like, comment, follow, or modify Xiaohongshu content.
- Do not operate live Juguang campaigns unless the user explicitly asks and account permissions are available.
- Do not claim that files, Obsidian notes, or Word verification succeeded unless verified.
- Do not overwrite old Obsidian notes; create dated notes and update indexes idempotently.
- If editing Feishu docs, preserve visible revision traces according to the user's preference: deleted/replaced source text should remain with strikethrough and new text should be purple where supported.
