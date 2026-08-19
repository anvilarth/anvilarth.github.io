#!/usr/bin/env python3
"""Regenerate sitemap.xml with lastmod taken from git commit dates.

Usage:
    python3 _design/gen_sitemap.py           # write sitemap.xml
    python3 _design/gen_sitemap.py --check   # exit 1 if sitemap.xml is stale

lastmod is the author date of the last commit that touched the file,
in W3C / ISO-8601 form with timezone offset. Falls back to the file's
mtime for files not yet committed.
"""

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://anvilarth.github.io/"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "sitemap.xml"

# (path relative to repo root, url path, priority)
# url path "" means the site root.
PAGES = [
    ("index.html",                     "",                              "1.0"),
    ("autoresearch.html",              "autoresearch.html",             "0.9"),
    ("gpu-story.html",                 "gpu-story.html",                "0.9"),
    ("blog.html",                      "blog.html",                     "0.8"),
    ("projects.html",                  "projects.html",                 "0.8"),
    ("realtime-video-calculator.html", "realtime-video-calculator.html","0.7"),
    ("about.md",                       "about.md",                      "0.6"),
    ("autoresearch.md",                "autoresearch.md",               "0.6"),
    ("autoresearch.en.md",             "autoresearch.en.md",            "0.6"),
    ("gpu-story.md",                   "gpu-story.md",                  "0.6"),
    ("gpu-story.en.md",                "gpu-story.en.md",               "0.6"),
    ("llms.txt",                       "llms.txt",                      "0.5"),
]


def git_lastmod(rel_path: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", rel_path],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        return out or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def mtime_lastmod(path: Path) -> str:
    ts = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return ts.astimezone().replace(microsecond=0).isoformat()


def lastmod_for(rel_path: str) -> str | None:
    path = ROOT / rel_path
    if not path.exists():
        print(f"  ! missing file, skipped: {rel_path}", file=sys.stderr)
        return None
    return git_lastmod(rel_path) or mtime_lastmod(path)


def build() -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for rel_path, url_path, priority in PAGES:
        lastmod = lastmod_for(rel_path)
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


def main() -> int:
    new = build()
    check = "--check" in sys.argv
    old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    if new == old:
        print("sitemap.xml is up to date")
        return 0
    if check:
        print("sitemap.xml is STALE - run: python3 _design/gen_sitemap.py", file=sys.stderr)
        return 1
    OUT.write_text(new, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(PAGES)} urls)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
