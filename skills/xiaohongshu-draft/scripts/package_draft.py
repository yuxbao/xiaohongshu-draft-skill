#!/usr/bin/env python3
"""Package a Markdown Xiaohongshu draft and images into an offline ZIP."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

SUPPORTED = {".png", ".jpg", ".jpeg", ".webp"}


def natural_key(path: Path) -> list[object]:
    return [int(part) if part.isdigit() else part.casefold()
            for part in re.split(r"(\d+)", path.name)]


def collect_images(image_dir: Path) -> list[Path]:
    if not image_dir.is_dir():
        raise ValueError(f"image directory does not exist: {image_dir}")
    images = sorted(
        (path for path in image_dir.iterdir()
         if path.is_file() and not path.is_symlink() and path.suffix.lower() in SUPPORTED
         and "/" not in path.name and "\\" not in path.name),
        key=natural_key,
    )
    if not images:
        raise ValueError(f"no supported images found in: {image_dir}")
    return images


def package(copy_file: Path, image_dir: Path, output: Path) -> list[Path]:
    if not copy_file.is_file():
        raise ValueError(f"draft Markdown file does not exist: {copy_file}")
    images = collect_images(image_dir)
    output = output.resolve()
    if output == copy_file.resolve() or output.parent == image_dir.resolve():
        raise ValueError("output ZIP must not replace the Markdown or sit in the image directory")
    manifest = {
        "format": "xiaohongshu-draft-bundle-v1",
        "note": "draft.md",
        "images": [f"images/{image.name}" for image in images],
        "publication_status": "local bundle only; not uploaded or saved on Xiaohongshu",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(copy_file, "draft.md")
        for image in images:
            archive.write(image, f"images/{image.name}")
        archive.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return images


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--copy", required=True, type=Path, help="Markdown file containing title and note copy")
    parser.add_argument("--images", required=True, type=Path, help="directory of selected PNG/JPG/JPEG/WebP images")
    parser.add_argument("--output", required=True, type=Path, help="output ZIP path")
    args = parser.parse_args()
    try:
        images = package(args.copy, args.images, args.output)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"Created local bundle: {args.output} ({len(images)} images)")
    print("This ZIP is not an uploaded or saved Xiaohongshu draft.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
