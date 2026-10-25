"""Apply the shared longread presentation without rewriting article content.

Used by build_publication.py and by the article builders in tg_channel.
"""
import re

from .paths import TEMPLATE
START = '<!-- shared-longread-template -->'
END = '<!-- /shared-longread-template -->'

def footer():
    return (TEMPLATE / 'footer.html').read_text().strip()


def apply_template(page, slug):
    page = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', page, flags=re.S)
    # All pages receive the exact same styles; embedding also works on file://.
    css = (TEMPLATE / 'style.css').read_text() + (TEMPLATE / 'footer.css').read_text() + '\n' + (TEMPLATE / 'post-toc.css').read_text()
    page = re.sub(r'<script\b[^>]*src=[\"\']/post-toc.js[\"\'][^>]*></script>', '', page)
    page = re.sub(r'<link\b[^>]*href=[\"\']/post-toc.css[\"\'][^>]*>\n?', '', page)
    toc = (TEMPLATE / 'post-toc.js').read_text()
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


