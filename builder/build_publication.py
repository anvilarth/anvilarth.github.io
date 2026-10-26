"""Finish the pages in dist/: shared template, analytics, static language pages and Latest.

Runs on the copies in dist/, before the sitemap is generated.
Blog cards supply Latest copy; article JSON-LD supplies publication dates.
"""
import html
import json
import re
from datetime import datetime

from .bake_en import Finder, bake, load_T
from .longread_enhance import enhance
from .longread_template import apply_template, apply_tool_footer
from .paths import BASE, DIST, ROOT

LOCALES = json.loads((ROOT / 'builder/locales.json').read_text())
ANALYTICS = '<script data-goatcounter="https://anvilarth.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'


def analytics(source):
    # Autoresearch already loads GoatCounter dynamically; keep exactly one loader.
    loaders = re.findall(r'<script\b[^>]*>.*?</script>', source, re.S)
    count = sum('gc.zgo.at/count.js' in script for script in loaders)
    if count > 1:
        raise ValueError('Duplicate GoatCounter loaders')
    if not count:
        source = source.replace('</body>', ANALYTICS + '\n</body>')
    return source


def language_runtime(source):
    """Normalize old article builders as well as already normalized pages."""
    old = "  if (lang === 'en') { if (location.hash === '#ru') history.replaceState(null, '', location.pathname); }\n  else { if (location.hash !== '#ru') history.replaceState(null, '', '#ru'); }"
    source = source.replace(old, '')
    source = source.replace("if (location.hash === '#ru') setLang('ru'); else setLang('en');", 'setLang(document.documentElement.lang);')
    if '    if (updateURL) {' in source:
        start = source.index('    if (updateURL) {')
        end = source.index("  document.getElementById('theme-btn').addEventListener", start)
        source = source[:start] + '  };\n  setLang(root.lang, false);\n' + source[end:]
    source = source.replace("var LANG='en';", 'var LANG=document.documentElement.lang;')
    source = source.replace("button.setAttribute('aria-pressed', String(value === lang));", "button.setAttribute('aria-current', value === lang ? 'page' : 'false');")
    source = re.sub(r"^  document.title = lang === 'ru' \?.* : DOC_TITLE;\n", '', source, flags=re.M)
    if '<script src="language-links.js"></script>' not in source:
        source = source.replace('</head>', '<script src="language-links.js"></script>\n</head>')
    return source


class AttributeTranslations(Finder):
    def __init__(self, source, translations, lang):
        super().__init__(source)
        self.translations = translations
        self.lang = lang
        self.edits = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        original = self.get_starttag_text()
        changed = original
        for attr in ('alt', 'aria-label', 'tex'):
            key = a.get('data-i18n-' + attr)
            if key:
                value = html.escape(self.translations[key][self.lang], quote=True)
                target = 'data-tex' if attr == 'tex' else attr
                pattern = r'(?<![\w-])' + target + r'="[^"]*"'
                changed, n = re.subn(pattern, lambda m: f'{target}="{value}"', changed)
                if n != 1:
                    raise ValueError(f'Missing translated attribute: {target}')
        if changed != original:
            self.edits.append((self.off(), self.off() + len(original), changed))
        super().handle_starttag(tag, attrs)


