#!/usr/bin/env python3
"""Submit sitemap.xml to Google Search Console after a deploy.

Usage (CI):
    GSC_SERVICE_ACCOUNT='<service account JSON>' python3 _design/submit_sitemap.py

Options:
    --wait        poll the live site until the deployed sitemap.xml matches
                  the one in the repo (GitHub Pages deploys asynchronously)
    --dry-run     authenticate and print what would be submitted, submit nothing

Setup (once):
    1. Google Cloud: enable the "Google Search Console API", create a service
       account, download its JSON key.
    2. Search Console -> Settings -> Users and permissions: add the service
       account's e-mail with "Full" permission (if the submit returns 403,
       make it an Owner via "Manage property owners").
    3. GitHub repo -> Settings -> Secrets -> Actions: add the JSON as
       GSC_SERVICE_ACCOUNT.

If the secret is not set the script prints a notice and exits 0, so CI stays
green until setup is done.

Why sitemaps.submit and not the Indexing API: the Indexing API is officially
limited to JobPosting / BroadcastEvent pages, and the old /ping endpoint was
retired in 2023. Resubmitting the sitemap is the supported way to tell Google
"something changed".
"""

import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import quote

SITE = "https://anvilarth.github.io/"
SITEMAP = SITE + "sitemap.xml"
ROOT = Path(__file__).resolve().parent.parent
SCOPE = "https://www.googleapis.com/auth/webmasters"
API = "https://www.googleapis.com/webmasters/v3/sites/{site}/sitemaps/{feed}"


def wait_for_deploy(timeout_s: int = 600, step_s: int = 20) -> bool:
    """Poll the live sitemap until it matches the repo copy."""
    expected = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    deadline = time.time() + timeout_s
    while True:
        try:
            req = urllib.request.Request(
                f"{SITEMAP}?nocache={int(time.time())}",
                headers={"Cache-Control": "no-cache"},
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                live = r.read().decode("utf-8")
            if live == expected:
                print("live sitemap.xml matches the repo")
                return True
            print("live sitemap.xml differs from repo, waiting for Pages deploy...")
        except Exception as exc:  # network hiccup: keep polling
            print(f"fetch failed ({exc}), retrying...")
        if time.time() >= deadline:
            print("::warning::Pages deploy not visible after "
                  f"{timeout_s}s; submitting anyway")
            return False
        time.sleep(step_s)


def main() -> int:
    raw = os.environ.get("GSC_SERVICE_ACCOUNT", "").strip()
    if not raw:
        print("::notice::GSC_SERVICE_ACCOUNT is not set; skipping sitemap submit")
        return 0

    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        print("::error::pip install google-auth requests", file=sys.stderr)
        return 1

    info = json.loads(raw)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=[SCOPE])
    session = AuthorizedSession(creds)

    if "--wait" in sys.argv:
        wait_for_deploy()

    url = API.format(site=quote(SITE, safe=""), feed=quote(SITEMAP, safe=""))
    print(f"submitting {SITEMAP} as {info.get('client_email')}")
    if "--dry-run" in sys.argv:
        print("dry run: nothing submitted")
        return 0

    resp = session.put(url, timeout=30)
    if resp.status_code in (200, 204):
        print("sitemap submitted")
    else:
        print(f"::error::submit failed: HTTP {resp.status_code}: {resp.text[:500]}",
              file=sys.stderr)
        if resp.status_code == 403:
            print("::error::give the service account Full (or Owner) access "
                  f"to {SITE} in Search Console", file=sys.stderr)
        return 1

    # Read back the status Google has for the sitemap (best effort).
    info_resp = session.get(url, timeout=30)
    if info_resp.ok:
        d = info_resp.json()
        print(json.dumps({k: d.get(k) for k in (
            "path", "lastSubmitted", "lastDownloaded", "isPending",
            "errors", "warnings")}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
