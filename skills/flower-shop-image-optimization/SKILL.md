---
name: flower-shop-image-optimization
description: Optimize bouquet and flower-shop photos for Xiaohongshu/小红书, WeChat, and social posting, including natural color correction, high-key bouquet brightening, gentle sharpening, EXIF orientation, 3:4 and 4:5 crops, 1080x1440 or 1080x1350 exports, smaller upload copies, and image-edit prompts. Use when the user asks for 花店图片优化, 花束修图, 小红书图片处理, 封面图优化, 原相机参数感, 照片变亮变干净, 批量修花图, or upload-ready flower images.
---

# Flower Shop Image Optimization

## Core Goal

Prepare flower-shop photos for social posting while preserving real flower texture and commercial credibility.

Optimize for:

- Clean, bright first impression.
- Realistic flower color, not plastic saturation.
- Clear bouquet focal point.
- Xiaohongshu-friendly vertical crops.
- Stable upload copies for browser/OpenCLI workflows.

Default to Chinese when the user writes Chinese.

## Workflow

1. Inspect the input image if available.
2. Identify the intended style: natural phone photo, high-key product photo, warm indoor shop photo, cool editorial image, or bouquet close-up.
3. Use deterministic image processing for simple improvements:
   - EXIF orientation correction.
   - Gentle exposure and contrast lift.
   - White balance correction.
   - Moderate saturation and sharpening.
   - Crop/export to 3:4 or 4:5.
4. Use image generation/editing only when the user asks for content-level changes such as replacing background, removing clutter, changing wrapping, or redesigning the bouquet.
5. Return output paths and briefly state what changed.

## Built-In Script

Use the script for batch upload-ready copies:

```bash
python3 ~/.codex/skills/flower-shop-image-optimization/scripts/optimize_flower_images.py \
  image1.jpg image2.jpg \
  --out-dir ./optimized \
  --preset natural \
  --aspect 3:4 \
  --size 1080x1440 \
  --upload-copy
```

The script requires Pillow. If the target Mac reports `No module named 'PIL'`, install it in that Python environment:

```bash
python3 -m pip install Pillow
```

Useful variants:

```bash
# 4:5 Xiaohongshu crop
python3 ~/.codex/skills/flower-shop-image-optimization/scripts/optimize_flower_images.py *.jpg --aspect 4:5 --size 1080x1350

# Softer high-key bouquet correction
python3 ~/.codex/skills/flower-shop-image-optimization/scripts/optimize_flower_images.py *.jpg --preset high-key

# Warmer indoor shop correction
python3 ~/.codex/skills/flower-shop-image-optimization/scripts/optimize_flower_images.py *.jpg --preset warm
```

If the skill is being used from a cloned repository before installation, run the same commands from that repository's `skills/flower-shop-image-optimization/scripts` directory.

## Editing Judgment

- Preserve real petal texture; avoid waxy skin-smoothing style on flowers.
- Do not over-whiten wrapping until flowers lose detail.
- Do not oversaturate reds and yellows; they clip easily.
- Keep shadows soft enough to show bouquet volume.
- For product inspection, prefer realistic clarity over trendy filters.
- For covers, crop around the bouquet face and leave room for title text.

## Reference

Read `references/photo-optimization-playbook.md` when deciding crop, preset, prompt wording, or when the user asks why a flower photo looks cheap/dirty/dim.

## Safety

- Do not overwrite original photos.
- Do not commit customer/private photos into the skill repository.
- Do not claim image quality was verified unless the output was opened or inspected.
