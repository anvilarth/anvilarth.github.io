"""Shared locations: sources live in the repository, the built site in dist/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
BASE = 'https://anvilarth.github.io/'
TEMPLATE = ROOT / '_design/longread-template'
