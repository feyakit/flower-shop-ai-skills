---
name: xhs-flower-draft-workflow
description: >
  End-to-end Xiaohongshu/小红书 workflow for flower-shop assets: optimize bouquet
  or flower-basket photos, write local-customer-acquisition titles and body copy,
  choose topics using the taught city-first buyer-intent order, and save the result
  to a Xiaohongshu draft box. Use when Codex is asked to process flower shop
  student素材, 成都/上海/南通/北京等本地花店素材, 图片优化, 小红书标题正文话题, or
  upload/save to 草稿箱. Requires per-account Xiaohongshu cookies when using
  cookie-based APIs or account-specific publishing; cookies must be supplied at
  runtime and never hard-coded.
---

# XHS Flower Draft Workflow

## Overview

Use this skill to turn flower-shop素材 into a Xiaohongshu draft without publishing. The standard path is:

1. Optimize images for Xiaohongshu.
2. Write a local flower-shop title and body copy.
3. Choose topics in the taught buyer-intent order.
4. Save to the correct account's draft box.
5. Verify the draft has the expected title, image count, and body content.

Never publish unless the user explicitly asks to publish. Default to saving a draft.

## Required Account Rule

Every Xiaohongshu account has its own cookie. Treat cookie data as a required runtime field for cookie-based workflows:

- Required field: `cookies_str` or `cookies`.
- Required scope: one value per account, never shared implicitly across accounts.
- Source: user input, local untracked account config, secret manager, environment variable, or already-authenticated browser session.
- Prohibited: do not hard-code cookies into this skill, GitHub repo, examples, logs, screenshots, or generated Markdown.
- If the selected account has no cookie or authenticated browser session, stop and ask for that account's cookie/login.

Read [references/account-cookies.md](references/account-cookies.md) before any cookie-based API call or multi-account draft workflow.

## Workflow

### 1. Inspect And Optimize Images

Inspect all provided images. Identify the best cover by sellability, not just cleanliness:

- Prefer a human-held image when it shows size and gift impact.
- Use clean product-only images as supporting detail images.
- Crop/export 3:4 vertical, usually `1080x1440`.
- Also create upload copies around `900x1200` or `720x960` when browser upload is unstable.
- Keep real flower texture. Do not invent flowers, change product structure, or over-filter petals.

Read [references/image-copy-workflow.md](references/image-copy-workflow.md) for the image and copy checklist.

### 2. Write Title And Body

Write for local customer acquisition:

- Title: short, Xiaohongshu-native, with a city word when local acquisition matters.
- Body: emotion first, then flower details, then recipient/scenario, then conversion info.
- Do not invent prices, store names, exact delivery promises, or stock availability.
- Use city/store lines only when supported by user context.

### 3. Choose Topics

Choose topics in the taught order:

1. City flower-shop search word.
2. City ordering / same-city transaction word.
3. Recipient buyer-intent word.
4. City + occasion word.
5. Occasion / relationship word.
6. Product/material/style word.
7. Product-format word.

For detailed patterns and examples, read [references/topic-selection.md](references/topic-selection.md).

### 4. Save To Draft Box

Use the safest available draft path:

- Prefer browser/OpenCLI draft save when the browser is already logged into the correct account.
- Use cookie-based API only when the selected account's `cookies_str`/`cookies` is available.
- Always pass a draft/save flag. Never trigger final publish by default.
- If platform-direct topic binding fails, do not force unverified topics into the body. Save the draft without bound topics and report the suggested manual topics.

Read [references/draft-save.md](references/draft-save.md) before saving drafts.

### 5. Verify And Clean Up

After saving:

- Verify the draft title.
- Verify image count.
- Verify body content. If normal draft readers return empty content, inspect raw local draft fields such as `content.draftStore.desc` and `descInnerHTML`.
- Clean duplicate failed drafts only when they are clearly created by the current task.
- Report any limitation clearly, especially failed topic binding or missing account cookies.
