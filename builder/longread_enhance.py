"""Structural additions to a baked longread page that need no author markup.

Runs in build_publication.py on each language page after the shared template
and the translation bake, so the page's `lang` and heading text are final:

- stable ids on h2/h3 (from data-i18n keys, then the text), so anchors and the
  contents navigation work without JavaScript;
- `eq-N` ids and `tabindex="0"` on display equations (`.equation`), plus the
  `eq-numbered` body class when a post has at least three of them;
- `fig-N` ids on captioned, visible figures (`.fig .figc`, `figure figcaption`),
  matching the CSS counter that prefixes captions with "Fig. N." / "Рис. N.";
- `data-label` on table cells from their header, for the phone card layout;
- a compact contents list before the first chapter, shown on phones only;
- the theme bootstrap defaults to the light theme instead of the system one.
"""
import html
import re
from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
LABELS = {'ru': 'В статье', 'en': 'In this article'}
THEME_OLD = ("var t=(q==='dark'||q==='light')?q:localStorage.getItem('theme');"
             "if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t)")
THEME_NEW = ("var t=(q==='dark'||q==='light')?q:localStorage.getItem('theme');"
             "document.documentElement.setAttribute('data-theme',t==='dark'?'dark':'light')")


class Elements(HTMLParser):
    """Every element with its source span, class list and hidden state."""

    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.lines = [0]
        for m in re.finditer('\n', src):
            self.lines.append(m.end())
        self.stack = []
        self.elements = []

    def off(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        start = self.off()
        hidden = 'display:none' in (a.get('style') or '').replace(' ', '') or any(e['hidden'] for e in self.stack)
        el = {'tag': tag, 'attrs': a, 'classes': (a.get('class') or '').split(), 'start': start,
              'open_end': start + len(self.get_starttag_text()), 'end': None, 'hidden': hidden,
              'parent': self.stack[-1] if self.stack else None}
        self.elements.append(el)
        if tag not in VOID:
            self.stack.append(el)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                for e in self.stack[i:]:
                    e['end'] = self.off()
                del self.stack[i:]
                return


def parse(src):
    p = Elements(src)
    p.feed(src)
    p.close()
    return p.elements


def inside(el, pred):
    while el is not None:
        if pred(el):
            return True
        el = el['parent']
    return False


def text_of(src, el):
    inner = src[el['open_end']:el['end']] if el['end'] else ''
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', inner))).strip()


def slugify(text):
    text = re.sub(r'[^\w]+', '-', text.lower(), flags=re.U).strip('-')
    return text[:60].rstrip('-') or 'section'


def add_attrs(src, el, attrs, edits):
    """Queue extra attributes for an element's start tag (skips ones it has)."""
    extra = ''.join(f' {k}="{html.escape(str(v), quote=True)}"' for k, v in attrs.items() if k not in el['attrs'])
    if not extra:
        return
    tag = src[el['start']:el['open_end']]
    assert tag.endswith('>')
    cut = -2 if tag.endswith('/>') else -1
    edits.append((el['start'], el['open_end'], tag[:cut] + extra + tag[cut:]))


def enhance(page, lang):
    els = parse(page)
    edits = []  # (start, end, replacement), non-overlapping
    main = next((e for e in els if e['tag'] == 'main'), None)
    in_main = (lambda e: inside(e, lambda x: x is main)) if main else (lambda e: True)
    in_src = lambda e: inside(e, lambda x: 'src' in x['classes'])
    in_nav = lambda e: inside(e, lambda x: x['tag'] == 'nav' or 'post-nav' in x['classes'])
    used = {e['attrs']['id'] for e in els if 'id' in e['attrs']}

    # Headings: ids for anchors, the sidebar and the phone contents.
    chapters = []
    counts = {'h2': 0, 'h3': 0}
    for e in els:
        if e['tag'] not in ('h2', 'h3') or not in_main(e) or in_nav(e) or in_src(e):
            continue
        counts[e['tag']] += 1
        if 'id' not in e['attrs']:
            base = e['attrs'].get('data-i18n') or slugify(text_of(page, e)) or f"{'section' if e['tag'] == 'h2' else 'sub'}-{counts[e['tag']]}"
            ident, suffix = base, 2
            while ident in used:
                ident = f'{base}-{suffix}'
                suffix += 1
            used.add(ident)
            add_attrs(page, e, {'id': ident}, edits)
            e['attrs']['id'] = ident
        if e['tag'] == 'h2':
            chapters.append((e['attrs']['id'], text_of(page, e)))

    # Display equations.
    equations = [e for e in els if 'equation' in e['classes'] and e['tag'] == 'div']
    for n, e in enumerate(equations, 1):
        add_attrs(page, e, {'id': f'eq-{n}', 'tabindex': '0'}, edits)

    # Captioned, visible figures; hidden ones generate no CSS counter step either.
    def is_figure(e):
        return e['tag'] == 'figure' or (e['tag'] == 'div' and 'fig' in e['classes'])
    def figure_of(e):
        p = e['parent']
        while p is not None and not is_figure(p):
            p = p['parent']
        return p
    captioned = []
    for e in els:
        if e['tag'] == 'figcaption' or 'figc' in e['classes']:
            fig = figure_of(e)
            if fig is not None and not fig['hidden'] and not e['hidden'] and fig not in captioned:
                captioned.append(fig)
    for n, fig in enumerate(captioned, 1):
        add_attrs(page, fig, {'id': f'fig-{n}'}, edits)

    # Tables: header text on every body cell for the phone layout.
    for table in (e for e in els if e['tag'] == 'table'):
        rows = [e for e in els if e['tag'] == 'tr' and inside(e, lambda x: x is table)]
        headers = None
        for row in rows:
            cells = [e for e in els if e['tag'] in ('th', 'td') and e['parent'] is row]
            if headers is None:
                if all(c['tag'] == 'th' for c in cells) and cells:
                    headers = [text_of(page, c) for c in cells]
                continue
            for cell, label in zip(cells, headers):
                if cell['tag'] == 'td' and label:
                    add_attrs(page, cell, {'data-label': label}, edits)

    # Phone contents before the first chapter.
    first = next((e for e in els if e['tag'] == 'section' and 'ch' in e['classes']), None)
    if first is not None and len(chapters) >= 2 and 'class="post-contents"' not in page:
        label = LABELS.get(lang, LABELS['en'])
        items = ''.join(f'<li><a href="#{ident}">{html.escape(title)}</a></li>' for ident, title in chapters)
        block = (f'<nav class="post-contents" aria-label="{label}"><p class="post-contents-title">{label}</p>'
                 f'<ol>{items}</ol></nav>\n')
        edits.append((first['start'], first['start'], block))

    for start, end, replacement in sorted(edits, key=lambda x: x[0], reverse=True):
        page = page[:start] + replacement + page[end:]

    if len(equations) >= 3 and not re.search(r'<body[^>]*class="[^"]*\beq-numbered\b', page):
        page, n = re.subn(r'<body(\s[^>]*)?>', lambda m: body_with_class(m[0], 'eq-numbered'), page, count=1)
        if n != 1:
            raise ValueError('missing <body>')

    page = page.replace(THEME_OLD, THEME_NEW, 1)
    return page


def body_with_class(tag, cls):
    if 'class="' in tag:
        return tag.replace('class="', f'class="{cls} ', 1)
    return tag[:-1] + f' class="{cls}">'
