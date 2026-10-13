"""Keep English as the static, indexable text of bilingual longreads.

python3 _design/bake_en.py          # bake T[key].en into every [data-i18n] element
python3 _design/bake_en.py --check  # fail when static HTML drifts from T

Russian stays a client-side toggle (#ru): search engines index English only.
Edit both languages in the page's `var T = {...}`, then run this script.
"""
import html, json, re, subprocess, sys
from html.parser import HTMLParser

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr'}

def load_T(src):
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

SITE = __import__('pathlib').Path(__file__).resolve().parent.parent
PAGES = ('gpu-story.html', 'autoresearch.html')

if __name__ == '__main__':
    stale = []
    for name in PAGES:
        path = SITE / name
        src = path.read_text(encoding='utf-8')
        out, n = bake(src)
        if out != src:
            stale.append(name)
            if '--check' not in sys.argv:
                path.write_text(out, encoding='utf-8')
    if '--check' in sys.argv and stale:
        raise SystemExit('Static English text is stale: ' + ', '.join(stale) + ' (run python3 _design/bake_en.py)')
    print('Static English text: ' + ('verified' if '--check' in sys.argv else 'baked'))
