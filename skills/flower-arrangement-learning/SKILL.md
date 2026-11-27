---
name: flower-arrangement-learning
description: Teach practical floristry by diagnosing and improving bouquet or floral arrangement photos using a commercial florist framework. Use when the user shares a bouquet/flower image and asks for 花艺学习, 花束诊断, 花艺缺陷, 怎么修改, 花艺师会怎么改, 包装/配色/层次/焦点问题, or wants an improved reference image based on critique.
---

# Flower Arrangement Learning

## Core Workflow

When the user provides a bouquet or floral arrangement image:

1. Inspect the image directly before judging. Identify the intended style first: round bouquet, natural style, Korean/ins style, open/closed form, hand-tied bouquet, boxed/basket arrangement, wedding item, or event installation.
2. Read `references/evaluation-framework.md` when detailed critique, teaching, or image-edit guidance is needed.
3. Diagnose from the commercial floristry lens: color, texture, form, proportion, focal point, line direction, density, depth, control of outline, packaging, and scenario fit.
4. Answer in practical florist language. Prefer: strengths, main defects, how to modify, and the order of operations.
5. If the user asks for a modified image, use image generation/editing with a prompt that preserves the original bouquet identity while applying the concrete fixes.

## Response Style

- Default to Chinese when the user writes Chinese.
- Be direct but constructive. Name the real defect rather than saying only "not harmonious."
- Tie each defect to a visual reason and a specific fix.
- For beginners, explain using simple design terms: 主色, 辅助色, 点缀色, 焦点, 层次, 疏密, 线条, 包装比例.
- Do not over-identify flower species when uncertain. Use visual categories such as 块状花, 线状花, 散状花, 面状花, 异形花, 叶材.
- When evaluating commercial value, consider first impression, photo effect, customer scenario, cost perception, and whether flowers or packaging are the visual lead.

## Output Template

Use this structure unless the user asks for another format:

```markdown
这束整体方向是：...

**优点**
...

**主要问题**
1. ...
2. ...

**如果我是花艺师，我会这样改**
...

**调整顺序**
1. ...
2. ...

一句话：...
```

For short requests, compress the template but keep concrete defects and fixes.

## Image Generation

When generating an improved reference image:

- Preserve the same camera angle, bouquet type, color family, and core flower identity unless the user requests a redesign.
- Apply only the critique-backed fixes: raise/lower flower face, reduce or reshape wrapping, clarify focal point, improve dome or line direction, reduce clutter, replace ribbon, add minor fillers, or create better spacing.
- State what was changed after generation, briefly.
