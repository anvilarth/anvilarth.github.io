"""Bake a language from a page's translation data into its static HTML.

build_publication.py uses it for both the English and the Russian page.
"""
import html, json, re, subprocess
from html.parser import HTMLParser

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr'}

def load_T(src):
    embedded = re.search(r'<script id="translations" type="application/json">(.*?)</script>', src, re.S)
    if embedded:
        return json.loads(embedded.group(1))
    start = src.index('var T')
    end = src.index('function setLang', start)
    js = src[start:end]
    out = subprocess.run(['node', '-e', 'const vm=require("vm");const c={};vm.runInNewContext(require("fs").readFileSync(0,"utf8")+";this.__T=T",c);process.stdout.write(JSON.stringify(c.__T))'],
                         input=js, capture_output=True, text=True, check=True).stdout
    return json.loads(out)

class Finder(HTMLParser):
    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.lines = [0]
        for m in re.finditer('\n', src):
            self.lines.append(m.end())
        self.stack = []   # (tag, key|None, is_html, content_start)
        self.hits = []    # (start, end, key, is_html)
    def off(self):
        l, c = self.getpos()
        return self.lines[l-1] + c
    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        a = dict(attrs)
        start = self.off() + len(self.get_starttag_text())
        key = a.get('data-i18n')
        if key and any(k for _, k, _, _ in self.stack):
            raise SystemExit(f'nested data-i18n: {key}')
        self.stack.append((tag, key, 'data-i18n-html' in a, start))
    def handle_startendtag(self, tag, attrs):
        if dict(attrs).get('data-i18n'):
            raise SystemExit('self-closing data-i18n')
    def handle_endtag(self, tag):
        if tag in VOID:
            return
        # pop to matching tag (tolerate implicitly closed <p>/<li>)
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                for t, key, is_html, start in self.stack[i+1:]:
                    if key:
                        raise SystemExit(f'implicitly closed data-i18n element {t} {key}')
                t, key, is_html, start = self.stack[i]
                del self.stack[i:]
                if key:
                    self.hits.append((start, self.off(), key, is_html))
                return

def bake(src, lang='en'):
    T = load_T(src)
    f = Finder(src); f.feed(src); f.close()
    missing = [k for _, _, k, _ in f.hits if k not in T or not T[k].get(lang)]
    if missing:
        raise SystemExit(f'missing {lang} for: {missing[:10]}')
    out = src
    for start, end, key, is_html in sorted(f.hits, reverse=True):
        val = T[key][lang] if is_html else html.escape(T[key][lang], quote=False)
        out = out[:start] + val + out[end:]
    return out, len(f.hits)
