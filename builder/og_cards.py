"""Render 1200×630 social cards for articles from their own metadata.

    uv run builder og [--drafts] [--out DIR] [--suffix S] [--profile DIR] [--chrome PATH] [slug ...]

The card is templates/og.html rendered by headless Chrome: title, lead (the
meta description), reading time, series part, author and site, in the
article's language. Output is og-<slug><suffix>.jpg in --out (default
static/img/og/). The profile directory is a throwaway Chrome user data dir.
"""
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlencode

from .paths import ROOT

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
MONTHS = {
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'ru': ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
}
WORDS = {
    'en': {'longread': 'Long-read', 'series': 'Series', 'part': 'Part', 'author': 'Andrei Filatov'},
    'ru': {'longread': 'Лонгрид', 'series': 'Серия', 'part': 'Часть', 'author': 'Андрей Филатов'},
}


def text(fragment):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', fragment))).strip()


def metadata(post: Path) -> dict:
    src = post.read_text()
    lang = re.search(r'<html\s[^>]*lang="(\w+)"', src)[1][:2]
    words = WORDS.get(lang, WORDS['en'])
    h1 = re.search(r'<h1\b[^>]*>(.*?)</h1>', src, re.S)[1]
    part = re.search(r'<span class="title-part">(.*?)</span>', h1, re.S)
    part_number = re.search(r'\d+', text(part[1])) if part else None
    title = text(re.sub(r'<span class="title-part">.*?</span>', '', h1, flags=re.S))
    lead = re.search(r'<meta name="description" content="([^"]*)"', src)
    meta = re.search(r'<p class="meta"[^>]*>(.*?)</p>', src, re.S)
    time = ''
    if meta:
        tail = text(meta[1]).split('·')[-1].strip()
        if '~' in tail:
            time = tail
    published = None
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
        obj = json.loads(block)
        if obj.get('@type') == 'BlogPosting' and obj.get('datePublished'):
            published = obj['datePublished']
    label = [words['longread']]
    if part_number:
        label += [words['series'], f"{words['part']} {part_number[0]}"]
    elif published:
        year, month = published[:4], int(published[5:7])
        label.append(f"{MONTHS.get(lang, MONTHS['en'])[month - 1]} {year}")
    return {
        'lang': lang,
        'title': title,
        'lead': html.unescape(lead[1]) if lead else '',
        'label': ' · '.join(label),
        'time': time,
        'author': words['author'],
        'tagline': 'anvilarth' + (f" · {published[:4]}" if published else ''),
    }


def render(params: dict, png: Path, profile: Path, chrome: str) -> None:
    url = (ROOT / 'templates/og.html').resolve().as_uri() + '?' + urlencode(params)
    cmd = ['perl', '-e', 'alarm 60; exec @ARGV', chrome, '--headless=new', '--disable-gpu',
           '--allow-file-access-from-files', f'--user-data-dir={profile}', '--hide-scrollbars',
           '--window-size=1200,630', '--virtual-time-budget=3000', f'--screenshot={png}', url]
    subprocess.run(cmd, check=True, capture_output=True)
    if not png.exists():
        raise SystemExit(f'Chrome produced no screenshot for {png.name}')


def to_jpeg(png: Path, jpg: Path) -> None:
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '88', str(png), '--out', str(jpg)],
                   check=True, capture_output=True)
    png.unlink()


def option(args, name, default=None):
    if name in args:
        i = args.index(name)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return default


def main() -> int:
    args = sys.argv[1:]
    drafts = '--drafts' in args
    if drafts:
        args.remove('--drafts')
    out = Path(option(args, '--out', ROOT / 'static/img/og'))
    suffix = option(args, '--suffix', '')
    chrome = option(args, '--chrome', CHROME)
    profile = option(args, '--profile')
    profile = Path(profile) if profile else Path(tempfile.mkdtemp(prefix='og-chrome-'))
    out.mkdir(parents=True, exist_ok=True)
    posts = ROOT / 'posts'
    slugs = args or sorted(p.name for p in posts.iterdir() if p.is_dir() and (drafts or not (p / 'DRAFT').exists()))
    for slug in slugs:
        post = posts / slug / 'post.html'
        if not re.search(r'<p class="meta"', post.read_text()):
            print(f'{slug}: not a longread (no header meta), skipped')
            continue
        params = metadata(post)
        png = out / f'og-{slug}{suffix}.png'
        render(params, png, profile, chrome)
        to_jpeg(png, out / f'og-{slug}{suffix}.jpg')
        print(f"wrote {out / f'og-{slug}{suffix}.jpg'}: {params['label']} · {params['title'][:50]}")
    return 0
