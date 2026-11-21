#!/usr/bin/env python3
"""Project covers: one flat editorial illustration series, same style for every project.

Each cover is generated as a 1536x1024 (3:2) image from STYLE + the project's subject
(the project's idea as a picture, never text or logos) and written uncropped to
static/img/projects/<name>.jpg at 1536x1024; an image of another ratio is padded with
the paper colour to 3:2. Pages show them with object-fit: contain on the same paper tone.

Usage: python3 templates/project-covers.py <dir with <name>.png files>
Needs Pillow (not a build dependency): uv run --with pillow python3 ...
"""
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "static/img/projects"
W, H = 1536, 1024
PAPER = (243, 237, 228)  # #f3ede4

STYLE = (
    "Editorial flat illustration for a machine-learning researcher's portfolio, one series. Wide 16:10 "
    'landscape composition, generous empty space, one clear central idea readable at thumbnail size. Warm'
    ' off-white paper background (#f3ede4) with subtle riso print grain; limited palette: rust red '
    '(#b5452b), deep ink brown-black (#1f1a17), warm sand (#d9c7ad), muted teal (#3f6f6a), soft peach '
    '(#f0c7a8). Simple geometric shapes, soft shadows, clean lines, calm and elegant like a Stripe Press '
    'or New Yorker spot illustration. Absolutely no text, letters, numbers, logos, UI or watermarks; no '
    "people's faces."
)

SUBJECTS = {
    'krea3': (
        'Idea: an image editor keeps one product consistent while changing the scene. The same small rust-red perfume bottle appears identical in three side-by-side arched frames, each frame a different setting: sunny beach, night city, minimal studio.'
    ),
    'krea2': (
        'Idea: a text-to-image model trained from scratch that can follow many visual styles. One identical simple horse silhouette repeated in a row of five tiles, each tile rendered in a distinct style: ink sketch, oil paint, flat paper cutout, glossy 3D, halftone print.'
    ),
    'calculator': (
        'Idea: estimating when video generation becomes real-time. A horizontal strip of film frames flowing from the left into a large round stopwatch on the right whose hand sits exactly at a marked threshold; small stacked blocks under the strip suggest compute.'
    ),
    'flux': (
        'Idea: small style adapters plugged into one big image model. A large ink-dark rounded block in the center with several small colored cartridges slotting into it, and from it a fan of the same landscape image emerging in different styles.'
    ),
    'esqa': (
        'Idea: a language model answering questions about long event sequences like transactions and logs. A long horizontal timeline of small dots, receipts and tick marks of varied colors flowing into a single rounded speech bubble that contains a small bright rust circle as the answer.'
    ),
    'kandinsky': (
        'Idea: a family of text-to-image and text-to-video models. A Bauhaus-inspired composition of circles, triangles and lines that on the right breaks into a sequence of film frames, the shapes moving slightly from frame to frame.'
    ),
    'taskdiscovery': (
        'Idea: discovering ways to split data on which neural networks generalize and agree. A grid of small rounded image tiles (animals and vehicles as simple icons) divided into two groups by one smooth curved boundary line, the two sides tinted teal and rust.'
    ),
    'baselines': (
        'Idea: control baselines for evaluating transfer learning, a lower bound and an upper bound. Two horizontal reference lines, a dashed floor and a solid ceiling, with a descending curve of dots between them and a small brass level instrument resting on the floor line.'
    ),
    'course': (
        'Idea: a deep learning course taught to students. A dark green school chalkboard in a wooden frame showing a simple chalk-drawn neural network of circles and connecting lines, a piece of chalk and a few stacked books beside it.'
    ),
    'linesearch': (
        'Idea: fast step-size line search for multi-task learning. A smooth rolling landscape with a valley; a dotted path of steps descending into the valley, each step shorter than the last, ending in a rust dot at the lowest point, a compass divider measuring one step.'
    ),
}


def main(src):
    from PIL import Image
    for name in SUBJECTS:
        im = Image.open(Path(src) / f"{name}.png").convert("RGB")
        im.thumbnail((W, H), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), PAPER)
        canvas.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
        canvas.save(OUT / f"{name}.jpg", quality=82, optimize=True, progressive=True)
        print(OUT / f"{name}.jpg")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
