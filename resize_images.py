# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "Pillow",
# ]
# ///
"""Resize images to a maximum width, preserving aspect ratio and EXIF.

Overwrites in place unless --out-dir is given.

    # Resize every image under content/photos to 1200px wide
    uv run resize_images.py --max-width 1200 content/photos

    # Write resized copies to a staging directory
    uv run resize_images.py --max-width 1200 --out-dir out content/photos
"""

import argparse
from pathlib import Path

from PIL import Image


def resize_image(
    src: Path,
    max_width: int,
    out_dir: Path | None,
    quality: int,
) -> None:
    with Image.open(src) as img:
        # Preserve original EXIF
        exif = img.info.get("exif")

        width, height = img.size
        if width <= max_width:
            print(f"{src}  →  already ≤ {max_width}px, skipped")
            return

        ratio = max_width / width
        new_size = (max_width, int(height * ratio))

        resized = img.resize(new_size, Image.LANCZOS)

        save_kwargs: dict = {}
        if exif:
            save_kwargs["exif"] = exif

        # Preserve quality for JPEG
        if img.format == "JPEG":
            save_kwargs["quality"] = quality
            save_kwargs["optimize"] = True

        dest = (out_dir / src.name) if out_dir else src
        if out_dir:
            out_dir.mkdir(parents=True, exist_ok=True)

        resized.save(dest, format=img.format, **save_kwargs)

        w, h = resized.size
        print(f"{src}  →  {w}×{h} ({src.stat().st_size / 1024:.0f} KB)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resize images to a maximum width, preserving EXIF."
    )
    parser.add_argument(
        "sources",
        nargs="+",
        type=Path,
        help="Image files or directories to resize.",
    )
    parser.add_argument(
        "--max-width",
        "-w",
        type=int,
        default=4032,
        help="Maximum width in pixels (default: 4032).",
    )
    parser.add_argument(
        "--quality",
        "-q",
        type=int,
        default=95,
        help="JPEG quality 1-100 (default: 95).",
    )
    parser.add_argument(
        "--out-dir",
        "-o",
        type=Path,
        default=None,
        help="Write resized files to this directory instead of overwriting.",
    )
    args = parser.parse_args()

    extensions = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}

    files: list[Path] = []
    for src in args.sources:
        if src.is_dir():
            files.extend(
                sorted(p for p in src.rglob("*") if p.suffix.lower() in extensions)
            )
        elif src.is_file():
            files.append(src)
        else:
            print(f"Warning: {src} does not exist, skipping")

    for f in files:
        resize_image(f, args.max_width, args.out_dir, args.quality)


if __name__ == "__main__":
    main()
