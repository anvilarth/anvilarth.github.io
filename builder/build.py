"""Assemble dist/ from the repository sources, then finish the pages in place."""
import shutil
from pathlib import Path

from . import build_publication, gen_sitemap
from .paths import DIST, ROOT

# Repository files that are not part of the site.
PRIVATE = {'builder', 'dist', 'pyproject.toml', 'uv.lock', 'AGENTS.md', 'README.md'}
# Unpublished articles: <slug>.html and assets/<slug>/ stay out of dist/ unless --drafts.
DRAFTS = {'rl-for-diffusion-part-1'}


def is_draft(rel: Path) -> bool:
    parts = rel.parts
    return (len(parts) == 1 and rel.suffix == '.html' and rel.stem in DRAFTS) or \
        (len(parts) > 1 and parts[0] == 'assets' and parts[1] in DRAFTS)


def sources(drafts: bool = False) -> dict[str, Path]:
    """Map every published path (relative to dist/) to its source file."""
    out = {}
    for path in sorted(ROOT.rglob('*')):
        rel = path.relative_to(ROOT)
        top = rel.parts[0]
        if top.startswith(('_', '.')) or top in PRIVATE or path.is_dir():
            continue
        if not drafts and is_draft(rel):
            continue
        out[rel.as_posix()] = path
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
