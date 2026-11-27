# Xiaohongshu Account Juguang Report Checklist

Use this reference when writing the report and candidate ranking.

## Evidence To Capture

- Account name, Xiaohongshu ID, profile URL, visible location/IP.
- Bio, service list, delivery promise, phone/DM hints if visible.
- Follows, followers, likes/collects.
- Pinned notes and first 20-40 public notes when accessible.
- For candidate notes: title, URL/id, likes, collects, comments, publication date, and comment examples.
- User screenshots copied into a report-local `assets/{slug}/` folder.

## Juguang Candidate Scoring

Rank notes by commercial intent, not vanity metrics alone.

### S

Use for first-round paid testing.

- Has explicit buying comments: `怎么买`, `在哪买`, `怎么定制`, `怎么联系`, `同城可以送吗`, `多少钱`, `有价格吗`.
- Content naturally supports conversion: product合集, price bands, delivery range, recipient/scenario choice, or strong local search.
- Cover/title can be improved without changing the note's core promise.

### A

Worth testing after small optimization.

- Has some comment intent or strong local-search value.
- Explains ordering, delivery, selection, process, or risk reduction.
- Needs cover, title, pinned comment, or DM format before spend.

### A-

Use mainly for trust or retargeting; avoid large first-round budget.

- Comments are supportive but not strongly buyer-intent.
- Topic may be defensive/avoidance-oriented, such as 避坑/声明/维权.
- Good for credibility after reframing into checklist/process/case proof.

### B

Do not test before repackaging.

- Pure case display with 0-3 likes and little comment intent.
- Good visual assets but weak title, no price/process/service detail.
- Convert into合集, comparison, price guide, or process note first.

### Not Recommended

- 0-like or 1-like single-product posts with no comments.
- Dark/unclear covers, tiny text, or no local/service keyword.
- Negative-tone statements that attract同行 support rather than buyer leads.
- Event case posts without package, process, budget, city, or booking info.

## Required Report Sections

1. 账号识别与结论
2. 数据来源与限制
3. 当前优势
4. 核心问题
5. 适合聚光推广的笔记
6. 不建议直接投的内容
7. 主页优化
8. 内容矩阵
9. 标题/封面重写方向
10. 首轮聚光方案
11. 7 天动作表
12. 资料来源

## Flower-Shop Local Acquisition Heuristics

- Separate 花礼线 and 布置线. Avoid making one homepage carry every service equally.
- Flower-gift notes should foreground recipient, budget, city, delivery, and customization.
- Event-decoration notes should foreground scenario, package/process, communication, budget range, before/after, and booking lead time.
- Trust notes should answer risk: fake cases, hidden fees, no communication, poor landing quality.
- Good local titles combine platform hook + local search term, for example:
  - `平度送女友花束合集｜不会选就看这篇`
  - `平度花店 100-300 花束参考｜生日约会都能用`
  - `平度婚房布置流程｜订婚前先看这篇`

## First-Round Juguang Plan

Default recommendation when no ad account data is available:

- Objective: private-message leads or customer acquisition, not likes.
- Budget: 50-100 RMB/day per candidate note for 3 days.
- Priority: 1-2 S notes first; do not split budget across many weak notes.
- Search keywords: city + flower shop / buy flowers / order flowers / birthday bouquet / girlfriend bouquet; add event terms for wedding/engagement only after the landing note is rebuilt.
- Evaluation: private-message starts, price inquiries, qualified leads, appointments, and transactions. Likes and saves are secondary.
- Stop rule: no buyer-intent messages after the test window, or comments/DMs reveal mismatch between note promise and service offer.

## Obsidian Note Metadata

Recommended frontmatter:

```yaml
---
type: 小红书账号诊断
platform: 小红书
account: "{account}"
date: YYYY-MM-DD
tags:
  - 小红书
  - 花店运营
  - 聚光推广
  - 账号诊断
---
```

Index link format:

```markdown
- [[NN-账号名小红书账号优化与聚光投放建议-YYYY-MM-DD]]
```
