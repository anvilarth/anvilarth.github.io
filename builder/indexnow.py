#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, Seznam, Naver...) about pages changed in a deploy.

Usage (CI, after `builder build`):
    uv run builder indexnow --previous live-sitemap.xml --wait
    uv run builder indexnow --all                     # every page in the sitemap

Options:
    --previous FILE   the sitemap that was live before this deploy; sends pages
                      whose <lastmod> changed, plus pages new in the sitemap
    --all             send every page listed in sitemap.xml
    --wait            poll the live site until the key file is served
                      (GitHub Pages deploys asynchronously)
    --dry-run         print what would be sent, send nothing

How it works: the key is not a secret. IndexNow proves site ownership by
fetching https://anvilarth.github.io/<key>.txt and checking that it contains
the key, so the key file is published at the site root. One request to
api.indexnow.org is shared with every participating search engine.

Google does not use IndexNow; submit_sitemap.py covers Google.
"""

import json
import re
import sys
import time
import urllib.error
import urllib.request
import os
from pathlib import Path
import xml.etree.ElementTree as ET

from .paths import BASE, DIST

HOST = "anvilarth.github.io"
ENDPOINT = "https://api.indexnow.org/indexnow"


def find_key() -> str:
    for path in DIST.glob("*.txt"):
        if re.fullmatch(r"[0-9a-f]{32}", path.stem):
            if path.read_text(encoding="utf-8").strip() == path.stem:
                return path.stem
    raise SystemExit("::error::no IndexNow key file (<32 hex>.txt) in dist/")


def arg(name: str) -> str | None:
    if name in sys.argv:
        i = sys.argv.index(name)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return None


NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def sitemap_entries(xml_text: str) -> dict[str, str]:
    """{loc: lastmod} of a sitemap, in document order. The sitemap is the
    single source of truth: IndexNow sends exactly what it says changed."""
    root = ET.fromstring(xml_text)
    out: dict[str, str] = {}
    for url in root.findall("sm:url", NS):
        loc = (url.findtext("sm:loc", "", NS) or "").strip()
        if loc:
            out[loc] = (url.findtext("sm:lastmod", "", NS) or "").strip()
    return out


def all_urls() -> list[str]:
    return list(sitemap_entries((DIST / "sitemap.xml").read_text(encoding="utf-8")))


def changed_urls(previous: Path) -> list[str]:
    """Pages whose <lastmod> changed against the previously live sitemap, plus
    pages new in it. gen_sitemap.py keeps lastmod honest (articles use their
    JSON-LD dateModified, so a template-only rebuild changes nothing), and
    IndexNow follows it, so the engines hear the same story as the sitemap."""
    new = sitemap_entries((DIST / "sitemap.xml").read_text(encoding="utf-8"))
    try:
        old = sitemap_entries(previous.read_text(encoding="utf-8"))
    except (OSError, ET.ParseError):
        old = {}
    return [loc for loc, lastmod in new.items() if old.get(loc) != lastmod]


def summary(lines: list[str]) -> None:
    """Append to the GitHub Actions job summary (no-op outside CI)."""
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")


def wait_for_key(key: str, timeout_s: int = 600, step_s: int = 20) -> None:
    url = f"{BASE}{key}.txt"
    deadline = time.time() + timeout_s
    while True:
        try:
            req = urllib.request.Request(f"{url}?nocache={int(time.time())}",
                                         headers={"Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.read().decode("utf-8").strip() == key:
                    print("key file is live")
                    return
        except Exception as exc:  # not deployed yet / network hiccup
            print(f"key file not live yet ({exc}), waiting...")
        if time.time() >= deadline:
            print(f"::warning::key file not live after {timeout_s}s; sending anyway")
            return
        time.sleep(step_s)


def main() -> int:
    key = find_key()
    previous = arg("--previous")
    if "--all" in sys.argv or not previous:
        urls = all_urls()
    else:
        urls = changed_urls(Path(previous))

    if not urls:
        print("no published pages changed; nothing to send")
        summary(["### IndexNow", "", "No published pages changed in this push; nothing sent."])
        return 0

    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"{BASE}{key}.txt",
        "urlList": urls,
    }
    print(json.dumps(payload, indent=1))
    if "--dry-run" in sys.argv:
        print("dry run: nothing sent")
        return 0

    if "--wait" in sys.argv:
        wait_for_key(key)

    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            status = r.status
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:500]
        # 422 = URLs/key mismatch, 403 = key file not reachable, 429 = too often.
        print(f"::error::IndexNow HTTP {exc.code}: {body}", file=sys.stderr)
        summary(["### IndexNow ❌", "", f"HTTP {exc.code}: `{body[:200]}`"])
        return 1

    print(f"IndexNow accepted {len(urls)} url(s): HTTP {status}")
    summary(["### IndexNow ✅", "",
             f"Sent {len(urls)} URL(s) to Bing, Yandex, Seznam and other "
             f"IndexNow engines (HTTP {status}):", ""]
            + [f"- {u}" for u in urls])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
