"""Turn the profile picture into the portrait cells that card.py draws.

Run it by hand when the profile picture changes, then commit the result:

    uv run --with pillow card/portrait.py AVATAR card/portrait.json

AVATAR is the profile picture at 460 x 460 pixels. The output is JSON:
"cells" holds one list per row, and each cell is null (blank) or
[tone 0-255, r, g, b]. "eyes" names the cells the blink redraws.

The crop, the masks and the eye cells are tuned to the current photo.
Check them against a render after a new photo.
"""
import json
import sys

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# These must match card.py, which draws each cell CELL_W wide and LINE_H high.
COLS = 92
CELL_W, LINE_H = 4.2, 8.0
CROP = (70, 20, 390, 440)
HAIR_ROWS = 17
EYES = {"rows": [30, 31, 32], "cols": [[16, 28], [45, 57]]}


def is_hair(rgb):
    r, g, b = rgb
    return r - b > 25 and (r + g + b) / 3 < 150


def portrait(path):
    im = Image.open(path).convert("RGB").crop(CROP)
    rows = int(COLS * im.height / im.width * CELL_W / LINE_H)
    small = im.filter(ImageFilter.UnsharpMask(4, 160)).resize((COLS, rows), Image.LANCZOS)
    small = ImageEnhance.Contrast(ImageEnhance.Color(small).enhance(1.6)).enhance(1.25)
    spans = []
    for y in range(rows):
        # The photo has sea and sky behind the face. Warm cells are hair and
        # skin, and every cell below the chin is shirt. Keep each row's span
        # from its first to its last kept cell, so eyes and shadows stay in.
        keep = []
        for x in range(COLS):
            r, g, b = small.getpixel((x, y))
            nx, ny = (x - COLS / 2) / (COLS * 0.5), (y - rows * 0.48) / (rows * 0.6)
            d = nx * nx + ny * ny
            sky = d > 0.3 and ny < 0.45 and (r + g + b) / 3 > 190
            keep.append(d < 1 and not sky and (r - b > 14 or ny > 0.45))
        kept = [x for x, k in enumerate(keep) if k]
        spans.append(range(kept[0], kept[-1] + 1) if kept else range(0))
    # Spread the tones of the kept cells alone, so the bright sky does not
    # squash the face into the middle of the ramp.
    mask = Image.new("L", small.size)
    for y, span in enumerate(spans):
        for x in span:
            mask.putpixel((x, y), 255)
    grey = ImageOps.equalize(small.convert("L"), mask)
    cells = [[(grey.getpixel((x, y)), small.getpixel((x, y))) if x in span else None
              for x in range(COLS)] for y, span in enumerate(spans)]
    # Sky shows through the curls on top of the head as pale cells. Paint
    # them in the median hair tone and colour, so the hair reads as one mass.
    hair = [c for row in cells[:HAIR_ROWS] for c in row if c and is_hair(c[1])]
    if hair:
        tone = sorted(c[0] for c in hair)[len(hair) // 2]
        colour = tuple(sorted(c[1][i] for c in hair)[len(hair) // 2] for i in range(3))
        for row in cells[:HAIR_ROWS]:
            for x, c in enumerate(row):
                if c and not is_hair(c[1]):
                    row[x] = (tone, colour)
    return [[None if c is None else [c[0], *c[1]] for c in row] for row in cells]


if __name__ == "__main__":
    src, dest = sys.argv[1:3]
    rows = ",\n".join("  " + json.dumps(row, separators=(",", ":")) for row in portrait(src))
    with open(dest, "w") as f:
        f.write(f'{{"eyes": {json.dumps(EYES)},\n"cells": [\n{rows}\n]}}\n')
