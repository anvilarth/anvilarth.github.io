"""Assemble dist/ from the repository sources, then finish the pages in place."""
import shutil
from pathlib import Path

from . import build_publication, gen_sitemap
from .paths import DIST, ROOT

POSTS = ROOT / 'posts'
# A post folder publishes post.html as /<slug>.html, its Markdown mirrors as
# /<slug>.md and /<slug>.en.md, and every other file under /assets/<slug>/.
POST_FILES = {'post.html': '{slug}.html', 'post.md': '{slug}.md', 'post.en.md': '{slug}.en.md'}


def files_under(folder: Path):
    return (p for p in sorted(folder.rglob('*')) if p.is_file() and p.name != '.DS_Store')


def sources(drafts: bool = False) -> dict[str, Path]:
    """Map every published path (relative to dist/) to its source file."""
    out = {}
    def add(rel: str, source: Path) -> None:
        if rel in out:
            raise SystemExit(f'{rel} comes from both {out[rel]} and {source}')
        out[rel] = source
    # Static files and hand-made pages keep their paths at the site root.
    for folder in ('static', 'pages'):
        for path in files_under(ROOT / folder):
            add(path.relative_to(ROOT / folder).as_posix(), path)
    for post in sorted(p for p in POSTS.iterdir() if p.is_dir()):
        if (post / 'DRAFT').exists() and not drafts:
            continue
        for path in files_under(post):
            rel = path.relative_to(post).as_posix()
            if rel == 'DRAFT':
                continue
            add(POST_FILES[rel].format(slug=post.name) if rel in POST_FILES else f'assets/{post.name}/{rel}', path)
    return out


def build(drafts: bool = False) -> None:
    files = sources(drafts)
    shutil.rmtree(DIST, ignore_errors=True)
    for rel, source in files.items():
        target = DIST / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    build_publication.write()
    gen_sitemap.write(files)
    print(f'Built dist/: {len(files)} source files' + (' (with drafts)' if drafts else ''))
