#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
except ModuleNotFoundError as exc:
    raise SystemExit(
        "This script requires Pillow. Install it with: python3 -m pip install Pillow"
    ) from exc


PRESETS = {
    "natural": {
        "rgb": (1.015, 1.005, 1.0),
        "brightness": 1.045,
        "contrast": 1.065,
        "color": 1.045,
        "sharpness": 1.14,
        "blur_radius": 0.45,
        "blend": 1.16,
    },
    "high-key": {
        "rgb": (1.025, 1.012, 0.995),
        "brightness": 1.075,
        "contrast": 1.055,
        "color": 1.035,
        "sharpness": 1.12,
        "blur_radius": 0.55,
        "blend": 1.14,
    },
    "warm": {
        "rgb": (1.035, 1.012, 0.985),
        "brightness": 1.055,
        "contrast": 1.07,
        "color": 1.06,
        "sharpness": 1.15,
        "blur_radius": 0.5,
        "blend": 1.17,
    },
}


def parse_size(text: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+)x(\d+)", text.strip().lower())
    if not match:
        raise argparse.ArgumentTypeError("size must look like 1080x1440")
    return int(match.group(1)), int(match.group(2))


def parse_aspect(text: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+):(\d+)", text.strip())
    if not match:
        raise argparse.ArgumentTypeError("aspect must look like 3:4 or 4:5")
    return int(match.group(1)), int(match.group(2))


def apply_rgb_gains(img: Image.Image, gains: tuple[float, float, float]) -> Image.Image:
    r, g, b = img.split()
    channels = []
    for channel, gain in zip((r, g, b), gains):
        channels.append(channel.point(lambda value, gain=gain: max(0, min(255, int(value * gain)))))
    return Image.merge("RGB", tuple(channels))


def optimize(img: Image.Image, preset_name: str) -> Image.Image:
    preset = PRESETS[preset_name]
    img = ImageOps.exif_transpose(img).convert("RGB")
    img = apply_rgb_gains(img, preset["rgb"])
    img = ImageEnhance.Brightness(img).enhance(preset["brightness"])
    img = ImageEnhance.Contrast(img).enhance(preset["contrast"])
    img = ImageEnhance.Color(img).enhance(preset["color"])
    img = ImageEnhance.Sharpness(img).enhance(preset["sharpness"])

    # Mild clarity without making petals crunchy.
    blurred = img.filter(ImageFilter.GaussianBlur(radius=preset["blur_radius"]))
    return Image.blend(blurred, img, preset["blend"])


def crop_to_aspect(img: Image.Image, aspect: tuple[int, int]) -> Image.Image:
    target = aspect[0] / aspect[1]
    width, height = img.size
    current = width / height
    if current > target:
        new_width = round(height * target)
        left = max(0, (width - new_width) // 2)
        return img.crop((left, 0, left + new_width, height))
    new_height = round(width / target)
    top = max(0, (height - new_height) // 2)
    return img.crop((0, top, width, top + new_height))


def unique_output_path(out_dir: Path, stem: str, suffix: str) -> Path:
    candidate = out_dir / f"{stem}{suffix}"
    counter = 2
    while candidate.exists():
        candidate = out_dir / f"{stem}-{counter}{suffix}"
        counter += 1
    return candidate


def process_image(src: Path, args: argparse.Namespace) -> list[Path]:
    img = Image.open(src)
    optimized = optimize(img, args.preset)
    outputs: list[Path] = []

    if args.keep_full:
        full_path = unique_output_path(args.out_dir, f"{src.stem}-optimized-full", ".jpg")
        optimized.save(full_path, quality=args.quality, optimize=True, progressive=True)
        outputs.append(full_path)

    cropped = crop_to_aspect(optimized, args.aspect)
    resized = cropped.resize(args.size, Image.Resampling.LANCZOS)
    main_path = unique_output_path(args.out_dir, f"{src.stem}-optimized-{args.size[0]}x{args.size[1]}", ".jpg")
    resized.save(main_path, quality=args.quality, optimize=True, progressive=True)
    outputs.append(main_path)

    if args.upload_copy:
        upload_size = (720, round(720 * args.aspect[1] / args.aspect[0]))
        upload = cropped.resize(upload_size, Image.Resampling.LANCZOS)
        upload_path = unique_output_path(args.out_dir, f"{src.stem}-upload-{upload_size[0]}x{upload_size[1]}", ".jpg")
        upload.save(upload_path, quality=90, optimize=True, progressive=True)
        outputs.append(upload_path)

    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Optimize flower-shop photos for social posting.")
    parser.add_argument("images", nargs="+", type=Path, help="Input image paths")
    parser.add_argument("--out-dir", type=Path, default=Path("optimized"), help="Output directory")
    parser.add_argument("--preset", choices=sorted(PRESETS), default="natural")
    parser.add_argument("--aspect", type=parse_aspect, default=(3, 4), help="Crop aspect, e.g. 3:4 or 4:5")
    parser.add_argument("--size", type=parse_size, default=(1080, 1440), help="Main export size, e.g. 1080x1440")
    parser.add_argument("--quality", type=int, default=95, help="JPEG quality")
    parser.add_argument("--upload-copy", action="store_true", help="Also create a smaller upload copy")
    parser.add_argument("--keep-full", action="store_true", help="Also save optimized uncropped full image")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for src in args.images:
        if not src.exists():
            raise FileNotFoundError(src)
        for out in process_image(src, args):
            print(out)


if __name__ == "__main__":
    main()
