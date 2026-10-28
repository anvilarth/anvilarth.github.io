"""Write dist/sitemap.xml with lastmod taken from the source files' history.

lastmod is the page's JSON-LD dateModified when it declares one (articles:
a template-only rebuild must not look like a content update). Otherwise it
is the author date of the last commit that changed the page's source file,
following renames so that moving a file does not count as an update, in
W3C / ISO-8601 form with timezone offset, falling back to the file's mtime
for files not yet committed.
"""

import re
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from .paths import BASE, DIST, ROOT

OUT = DIST / "sitemap.xml"

# (path relative to dist/, url path, priority)
# url path "" means the site root.
#
# HTML pages only. The .md mirrors and llms.txt are for LLM crawlers
# (advertised in robots.txt / llms.txt); listing them here makes Google
# treat them as duplicate copies of the articles.
BASE_PAGES = [
    ("rl-for-diffusion-part-2.html", "rl-for-diffusion-part-2.html", "0.9"),
    ("rl-for-diffusion-part-1.html", "rl-for-diffusion-part-1.html", "0.9"),
    ("preference-optimization.html", "preference-optimization.html", "0.9"),
    ("index.html",                     "",                              "1.0"),
    ("autoresearch.html",              "autoresearch.html",             "0.9"),
    ("gpu-story.html",                 "gpu-story.html",                "0.9"),
    ("blog.html",                      "blog.html",                     "0.8"),
    ("projects.html",                  "projects.html",                 "0.8"),
    ("realtime-video-calculator.html", "realtime-video-calculator.html","0.7"),
]
LOCALES = json.loads((ROOT / 'builder/locales.json').read_text())
PAGES = BASE_PAGES + [(slug + '.ru.html', slug + '.ru.html', '0.9') for slug in LOCALES]


def git_lastmod(source: Path) -> str | None:
    # --follow keeps history across moves; pure renames (R100) are not edits.
    try:
        log = subprocess.run(
            ["git", "log", "--follow", "--name-status", "--format=%x00%aI", "--",
             source.relative_to(ROOT).as_posix()],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return None
    for entry in log.split("\0")[1:]:
        date, _, status = entry.strip().partition("\n")
        if not status.strip().startswith("R100"):
            return date
    return None


def mtime_lastmod(path: Path) -> str:
    ts = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return ts.astimezone().replace(microsecond=0).isoformat()


def declared_lastmod(path: Path) -> str | None:
    match = re.search(r'"dateModified":\s*"([^"]+)"', path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def lastmod_for(rel_path: str, sources: dict[str, Path]) -> str | None:
    path = DIST / rel_path
    if not path.exists():
        print(f"  ! missing file, skipped: {rel_path}", file=sys.stderr)
        return None
    source = sources[rel_path.replace('.ru.html', '.html')]
    return declared_lastmod(path) or git_lastmod(source) or mtime_lastmod(source)


def build(sources: dict[str, Path]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for rel_path, url_path, priority in PAGES:
        lastmod = lastmod_for(rel_path, sources)
        if lastmod is None:
            continue
        loc = BASE + url_path
        lines.append(
            f"  <url><loc>{loc}</loc>"
            f"<lastmod>{lastmod}</lastmod>"
            f"<priority>{priority}</priority></url>"
        )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def write(sources: dict[str, Path]) -> None:
    OUT.write_text(build(sources), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(PAGES)} urls)")
