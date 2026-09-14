#!/usr/bin/env python3
"""Lighthouse budgets for anvilarth.github.io, mobile and desktop.

Serves the working tree over HTTP, runs Lighthouse against every page in
sitemap.xml and compares the results with the budgets below.

Two tiers of budget, because not every metric is reproducible on shared CI
hardware:

  hard  CLS, accessibility, SEO - geometry and markup, identical on any
        machine. A violation fails the build.
  soft  performance score, LCP, TBT - depend on the runner's CPU. A violation
        is reported as a warning only.

Usage:
  python3 _design/perf_check.py                        # both form factors
  python3 _design/perf_check.py --form-factor mobile
  python3 _design/perf_check.py --runs 5 --reports out/

Needs Node (for `npx lighthouse`) and a Chrome/Chromium binary.
"""

from __future__ import annotations

import argparse
import functools
import gzip
import json
import os
import statistics
import subprocess
import sys
import tempfile
import threading
import xml.etree.ElementTree as ET
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

BASE = "https://anvilarth.github.io/"
ROOT = Path(__file__).resolve().parent.parent
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
LIGHTHOUSE = "lighthouse@12"

# metric key -> (label, unit, comparison, mobile budget, desktop budget)
# comparison "<=" means lower is better.
HARD = {
    "cumulative-layout-shift": ("CLS", "", "<=", 0.10, 0.10),
    "_score_accessibility": ("a11y", "", ">=", 100, 100),
    "_score_seo": ("SEO", "", ">=", 95, 95),
}
SOFT = {
    "_score_performance": ("perf", "", ">=", 90, 95),
    "largest-contentful-paint": ("LCP", "ms", "<=", 2500, 1500),
    "total-blocking-time": ("TBT", "ms", "<=", 200, 100),
}
BUDGETS = {**HARD, **SOFT}


def pages_from_sitemap() -> list[str]:
    """Every published HTML page, as a root-relative URL path.

    The sitemap also lists the Markdown mirrors of the articles; Lighthouse
    refuses anything that is not served as HTML, so they are skipped.
    """
    tree = ET.parse(ROOT / "sitemap.xml")
    out = []
    for url in tree.getroot().findall("sm:url", NS):
        loc = (url.findtext("sm:loc", namespaces=NS) or "").strip()
        if not loc.startswith(BASE):
            continue
        path = "/" + unquote(loc[len(BASE):])
        if path.endswith("/") or path.endswith(".html"):
            out.append(path)
    return out


# GitHub Pages serves text assets gzipped. Without this the local server looks
# ~95 KiB heavier per article and every run trips the text-compression audit.
GZIP_TYPES = ("text/", "application/javascript", "application/json",
              "application/xml", "image/svg+xml")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args) -> None:  # keep the run output readable
        pass

    def do_GET(self) -> None:
        path = Path(self.translate_path(self.path))
        if path.is_dir():
            path = path / "index.html"
        ctype = self.guess_type(str(path))
        if (not path.is_file()
                or not ctype.startswith(GZIP_TYPES)
                or "gzip" not in self.headers.get("Accept-Encoding", "")):
            super().do_GET()
            return
        body = gzip.compress(path.read_bytes(), 6)
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def serve(root: Path) -> tuple[ThreadingHTTPServer, int]:
    handler = functools.partial(QuietHandler, directory=str(root))
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def run_lighthouse(url: str, form_factor: str, out_path: Path, profile: Path) -> dict:
    # Always a dedicated, throwaway browser profile - never the developer's own.
    flags = ("--headless=new --no-sandbox --disable-dev-shm-usage "
             f"--user-data-dir={profile}")
    cmd = [
        "npx", "--yes", LIGHTHOUSE, url,
        "--quiet",
        "--only-categories=performance,accessibility,seo",
        "--output=json", f"--output-path={out_path}",
        f"--chrome-flags={flags}",
    ]
    if form_factor == "mobile":
        cmd += ["--form-factor=mobile", "--screenEmulation.mobile"]
    else:
        cmd += ["--preset=desktop"]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not out_path.exists():
        sys.stderr.write(proc.stderr[-4000:] + "\n")
        raise SystemExit(f"lighthouse failed for {url} ({form_factor})")
    return json.loads(out_path.read_text(encoding="utf-8"))


def collect(report: dict) -> dict[str, float]:
    """Pull every budgeted metric out of one Lighthouse report."""
    values: dict[str, float] = {}
    for key in BUDGETS:
        if key.startswith("_score_"):
            cat = report["categories"].get(key[len("_score_"):])
            values[key] = round(cat["score"] * 100) if cat else float("nan")
        else:
            values[key] = report["audits"][key]["numericValue"]
    return values


