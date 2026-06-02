# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "PyExifTool",
# ]
# ///
"""List image files sorted by capture date (from EXIF data).

Outputs relative paths suitable for pasting as the inputs argument to
prepare_images.py.  Use it like this:

    uv run prepare_images.py $(uv run list_images_by_date.py content/photos)
"""

import argparse
from pathlib import Path

from exiftool import ExifToolHelper


def main() -> None:
    parser = argparse.ArgumentParser(
        description="List images sorted by EXIF capture date."
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory containing images to scan.",
    )
    args = parser.parse_args()

    directory: Path = args.directory.resolve()
    if not directory.is_dir():
        parser.error(f"{directory} is not a directory")

    # Collect every image in the tree
    extensions = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic", ".heif", ".webp"}
    paths = sorted(
        p for p in directory.rglob("*") if p.suffix.lower() in extensions
    )

    if not paths:
        return

    with ExifToolHelper() as eth:
        # Ask exiftool for DateTimeOriginal (fast – one invocation)
        metadata = eth.get_tags(
            [str(p) for p in paths],
            tags="DateTimeOriginal",
        )

    # Pair each path with its date, falling back to "0" so undated files
    # sort to the front (you can easily spot them).
    dated: list[tuple[str, Path]] = []
    for i, p in enumerate(paths):
        dt = metadata[i].get("EXIF:DateTimeOriginal", "0")
        dated.append((dt, p))

    dated.sort(key=lambda item: item[0])

    # Print paths relative to the current working directory (or the
    # directory argument itself) so prepare_images.py finds them.
    cwd = Path.cwd()
    for _, p in dated:
        try:
            rel = p.relative_to(cwd)
        except ValueError:
            rel = p
        print(rel)


if __name__ == "__main__":
    main()
