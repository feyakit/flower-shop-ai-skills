---
name: xhs-flower-shop-growth
description: Create Xiaohongshu/小红书 content for flower shops and flower-shop students focused on local customer acquisition. Use when the user provides bouquet/flower-shop photos or videos and asks for 小红书标题、正文、话题、标签、草稿箱、花店获客文案、爆款标题公式, or asks to write city-specific flower shop posts such as 成都/南通/上海/北京花店素材, birthday bouquets, girlfriend/boyfriend bouquets, best-friend bouquets, graduation bouquets, anniversary flowers, or same-city ordering posts.
---

# Xiaohongshu Flower Shop Growth

## Core Goal

Turn flower shop assets into Xiaohongshu posts that can attract local customers, not just display pretty work. Optimize for:

- Local search: city + flower shop + ordering/delivery terms.
- Human desire: girlfriend, birthday, anniversary, first date, best friend, opening gift.
- Conversion: budget, style, recipient, delivery/self-pickup, DM invitation.
- Safety: save drafts only unless the user explicitly asks to publish.

Default the local market to 成都 only when the user has said they operate a Chengdu flower shop or the current task clearly references Chengdu. Otherwise ask once or infer from user-provided context.

## Workflow

1. Inspect the user's images and identify sellable angles: style, colors, flowers, scene, recipient, gifting moment, and best cover image.
2. If a title-formula spreadsheet is provided, read it and extract formulas. Otherwise use `references/title-formulas.md`.
3. Optimize images for Xiaohongshu:
   - Main deliverables: 3:4 vertical, usually 1080x1440.
   - For browser/OpenCLI upload instability: create a smaller 720x960 or 900x1200 upload copy.
   - Preserve real flower texture; avoid heavy filters.
4. Write titles using Xiaohongshu-native formulas, not flat SEO labels. Prefer the specific formula requested by the user.
5. Write body copy with the learned flower-shop student structure:
   - Emotional opening.
   - Bouquet description: color, flower materials, packaging, style, and sellable detail.
   - Recipient + scene: girlfriend, boyfriend, best friend, mom, birthday, anniversary, graduation, date, first meeting, etc.
   - Store information: city flower shop, same-city delivery, handwritten card, custom bouquet, budget/style DM.
   - Search topics: 8-10 tags, ordered by local search and buyer intent.
6. Save to Xiaohongshu draft box:
   - Prefer `opencli xiaohongshu publish ... --draft --site-session persistent`.
   - Never click or call final publish unless explicitly requested.
   - Verify the draft list shows the expected title and image count.
   - If `draft-open` shows empty content, read raw IndexedDB fields when needed; newer creator drafts may store body in `content.draftStore.desc` and `descInnerHTML`.
7. Clean up failed duplicate drafts created during retries when they are clearly yours and have the same title/images.

## Title Rules

Do not use bland titles such as `成都花店｜蓝白花束适合送礼` as the main version. They are searchable but lack platform feel.

Default target: about 20 Chinese characters, with one tasteful emoji when useful. Include a local city word such as `成都花店`, `南通花店`, `上海花店`, or `北京花店` unless the user asks otherwise.

Use one of these patterns:

- `女朋友想收到的蓝白花束｜成都花店`
- `哪个女生能拒绝蓝白花束呀｜成都花店`
- `真有女生收到这束花会不心动吗`
- `见女朋友前顺手买了束花｜成都花店`
- `美到失语的蓝白蝴蝶兰花束｜成都花店`
- `男朋友审美开窍了｜成都花店`
- `这束花的美值得单独发条朋友圈`

Keep titles typically within Xiaohongshu's creator title limit. If using OpenCLI publish, keep title at or under 20 Chinese characters unless the tool/page accepts more.

## Default Body Shape

```text
{情绪开场，先写收到花/送花的人会有什么感受。}

{花束描述：花材、色系、包装、风格、特点。}

{人群 + 场景：适合送给谁，适合什么场景。}

📍{城市}花店
🚗{城市}同城可配送
💌可搭配手写贺卡，支持按预算、色系和送花对象定制

#{城市花店} #{城市买花} #{送花对象花束} #{使用场景花束} #{产品/风格词} #{同城配送词}
```

When the user asks for higher quality 正文 or topics, read `references/content-and-topics.md`.

## Tooling Notes

- If the user provides `.xlsx` title formulas, use the spreadsheet skill or bundled Python/openpyxl to inspect sheet names and rows.
- If researching Xiaohongshu keywords, use the agent-reach/OpenCLI Xiaohongshu backend when available.
- For draft creation via OpenCLI, if topic binding fails, put hashtag text in the body and omit `--topics`.
- If image upload times out, generate smaller upload copies and increase `OPENCLI_BROWSER_COMMAND_TIMEOUT`.
- If OpenCLI creates partial drafts with title/images but empty body, delete only the drafts clearly created in the current task.

## References

Read `references/title-formulas.md` when the user asks for “网感”, “爆款标题”, “标题公式”, or when no current spreadsheet is provided.
Read `references/content-and-topics.md` when writing the body, topics, tags, store information, or student-ready Xiaohongshu copy.
