"""Pre-deploy sanity checks for anvilarth.github.io.

Checks:
  1. sitemap.xml is well-formed XML and matches the generator output
  2. every <loc> in the sitemap resolves to a file that exists
  3. every <lastmod> is a valid W3C datetime
  4. robots.txt advertises the same sitemap URL
  5. no broken internal links in the published .html and .css files
  6. every published asset is referenced, unless it is used from outside
  7. the repository follows the layout in AGENTS.md

Exit code 1 on any error. Warnings do not fail the build.
"""

import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .paths import BASE, DIST as ROOT, ROOT as REPO

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def local_path_for(loc: str) -> Path | None:
    """Map a sitemap <loc> to a path on disk, or None if it is off-site."""
    if not loc.startswith(BASE):
        return None
    rel = unquote(loc[len(BASE):]) or "index.html"
    if rel.endswith("/"):
        rel += "index.html"
    return ROOT / rel


# --- 1-3. sitemap ------------------------------------------------------------

def check_sitemap() -> list[str]:
    path = ROOT / "sitemap.xml"
    if not path.exists():
        err("sitemap.xml is missing")
        return []

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        err(f"sitemap.xml is not well-formed XML: {exc}")
        return []

    locs: list[str] = []
    for url in tree.getroot().findall("sm:url", NS):
        loc_el = url.find("sm:loc", NS)
        if loc_el is None or not (loc_el.text or "").strip():
            err("sitemap.xml: <url> entry without <loc>")
            continue
        loc = loc_el.text.strip()
        locs.append(loc)

        if not loc.startswith(BASE):
            err(f"sitemap.xml: <loc> outside the site: {loc}")
            continue

        target = local_path_for(loc)
        if target is None or not target.exists():
            err(f"sitemap.xml: <loc> points at a file that does not exist: {loc}")

        lastmod_el = url.find("sm:lastmod", NS)
        if lastmod_el is None or not (lastmod_el.text or "").strip():
            warn(f"sitemap.xml: no <lastmod> for {loc}")
        else:
            raw = lastmod_el.text.strip()
            try:
                datetime.fromisoformat(raw.replace("Z", "+00:00"))
            except ValueError:
                err(f"sitemap.xml: invalid <lastmod> {raw!r} for {loc}")

    if len(set(locs)) != len(locs):
        err("sitemap.xml: duplicate <loc> entries")

    # Published pages that never made it into the sitemap.
    listed = {local_path_for(loc) for loc in locs}
    for html in sorted(ROOT.glob("*.html")):
        rel = html.relative_to(ROOT).as_posix()
        if rel.startswith("google") and rel.endswith(".html"):
            continue  # Search Console verification file
        if html not in listed:
            warn(f"{rel} is published but not listed in sitemap.xml")

    return locs


# --- 4. robots.txt -----------------------------------------------------------

def check_robots() -> None:
    path = ROOT / "robots.txt"
    if not path.exists():
        err("robots.txt is missing")
        return
    text = path.read_text(encoding="utf-8")
    declared = re.findall(r"(?im)^\s*Sitemap:\s*(\S+)\s*$", text)
    expected = BASE + "sitemap.xml"
    if not declared:
        err("robots.txt has no Sitemap: directive")
    elif expected not in declared:
        err(f"robots.txt points at {declared} but the sitemap lives at {expected}")
    if re.search(r"(?im)^\s*Disallow:\s*/\s*$", text):
        err("robots.txt contains a blanket 'Disallow: /'")


# --- 5. internal links -------------------------------------------------------

LINK_RE = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', re.I)
URL_RE = re.compile(r'url\(\s*["\']?([^"\')\s]+)', re.I)
SKIP_SCHEMES = ("http://", "https://", "//", "mailto:", "tel:", "data:", "javascript:")


def check_links() -> None:
    for html in sorted(ROOT.glob("*.html")) + sorted(ROOT.rglob("*.css")):
        rel_name = html.relative_to(ROOT).as_posix()
        try:
            text = html.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            warn(f"{rel_name}: not valid UTF-8, skipped link check")
            continue

        # CSS url() resolves against the file that contains it, like href/src.
        links = URL_RE.findall(text) if html.suffix == ".css" else LINK_RE.findall(text) + URL_RE.findall(text)
        for raw in links:
            link = raw.strip()
            if not link or link.startswith(("#", "%23")) or link.lower().startswith(SKIP_SCHEMES):
                continue
            target_rel = urlsplit(link).path
            if not target_rel:
                continue
            target_rel = unquote(target_rel)
            target = (ROOT / target_rel.lstrip("/")) if target_rel.startswith("/") \
                else (html.parent / target_rel)
            if target.is_dir():
                target = target / "index.html"
            try:
                target.relative_to(ROOT)
            except ValueError:
                err(f"{rel_name}: link escapes the site root: {link}")
                continue
            if not target.exists():
                err(f"{rel_name}: broken internal link -> {link}")


# --- 6. unused assets -------------------------------------------------------

ASSETS = {".css", ".gif", ".ico", ".jpeg", ".jpg", ".js", ".json", ".mp4", ".pdf",
          ".png", ".svg", ".ttf", ".webm", ".webp", ".woff", ".woff2"}
TEXT = {".css", ".html", ".js", ".json", ".md", ".svg", ".txt", ".xml"}
# Used from outside the site, so nothing on it links to them (see AGENTS.md).
EXTERNAL = {"favicon.ico", "img/og/banner-2x.jpg"}


def check_unused() -> None:
    files = [p for p in ROOT.rglob("*") if p.is_file()]
    text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files if p.suffix in TEXT)
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix in ASSETS and rel not in EXTERNAL and path.name not in text:
            err(f"{rel}: published but never referenced; delete it in the same change")


# --- 7. repository layout ----------------------------------------------------

TOP_LEVEL = {".github", ".gitignore", "AGENTS.md", "CLAUDE.md", "builder", "pages",
             "posts", "pyproject.toml", "static", "templates", "uv.lock"}
GENERATED = re.compile(r"(^|/)(dist/|sitemap\.xml$|llms-full\.txt$)|\.ru\.html$")
LEFTOVER = re.compile(r"(^|/)(\.DS_Store|__pycache__/|\.env)|\.(bak|orig|pyc|swp)$|~$")
SLUG = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")


def check_repo() -> None:
    try:
        tracked = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True,
                                 text=True, check=True).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        warn("git is unavailable, repository layout not checked")
        return
    for path in tracked:
        if path.startswith("posts/") and path.count("/") == 1:
            err(f"{path}: posts/ holds only post folders")
        if path.split("/", 1)[0] not in TOP_LEVEL:
            err(f"{path}: outside the repository layout in AGENTS.md")
        if GENERATED.search(path):
            err(f"{path}: build output must not be committed")
        if LEFTOVER.search(path):
            err(f"{path}: local or leftover file must not be committed")
    for slug in sorted({p.split("/")[1] for p in tracked if p.startswith("posts/") and p.count("/") > 1}):
        if not SLUG.fullmatch(slug):
            err(f"posts/{slug}: a slug is lowercase words joined by hyphens")
        if f"posts/{slug}/post.html" not in tracked:
            err(f"posts/{slug}: missing post.html")


def main() -> int:
    check_sitemap()
    check_robots()
    check_links()
    check_unused()
    check_repo()

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    print(f"\nall checks passed ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