def culprits(report: dict) -> list[str]:
    """Elements Lighthouse blames for the layout shifts, for the summary."""
    items = report["audits"].get("layout-shifts", {}).get("details", {}).get("items", [])
    return [
        f"{item['score']:.3f} {item['node'].get('selector', '?')}"
        for item in items if item.get("score", 0) >= 0.005
    ]


def fmt(key: str, value: float) -> str:
    label, unit, *_ = BUDGETS[key]
    if key == "cumulative-layout-shift":
        return f"{value:.3f}"
    if unit == "ms":
        return f"{value / 1000:.2f}s"
    return f"{value:.0f}"


def violates(key: str, value: float, form_factor: str) -> bool:
    _, _, cmp_op, mobile, desktop = BUDGETS[key]
    budget = mobile if form_factor == "mobile" else desktop
    return value > budget if cmp_op == "<=" else value < budget


def budget_of(key: str, form_factor: str) -> float:
    _, _, _, mobile, desktop = BUDGETS[key]
    return mobile if form_factor == "mobile" else desktop


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--form-factor", choices=["mobile", "desktop", "both"], default="both")
    ap.add_argument("--runs", type=int, default=3,
                    help="Lighthouse runs per page; the median is scored")
    ap.add_argument("--pages", nargs="*", help="override the sitemap page list")
    ap.add_argument("--reports", type=Path,
                    help="directory to keep the raw JSON reports in")
    ap.add_argument("--chrome-profile", type=Path,
                    help="dedicated --user-data-dir for the headless browser "
                         "(default: a throwaway one per page); never point this "
                         "at a real browser profile")
    args = ap.parse_args()

    pages = args.pages or pages_from_sitemap()
    factors = ["mobile", "desktop"] if args.form_factor == "both" else [args.form_factor]
    reports_dir = args.reports
    if reports_dir:
        reports_dir.mkdir(parents=True, exist_ok=True)

    httpd, port = serve(ROOT)
    lines: list[str] = []
    failures: list[str] = []
    warnings: list[str] = []

    try:
        for factor in factors:
            lines.append(f"\n### {factor}\n")
            header = ["page"] + [BUDGETS[k][0] for k in BUDGETS]
            lines.append("| " + " | ".join(header) + " |")
            lines.append("|" + "---|" * len(header))
            budget_row = ["budget"] + [
                f"{'≤' if BUDGETS[k][2] == '<=' else '≥'} "
                f"{fmt(k, budget_of(k, factor))}"
                for k in BUDGETS
            ]
            lines.append("| " + " | ".join(budget_row) + " |")

            for page in pages:
                url = f"http://127.0.0.1:{port}{page}"
                runs = []
                last_report = None
                with tempfile.TemporaryDirectory() as tmp:
                    profile = args.chrome_profile or Path(tmp) / "chrome-profile"
                    for i in range(args.runs):
                        out = Path(tmp) / f"lh-{i}.json"
                        last_report = run_lighthouse(url, factor, out, profile)
                        runs.append(collect(last_report))
                        if reports_dir and i == 0:
                            name = (page.strip("/") or "index").replace("/", "_")
                            (reports_dir / f"{name}.{factor}.json").write_text(
                                json.dumps(last_report), encoding="utf-8")

                median = {k: statistics.median(r[k] for r in runs) for k in BUDGETS}
                cells = []
                for key, value in median.items():
                    cell = fmt(key, value)
                    if violates(key, value, factor):
                        cell = f"**{cell}** ⚠️"
                        target = (f"{page} [{factor}] {BUDGETS[key][0]}={fmt(key, value)} "
                                  f"(budget {'≤' if BUDGETS[key][2] == '<=' else '≥'} "
                                  f"{fmt(key, budget_of(key, factor))})")
                        (failures if key in HARD else warnings).append(target)
                    cells.append(cell)
                lines.append("| " + " | ".join([page] + cells) + " |")

                shifts = culprits(last_report) if last_report else []
                if shifts and median["cumulative-layout-shift"] >= 0.005:
                    lines.append(f"| ↳ shifts | {'<br>'.join(shifts)} |"
                                 + " |" * (len(header) - 2))
    finally:
        httpd.shutdown()

    body = "\n".join(lines)
    print(body)

    if warnings:
        print("\nSoft budget warnings (runner-dependent, not fatal):")
        for w in warnings:
            print(f"  - {w}")
    if failures:
        print("\nHard budget violations:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(f"## Lighthouse ({args.runs} runs, median)\n{body}\n")
            if warnings:
                fh.write("\n**Soft warnings:** " + "; ".join(warnings) + "\n")
            if failures:
                fh.write("\n**Failed:** " + "; ".join(failures) + "\n")

    if failures:
        print(f"\n{len(failures)} hard budget violation(s)", file=sys.stderr)
        return 1
    print(f"\nall budgets met ({len(warnings)} soft warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
