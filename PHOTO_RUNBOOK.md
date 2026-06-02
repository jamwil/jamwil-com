# Photo Pipeline Runbook

Three scripts that take edited RAWs from Photomator (or Apple Photos) through to
Zola-ready markdown snippets.

---

## Rationale

You edit RAWs in **Photomator**, which handles the RAW → raster conversion
(demosaicing, tone curves, color grading). That export is your _master_.
Everything downstream should preserve its fidelity.

| Step                    | Tool                     | What it does                                                                                                      |
| ----------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| **Export**              | Photomator / Photos      | JPEG 100%, no size cap                                                                                            |
| **Resize** (safety net) | `resize_images.py`       | Downscale anything wider than 4032px at quality 95 — near-lossless, only touches images that exceed the threshold |
| **Sort**                | `list_images_by_date.py` | Order by EXIF capture date                                                                                        |
| **Snippet + clean**     | `prepare_images.py`      | Strip GPS/serial/private EXIF, emit Zola shortcodes + metadata table                                              |

The key insight: at 4032px (≈ iPhone 15 Pro native), **most photos won't get
resized at all**. The resize script only acts on files from higher-resolution
sensors (e.g. full-frame mirrorless at 6000px+). Quality 95 is chosen because
quality is non-linear after ~90 — 95 gives you effectively lossless fidelity for
the web while keeping file sizes reasonable for the occasional file that _does_
get re-encoded.

---

## The Scripts

| Script                   | Purpose                                                                                    | Dependencies          |
| ------------------------ | ------------------------------------------------------------------------------------------ | --------------------- |
| `resize_images.py`       | Downscale images exceeding 4032px (safety net); preserves EXIF, near-lossless quality (95) | `Pillow`              |
| `list_images_by_date.py` | List images sorted by capture date (EXIF `DateTimeOriginal`)                               | `PyExifTool`          |
| `prepare_images.py`      | Strip sensitive EXIF, print a Zola HTML snippet + `resize_image` shortcode                 | `click`, `PyExifTool` |

All three use PEP 723 inline metadata:

```bash
uv run resize_images.py --help
uv run list_images_by_date.py --help
uv run prepare_images.py --help
```

---

## Prerequisites

```bash
# exiftool (system) — needed by PyExifTool
sudo apt install libimage-exiftool-perl   # Ubuntu / Debian
# brew install exiftool                   # macOS

# uv (Python package runner)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Step-by-Step Pipeline

### 0. Export from Photomator / Apple Photos

- File format: **JPEG**
- Quality: **100% / Maximum**
- Size: **No limit** (full resolution)

Copy / symlink exports into your Zola content tree, e.g.
`content/photos/event-name/`.

### 1. Resize (safety net)

Catches anything wider than 4032px and brings it down without perceptible
quality loss. Images already ≤ 4032px pass through untouched.

```bash
# Overwrite in place (work on copies of your exports)
uv run resize_images.py content/photos/event-name/

# Or write resized versions to a staging directory
uv run resize_images.py -o content/photos/event-name/ ~/exports/event-name/

# Explicit threshold
uv run resize_images.py --max-width 4032 --quality 95 content/photos/event-name/
```

### 2. List in chronological order

```bash
uv run list_images_by_date.py content/photos/event-name/
```

Output:

```
content/photos/event-name/IMG_4402.jpg
content/photos/event-name/IMG_4405.jpg
content/photos/event-name/IMG_4411.jpg
```

### 3. Generate Zola snippets + strip EXIF

Pipe the sorted list into `prepare_images.py`.

```bash
# Preview snippets in terminal
uv run prepare_images.py $(uv run list_images_by_date.py content/photos/event-name/)

# Save to a Zola page
uv run prepare_images.py \
    $(uv run list_images_by_date.py content/photos/event-name/) \
    > content/posts/event.md

# Clean EXIF too (removes GPS, serial numbers, etc.)
uv run prepare_images.py --clean \
    $(uv run list_images_by_date.py content/photos/event-name/) \
    > content/posts/event.md
```

Each image produces:

```html
{{ resize_image(path="content/photos/event-name/IMG_4402.jpg", width=500,
height=500, op="fit_width", alt="") }}

<!-- content/photos/event-name/IMG_4402.jpg -->
<table>
  <tr>
    <td>Make</td>
    <td>Apple</td>
  </tr>
  <tr>
    <td>Camera Model Name</td>
    <td>iPhone 15 Pro</td>
  </tr>
  ...
  <tr>
    <td colspan="2">
      {{ image_link(path='photos/event-name/IMG_4402.jpg', text='View full
      resolution') }}
    </td>
  </tr>
</table>

<div style="clear:both;"></div>
```

> ⚠️ `--clean` modifies images in place. Run it on your working copies, not the
> Photomator originals.

---

## All-in-One

From Photomator export to published page:

```bash
# 1. Safety-net resize exports into content tree
uv run resize_images.py -o content/photos/event/ ~/exports/event/

# 2. Strip EXIF + emit page
uv run prepare_images.py --clean \
    $(uv run list_images_by_date.py content/photos/event/) \
    > content/posts/event.md
```

---

## Troubleshooting

| Problem                                        | Likely fix                                                              |
| ---------------------------------------------- | ----------------------------------------------------------------------- |
| `exiftool` not found                           | `sudo apt install libimage-exiftool-perl`                               |
| "No such file" from `prepare_images.py`        | Ensure paths from `list_images_by_date.py` resolve relative to `cwd`    |
| Images with no `DateTimeOriginal` sort first   | Check those files — they may lack EXIF or be screenshots                |
| Resize script skipped a file you wanted shrunk | It's already ≤ 4032px; pass `-w` to lower the threshold                 |
| Generational artifacts visible                 | Export from Photomator at 100%; use `--quality 98` in the resize script |
