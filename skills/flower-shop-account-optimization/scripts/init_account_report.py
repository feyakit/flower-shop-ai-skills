#!/usr/bin/env python3
"""Initialize local paths for a Xiaohongshu account diagnosis report."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
from pathlib import Path


DEFAULT_WORKSPACE = Path(os.environ.get("XHS_ACCOUNT_REPORT_WORKSPACE", "xhs-account-reports"))
DEFAULT_OBSIDIAN_DIR = Path(
    os.environ.get("XHS_ACCOUNT_OBSIDIAN_DIR", "xhs-account-diagnosis-notes")
)


def slugify(text: str) -> str:
    ascii_slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    if ascii_slug:
        return ascii_slug[:48]
    compact = re.sub(r"\s+", "", text)
    return compact[:24] or "xhs-account"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create standard report paths for an XHS account diagnosis.")
    parser.add_argument("--account", required=True, help="Account display name.")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="Report date, YYYY-MM-DD.")
    parser.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)
    parser.add_argument("--obsidian-dir", type=Path, default=DEFAULT_OBSIDIAN_DIR)
    parser.add_argument("--index-number", default="", help="Optional Obsidian note sequence, e.g. 07.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    account = args.account.strip()
    slug = slugify(account)
    assets_dir = args.workspace / "assets" / slug
    assets_dir.mkdir(parents=True, exist_ok=True)
    args.obsidian_dir.mkdir(parents=True, exist_ok=True)

    base = f"{account}小红书账号优化与聚光投放报告"
    prefix = f"{args.index_number}-" if args.index_number else ""
    obsidian_name = f"{prefix}{account}小红书账号优化与聚光投放建议-{args.date}.md"

    paths = {
        "assets_dir": assets_dir,
        "html_report": args.workspace / f"{base}.html",
        "word_report": args.workspace / f"{base}.docx",
        "obsidian_note": args.obsidian_dir / obsidian_name,
        "obsidian_index": args.obsidian_dir / "账号诊断资料清单.md",
    }

    for key, value in paths.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
