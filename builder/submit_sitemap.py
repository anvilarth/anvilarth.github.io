"""Submit XML and text sitemaps to Google Search Console after a deploy.

Usage (CI):
    GSC_SERVICE_ACCOUNT='<service account JSON>' uv run builder submit-sitemap

Options:
    --wait        poll the live site until both deployed sitemaps match the
                  build (GitHub Pages deploys asynchronously)
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
from urllib.parse import quote

SITE = "https://anvilarth.github.io/"
SITEMAPS = ("sitemap.xml", "sitemap.txt")
from .paths import DIST
SCOPE = "https://www.googleapis.com/auth/webmasters"
API = "https://www.googleapis.com/webmasters/v3/sites/{site}/sitemaps/{feed}"


def wait_for_deploy(timeout_s: int = 600, step_s: int = 20) -> bool:
    """Poll the live sitemap until it matches the repo copy."""
    expected = {name: (DIST / name).read_text(encoding="utf-8") for name in SITEMAPS}
    deadline = time.time() + timeout_s
    while True:
        try:
            matches = True
            for name, content in expected.items():
                req = urllib.request.Request(
                    f"{SITE}{name}?nocache={int(time.time())}",
                    headers={"Cache-Control": "no-cache"},
                )
                with urllib.request.urlopen(req, timeout=30) as r:
                    matches = (r.read().decode("utf-8") == content) and matches
            if matches:
                print("live XML and text sitemaps match the build")
                return True
            print("live sitemaps differ from the build, waiting for Pages deploy...")
        except Exception as exc:  # network hiccup: keep polling
            print(f"fetch failed ({exc}), retrying...")
        if time.time() >= deadline:
            print("::error::Pages deploy not visible after "
                  f"{timeout_s}s; no sitemaps submitted")
            return False
        time.sleep(step_s)


def main() -> int:
    raw = os.environ.get("GSC_SERVICE_ACCOUNT", "").strip()
    if not raw:
        # A warning, not a notice: a green job that never reaches Google is
        # easy to miss. Still exit 0 so the deploy is not blocked.
        print("::warning::GSC_SERVICE_ACCOUNT is not set; sitemap NOT submitted "
              "to Google (see the setup steps at the top of submit_sitemap.py)")
        summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary_path:
            with open(summary_path, "a", encoding="utf-8") as fh:
                fh.write("### Google sitemap submit ⚠️\n\n"
                         "Skipped: the `GSC_SERVICE_ACCOUNT` secret is not set, "
                         "so Google only sees changes on its own recrawl. "
                         "Setup steps: `builder/submit_sitemap.py`.\n")
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

    if "--wait" in sys.argv and not wait_for_deploy():
        return 1

    if "--dry-run" in sys.argv:
        print(f"dry run: would submit {', '.join(SITE + name for name in SITEMAPS)}")
        return 0

    summary = []
    failed = False
    for name in SITEMAPS:
        sitemap = SITE + name
        url = API.format(site=quote(SITE, safe=""), feed=quote(sitemap, safe=""))
        resp = session.put(url, timeout=30)
        if resp.status_code not in (200, 204):
            print(f"::error::{name} submit failed: HTTP {resp.status_code}", file=sys.stderr)
            summary.append(f"- `{name}`: submission failed (HTTP {resp.status_code}).")
            failed = True
            continue
        print(f"{name}: submission accepted; this does not confirm fetching or indexing")
        info_resp = session.get(url, timeout=30)
        if not info_resp.ok:
            print(f"::warning::{name}: status unavailable (HTTP {info_resp.status_code})")
            summary.append(f"- `{name}`: submitted; processing status unavailable.")
            continue
        d = info_resp.json()
        print(json.dumps({k: d.get(k) for k in (
            "path", "lastSubmitted", "lastDownloaded", "isPending",
            "errors", "warnings")}, indent=1))
        if int(d.get('errors', 0)):
            state = f"Google reports {d['errors']} errors"
            failed = True
            print(f"::error::{name}: {state}")
        elif d.get('isPending') or not d.get('lastDownloaded'):
            state = 'awaiting Google processing; fetch is NOT confirmed'
            print(f"::warning::{name}: {state}")
        else:
            state = f"last downloaded {d['lastDownloaded']}; page indexing is separate"
        summary.append(f"- `{name}`: {state}.")
    summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_path:
        with open(summary_path, 'a', encoding='utf-8') as fh:
            fh.write('### Google sitemap processing\n\n' + '\n'.join(summary) + '\n')
    if failed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
