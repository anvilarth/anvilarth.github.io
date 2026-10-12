"""Apply the shared longread presentation without rewriting article content.

python3 _design/longread_template.py          # refresh site articles
python3 _design/longread_template.py --check  # fail on template drift
python3 _design/longread_template.py FILE --slug SLUG  # local article build
"""
from pathlib import Path
import argparse
import re
import shutil

SITE = Path(__file__).resolve().parent.parent
TEMPLATE = SITE / '_design/longread-template'
POSTS = ('gpu-story', 'autoresearch', 'preference-optimization')
START = '<!-- shared-longread-template -->'
END = '<!-- /shared-longread-template -->'

def footer():
    return (TEMPLATE / 'footer.html').read_text().strip()


def apply_template(page, slug):
    page = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', page, flags=re.S)
    # All pages receive the exact same styles; embedding also works on file://.
    css = (TEMPLATE / 'style.css').read_text() + (TEMPLATE / 'footer.css').read_text() + '\n' + (SITE / 'post-toc.css').read_text()
    page = re.sub(r'<script\b[^>]*src=[\"\']/post-toc.js[\"\'][^>]*></script>', '', page)
    toc = (SITE / 'post-toc.js').read_text()
    block = START + '\n<style data-template="longread">' + css + '</style>\n<script data-template="toc">' + toc + '</script>\n' + END + '\n'
    assert '</head>' in page
    page = page.replace('</head>', block + '</head>', 1)
    page = re.sub(r'<p\b[^>]*class="md-link"[^>]*>.*?</p>\s*', '', page, flags=re.S)
    source = re.search(r'<section\b[^>]*class="src"[^>]*>.*?</section>', page, flags=re.S)
    if not source:
        raise ValueError(f'{slug}: missing sources section')
    page = page[:source.end()] + '\n' + footer() + '\n' + page[source.end():].lstrip('\n')
    return page

def apply_tool_footer(page):
    page = re.sub(r'<!-- shared-agent-footer -->.*?<!-- /shared-agent-footer -->\n?', '', page, flags=re.S)
    page = re.sub(r'<p\b[^>]*class="md-link"[^>]*>.*?</p>\s*', '', page, flags=re.S)
    css = (TEMPLATE / 'footer.css').read_text()
    page = page.replace('</head>', '<!-- shared-agent-footer --><style>' + css + '</style><!-- /shared-agent-footer -->\n</head>', 1)
    return page.replace('</main>', footer() + '\n</main>', 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', nargs='?', type=Path)
    parser.add_argument('--slug')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    paths = [(args.file, args.slug or args.file.stem)] if args.file else [(SITE / (slug + '.html'), slug) for slug in (*POSTS, 'realtime-video-calculator')]
    stale = []
    for path, slug in paths:
        before = path.read_text()
        after = apply_tool_footer(before) if slug == 'realtime-video-calculator' else apply_template(before, slug)
        if before != after:
            stale.append(path.name)
            if not args.check:
                path.write_text(after)
                if path.parent.resolve() != SITE:
                    shutil.copytree(SITE / 'fonts', path.parent / 'fonts', dirs_exist_ok=True)
    if args.check and stale:
        raise SystemExit('Stale longread template: ' + ', '.join(stale))
    print('Shared longread template: ' + ('verified' if args.check else 'applied'))

if __name__ == '__main__':
    main()