def localized(source, slug, lang):
    source, _ = bake(source, lang)
    parser = AttributeTranslations(source, load_T(source), lang)
    parser.feed(source)
    for start, end, replacement in reversed(parser.edits):
        source = source[:start] + replacement + source[end:]
    source = re.sub(r'<html lang="[^"]+">', f'<html lang="{lang}">', source, count=1)
    url = BASE + slug + ('.ru.html' if lang == 'ru' else '.html')
    source = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?', '', source)
    links = ''.join(f'<link rel="alternate" hreflang="{code}" href="{BASE}{slug}{suffix}">\n'
                    for code, suffix in [('en', '.html'), ('ru', '.ru.html'), ('x-default', '.html')])
    source = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{url}">\n' + links.rstrip(), source)
    source = re.sub(r'(<meta property="og:url" content=")[^"]+', lambda m: m[1] + url, source)
    source = re.sub(r'(<meta property="og:locale" content=")[^"]+', lambda m: m[1] + ('ru_RU' if lang == 'ru' else 'en_US'), source)
    switch = '<div class="lang-switch">' + ''.join(
        f'<a class="lang-btn{" active" if code == lang else ""}" id="btn-{code}" data-language="{code}" '
        f'hreflang="{code}" lang="{code}" href="{slug}{suffix}"' + (' aria-current="page"' if code == lang else '') + f'>{code.upper()}</a>'
        for code, suffix in [('ru', '.ru.html'), ('en', '.html')]) + '</div>'
    source, n = re.subn(r'<div class="lang-switch">.*?</div>', lambda m: switch, source, flags=re.S)
    if n != 1:
        raise ValueError(f'{slug}: expected one language switch')
    if lang == 'ru':
        meta = LOCALES[slug]
        if 'heading' in meta:
            source = re.sub(r'<h1>.*?</h1>', lambda m: '<h1>' + html.escape(meta['heading']) + '</h1>', source, count=1)
        source = re.sub(r'<title>.*?</title>', lambda m: '<title>' + html.escape(meta['title']) + '</title>', source, count=1)
        for key in ('description', 'og:description', 'twitter:description', 'og:title', 'twitter:title'):
            value = meta['title' if key.endswith('title') else 'description']
            pattern = r'(<meta (?:name|property)="' + key + r'" content=")[^"]*'
            source = re.sub(pattern, lambda m: m[1] + html.escape(value, quote=True), source)
        def schema(match):
            obj = json.loads(match[1])
            if obj.get('@type') == 'BlogPosting':
                obj.update(headline=meta['title'], description=meta['description'], inLanguage='ru', mainEntityOfPage=url)
            return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'
        source = re.sub(r'<script type="application/ld\+json">(.*?)</script>', schema, source, flags=re.S)
        source = source.replace('</svg>Main</a>', '</svg>Главная</a>').replace('</svg>Blog</a>', '</svg>Блог</a>')
        source = source.replace('aria-label="Toggle theme"', 'aria-label="Переключить тему"').replace('title="Toggle theme"', 'title="Переключить тему"')
    return source


def latest_block(blog, pages):
    cards = re.findall(r'<a href="(/[^"]+\.html)" class="post-item">(.*?)</a>', blog, re.S)
    candidates = []
    for href, card in cards:
        source = pages.get(href.lstrip('/'))
        if source is None:
            raise ValueError(f'Blog card points to an unregistered page: {href}')
        schemas = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)]
        articles = [s for s in schemas if s.get('@type') == 'BlogPosting']
        if not articles:
            continue  # Interactive tools are not dated article publications.
        date = datetime.fromisoformat(articles[0]['datePublished']).date()
        def field(cls):
            match = re.search(r'<[^>]+class="' + cls + r'"[^>]*>(.*?)</[^>]+>', card, re.S)
            if not match:
                raise ValueError(f'{href}: missing {cls}')
            return match[1]
        candidates.append((date, href, field('post-date'), field('post-title'), field('post-desc')))
    if not candidates:
        raise ValueError('No published articles found for Latest')
    _, href, date_label, title, description = max(candidates)
    return (f'<div class="latest-post">\n'
            f'    <span class="latest-post-date">Latest · {date_label}</span>\n'
            f'    <a href="{href}" class="latest-post-title">{title}</a>\n'
            f'    <p class="latest-post-desc">{description}</p>\n  </div>')


def build():
    from .gen_sitemap import BASE_PAGES
    pages = {name: (DIST / name).read_text() for name, _, _ in BASE_PAGES}
    for slug in LOCALES:
        name = slug + '.html'
        source = analytics(apply_template(language_runtime(pages[name]), slug))
        for lang, target in (('en', name), ('ru', slug + '.ru.html')):
            pages[target] = enhance(localized(source, slug, lang), lang)
    tool = 'realtime-video-calculator.html'
    pages[tool] = apply_tool_footer(pages[tool])
    pages = {name: analytics(source) for name, source in pages.items()}
    block = latest_block(pages['blog.html'], pages)
    pages['index.html'], count = re.subn(r'<div class="latest-post">.*?</div>', lambda m: block, pages['index.html'], flags=re.S)
    if count != 1:
        raise ValueError('Expected exactly one Latest block on the homepage')
    return pages


def write():
    for name, content in build().items():
        (DIST / name).write_text(content)
