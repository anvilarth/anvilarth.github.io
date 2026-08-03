#!/usr/bin/env python3
"""Generate uniform project covers for the site.

Editorial layout, same for every project — only the text differs:
top meta row (year · org / category tag), big serif title with one
italic amber accent word, bottom hairline with the project domain.
Renders an HTML template with headless Chrome into img/projects/<name>.jpg.

Usage: python3 img/projects/make_covers.py
Original screenshots are backed up to img/projects/_screenshots/ on first run.
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1280, 720

PROJECTS = [
    # (output name, label, title_html, tag, domain)
    ("krea2",         "2026 · Krea",            "<em>Krea</em> 2",                    "foundation model",  "krea.ai"),
    ("calculator",    "2026 · Interactive tool", "Realtime <em>Video</em> Calculator", "first-principles",  "anvilarth.github.io"),
    ("flux",          "2024 · XLabs",            "XLabs <em>FLUX</em> LoRAs",          "style adapters",    "huggingface.co"),
    ("esqa",          "2024 · Kandinsky Labs",   "<em>ESQA</em>",                      "benchmark",         "github.com"),
    ("kandinsky",     "2023–24 · Kandinsky Labs", "Kandinsky <em>3 / 4</em>",          "t2i & t2v",         "ai-forever.github.io"),
    ("taskdiscovery", "2022 · NeurIPS · EPFL",   "Task <em>Discovery</em>",            "paper",             "taskdiscovery.epfl.ch"),
    ("baselines",     "2022 · EPFL",             "Simple Control <em>Baselines</em>",  "paper",             "transfer-controls.epfl.ch"),
    ("course",        "2022 · Teaching",         "Deep Learning <em>Course</em>",      "course",            "github.com"),
    ("linesearch",    "2021 · Paper",            "Fast <em>Line Search</em> for MTL",  "paper",             "arxiv.org"),
]

TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;overflow:hidden;position:relative;background:#0c0a09}}
body::before{{content:'';position:absolute;inset:0;background:
  radial-gradient(900px 500px at 85% 0%,rgb(245 158 11/.08),transparent 60%),
  radial-gradient(700px 500px at 0% 100%,rgb(231 229 228/.03),transparent 55%)}}
body::after{{content:'';position:absolute;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.05'/%3E%3C/svg%3E")}}
.frame{{position:absolute;inset:26px;border:1px solid #292524}}
.stack{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 96px}}
.label{{font-family:'JetBrains Mono',monospace;font-weight:500;font-size:19px;letter-spacing:.2em;text-transform:uppercase;color:#f59e0b;margin-bottom:34px}}
.rule{{width:48px;height:1px;background:#292524;margin-bottom:34px}}
.title{{font-family:'Playfair Display',Georgia,serif;font-weight:600;font-size:80px;line-height:1.08;letter-spacing:-.02em;color:#e7e5e4}}
.title em{{font-style:normal;font-weight:500;color:#e7e5e4}}
.foot{{position:absolute;left:64px;right:64px;bottom:52px;text-align:center;
  font-family:'JetBrains Mono',monospace;font-weight:400;font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:#78716c}}
.foot::before{{content:'';position:absolute;left:0;right:0;top:-18px;height:1px;background:#292524}}
</style></head>
<body>
<div class="frame"></div>
<div class="stack">
  <div class="label">{label}</div>
  <div class="rule"></div>
  <div class="title">{title}</div>
</div>
<div class="foot">{tag} · {domain}</div>
</body></html>
"""


def main():
    backup = HERE / "_screenshots"
    backup.mkdir(exist_ok=True)
    tmp = HERE / "_cover_tmp.html"

    for name, label, title, tag, domain in PROJECTS:
        out = HERE / f"{name}.jpg"
        if out.exists() and not (backup / f"{name}.jpg").exists():
            shutil.copy2(out, backup / f"{name}.jpg")

        tmp.write_text(TEMPLATE.format(w=W, h=H, label=label, title=title,
                                       tag=tag, domain=domain))
        url = "file://" + str(tmp)
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             f"--window-size={W},{H}", "--virtual-time-budget=6000",
             f"--screenshot={out}", url],
            check=True, capture_output=True)
        print(f"ok {out.name}")

    tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
