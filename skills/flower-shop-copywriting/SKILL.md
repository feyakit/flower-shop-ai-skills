---
name: flower-shop-copywriting
description: Create Chinese Xiaohongshu/小红书 copywriting packages for flower shops and flower-shop students, including titles, body copy, hashtags, cover text, city-local search terms, buyer-scene angles, bouquet descriptions, and draft-ready content. Use when the user asks for 花店写文案, 花店小红书文案, 花店获客文案, 标题/正文/话题/标签, 爆款标题公式, 朋友圈/私域种草文案, or city-specific flower shop posts for bouquets, birthdays, anniversaries, graduation, girlfriends, boyfriends, best friends, and same-city delivery.
---

# Flower Shop Copywriting

## Core Goal

Turn flower shop assets into copy that can attract local buyers, not just describe pretty flowers.

Optimize for:

- Local search: city + flower shop + buying/ordering/delivery terms.
- Human desire: girlfriend, birthday, anniversary, first date, best friend, graduation, opening gift.
- Conversion: budget, style, recipient, delivery/self-pickup, DM invitation.
- Platform feel: Xiaohongshu-native titles and concise body copy.

Default to Chinese when the user writes Chinese.

## Input Handling

- If the user provides bouquet photos, inspect the image first and extract sellable angles: style, colors, flowers, recipient, gifting moment, size impression, wrapping, and best cover angle.
- If the city is missing, ask once unless context makes it obvious.
- If flower material is uncertain, describe visible categories and color/style instead of pretending to know exact species.
- If the user gives a required formula, follow it exactly.
- Do not invent prices, inventory, delivery range, discounts, or exact delivery time.

## Standard Workflow

1. Identify the buyer scenario: 送女友、送男友、送闺蜜、生日、纪念日、毕业、约会、开业、探店、妈妈/老师/领导.
2. Choose 3-8 titles with different hooks:
   - 情绪代入
   - 人群 + 场景
   - 反问/设问
   - 产品命名
   - 城市搜索
3. Write one polished body:
   - Emotional opening.
   - Bouquet description: color, flower materials when known, packaging, style, and sellable detail.
   - Recipient + scene.
   - Store conversion information: city flower shop, same-city delivery, handwritten card, custom budget/style.
4. Add 8-10 hashtags ordered by local search and buyer intent.
5. Add cover text suggestions when useful.
6. If asked for multiple posts, vary angle and title formula instead of repeating the same structure.

## Title Rules

Avoid flat directory titles as the main version:

- Weak: `成都花店｜蓝白花束适合送礼`
- Better: `女朋友想收到的蓝白花束｜成都花店`

Keep titles usually around 20 Chinese characters. Include a city term such as `成都花店`, `南通花店`, `上海花店`, or `北京花店` when local customer acquisition matters.

## Output Shape

Use this structure unless the user asks otherwise:

```text
标题备选：
1. ...
2. ...
3. ...

正文：
...

话题：
#城市花店 #城市买花 ...

封面字：
...
```

For student-ready batches, include a short "为什么这样写" note after the copy.

## References

Read `references/title-formulas.md` when the user asks for 网感、爆款标题、标题公式, or when no current spreadsheet is provided.

Read `references/content-and-topics.md` when writing正文、话题、标签、门店信息, or a student-ready Xiaohongshu content package.

## Safety

- Save drafts only when using publishing tools unless the user explicitly says to publish.
- Do not promise stock, price, delivery time, refund, or custom-replica accuracy without user-provided facts.
- If editing Feishu docs, preserve visible revision traces according to the user's preference: deleted/replaced source text should remain with strikethrough and new text should be purple where supported.
