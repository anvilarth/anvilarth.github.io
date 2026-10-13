#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, Seznam, Naver...) about pages changed in a deploy.

Usage (CI):
    python3 _design/indexnow.py --before <sha> --after HEAD --wait
    python3 _design/indexnow.py --all                 # every page in the sitemap

Options:
    --before/--after  commits to compare sitemap.xml between; sends pages whose
                      <lastmod> changed, plus pages new in the sitemap
    --all             send every page listed in sitemap.xml
    --wait            poll the live site until the key file is served
                      (GitHub Pages deploys asynchronously)
    --dry-run         print what would be sent, send nothing

How it works: the key is not a secret. IndexNow proves site ownership by
fetching https://anvilarth.github.io/<key>.txt and checking that it contains
the key, so the key file lives in the repo root. One request to
api.indexnow.org is shared with every participating search engine.

Google does not use IndexNow; submit_sitemap.py covers Google.
"""

import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "_design"))
from gen_sitemap import BASE  # noqa: E402
import xml.etree.ElementTree as ET  # noqa: E402
import os  # noqa: E402

HOST = "anvilarth.github.io"
ENDPOINT = "https://api.indexnow.org/indexnow"
ZERO_SHA = "0" * 40


def find_key() -> str:
    for path in ROOT.glob("*.txt"):
        if re.fullmatch(r"[0-9a-f]{32}", path.stem):
            if path.read_text(encoding="utf-8").strip() == path.stem:
                return path.stem
    raise SystemExit("::error::no IndexNow key file (<32 hex>.txt) in the repo root")


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
    return list(sitemap_entries((ROOT / "sitemap.xml").read_text(encoding="utf-8")))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout


def changed_urls(before: str, after: str) -> list[str]:
    """Pages whose <lastmod> changed between the two sitemaps, plus pages new
    in the sitemap. gen_sitemap.py keeps lastmod honest (articles use their
    JSON-LD dateModified, so a template-only rebuild changes nothing), and
    IndexNow follows it, so the engines hear the same story as the sitemap."""
    new = sitemap_entries(git("show", f"{after}:sitemap.xml"))
    try:
        old = sitemap_entries(git("show", f"{before}:sitemap.xml"))
    except (subprocess.CalledProcessError, ET.ParseError):
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
    before, after = arg("--before"), arg("--after")

    if "--all" in sys.argv or not before or before == ZERO_SHA or not after:
        urls = all_urls()
    else:
        try:
            urls = changed_urls(before, after)
        except subprocess.CalledProcessError:
            print("::notice::commit range not available, sending every page")
            urls = all_urls()

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
