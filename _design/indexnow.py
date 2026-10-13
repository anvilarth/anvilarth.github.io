#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, Seznam, Naver...) about pages changed in a deploy.

Usage (CI):
    python3 _design/indexnow.py --before <sha> --after <sha> --wait
    python3 _design/indexnow.py --all                 # every page in the sitemap

Options:
    --before/--after  commit range of the push; only pages whose HTML (or
                      assets/<slug>/ files) changed in that range are sent
    --all             send every page from gen_sitemap.PAGES
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
from gen_sitemap import BASE, PAGES  # noqa: E402

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


def all_urls() -> list[str]:
    return [BASE + url_path for _, url_path, _ in PAGES]


def changed_urls(before: str, after: str) -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", before, after],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    changed = set(out)
    urls = []
    for rel_path, url_path, _ in PAGES:
        slug = rel_path.removesuffix(".html")
        if rel_path in changed or any(f.startswith(f"assets/{slug}/") for f in changed):
            urls.append(BASE + url_path)
    return urls


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
            print(f"IndexNow accepted {len(urls)} url(s): HTTP {r.status}")
            return 0
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:500]
        # 422 = URLs/key mismatch, 403 = key file not reachable, 429 = too often.
        print(f"::error::IndexNow HTTP {exc.code}: {body}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
