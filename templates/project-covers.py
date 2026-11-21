#!/usr/bin/env python3
"""Project covers: one still-life photo series, same style for every project.

Each cover is generated as a 1536x1024 image from STYLE + the project's subject
(an object metaphor, never text or logos), then centre-cropped to 16:10 and
written to static/img/projects/<name>.jpg at 1280x800.

Usage: python3 templates/project-covers.py <dir with <name>.png files>
Needs Pillow (not a build dependency): uv run --with pillow python3 ...
"""
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "static/img/projects"
W, H = 1280, 800

STYLE = (
    "Editorial studio still-life photograph, medium-format film look, fine natural grain. "
    "One object group centered, occupying about 40 percent of the frame width with generous "
    "empty backdrop around it, camera at a 3/4 angle about 30 degrees above, 85mm lens, shallow "
    "depth of field. Seamless matte paper backdrop in warm stone grey (#d9d2c7), soft diffused "
    "daylight from the upper left, gentle long soft shadow to the lower right. Muted natural "
    "colours with one rich colour accent from the object itself. No text, no letters, no "
    "numbers, no logos, no people, no hands, no UI."
)

SUBJECTS = {
    "krea3": "three identical small ceramic vases side by side, glazed cobalt blue, speckled cream and deep green.",
    "krea2": "a small oval wooden artist palette with eight round dabs of oil paint in an arc, one flat brush across it.",
    "calculator": "a vintage wooden slide rule lying diagonally beside a small chrome stopwatch.",
    "flux": "a vintage 35mm film camera with a stack of coloured glass lens filters beside it.",
    "esqa": "a long strip of cream punched paper tape curling in loose loops.",
    "kandinsky": "a Bauhaus-style sculpture of painted wooden circles, a triangle and rods, a curl of film strip at its base.",
    "taskdiscovery": "two shallow ceramic dishes of amber and blue glass marbles, a few marbles between them.",
    "baselines": "a small brass balance scale, perfectly level, with polished brass calibration weights beside it.",
    "course": "a blank black school slate in a wooden frame, a stick of white chalk and a felt eraser beside it.",
    "linesearch": "a folding wooden carpenter's ruler partly unfolded in a zigzag, a brass compass divider next to it.",
}


def main(src):
    from PIL import Image
    for name in SUBJECTS:
        im = Image.open(Path(src) / f"{name}.png").convert("RGB")
        w, h = im.size
        ch = round(w * H / W)
        top = (h - ch) // 2
        im.crop((0, top, w, top + ch)).resize((W, H), Image.LANCZOS).save(
            OUT / f"{name}.jpg", quality=82, optimize=True, progressive=True)
        print(OUT / f"{name}.jpg")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
