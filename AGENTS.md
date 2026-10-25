# Site maintenance

Communicate with the user in Russian. Keep repository instructions in English.

## Repository rules

These rules are mandatory for every agent and session. `uv run builder check`
enforces the mechanical ones locally and in CI. If a task seems to need an
exception, stop and ask the user.

### Layout

Every file has exactly one place:

| Path | Holds | Published as |
|---|---|---|
| `posts/<slug>/` | one article: `post.html`, optional Markdown mirrors `post.md` / `post.en.md`, the article's own files | `/<slug>.html`, `/<slug>.md`, `/<slug>.en.md`, `/assets/<slug>/…` |
| `pages/` | hand-made pages: home, blog, projects, `about.md` profile | site root |
| `static/` | files served as is: icons, fonts, `robots.txt`, `llms.txt`, shared scripts and styles, images used by pages | site root |
| `templates/` | the shared longread template (`longread/`) and sources of generated images (`og.html`, `apple-touch-icon.svg`, `project-covers.py`) | never |
| `builder/` | the build and its checks, run as `uv run builder …` | never |

- The root holds only `AGENTS.md`, `CLAUDE.md`, `pyproject.toml`, `uv.lock`,
  `.gitignore` and `.github/`. Do not add top-level files or folders, or a new
  kind of content to these folders, without the user's approval.
- A slug is lowercase words joined by hyphens, and it is the article's URL. An
  empty `DRAFT` file in a post folder keeps the post out of the build.
- Files used by a single article go into its folder. Images already in
  `static/img/` stay there because their URLs are public.

### Never commit

- Build output: `dist/`, `*.ru.html`, `sitemap.xml`, `llms-full.txt`.
- Leftovers: backups, old or alternative versions of a file, design sketches,
  screenshots, notes, reports, logs, scratch scripts. Git history is the
  archive; scratch work goes to a temporary directory outside the repository.
- Local state: `.env`, `.venv/`, `__pycache__/`, `.DS_Store`, editor files.
- Credentials and private keys. `.env` stays local with mode `0600`; never echo
  its contents or private keys in logs, PRs or tool output. The IndexNow key
  is public by design.
- Unused files. When a change stops using a file, delete the file in the same
  commit. The exception is files used from outside, which nothing on the site
  links to; keep them at their URLs: `static/favicon.ico` (browsers request
  it), `static/googlef9829f193c6aa21c.html` (Search Console ownership),
  `static/b16ed2af9fe652f7c59f8cdc82697b13.txt` (IndexNow key) and
  `static/img/og/banner-2x.jpg` (the GitHub profile README embeds it).

### Editing

- Published URLs are permanent. Do not rename, move or delete a published page,
  Markdown mirror, image or other file without the user's approval.
- Edit sources only, never `dist/` or generated output. The block between the
  `<!-- shared-longread-template -->` markers in a post is replaced by the
  build: change `templates/longread/` instead. The homepage Latest card is
  derived by the build: never maintain it by hand.
- DPO (`posts/preference_optimization/`) and RL for Diffusion
  (`posts/rl_for_diffusion_part_1/`) are written and built in the adjacent
  `tg_channel` project, then synced here by their `publish_build.py`. Edit
  them there and follow that project's instructions; never hand-edit their
  copies in `posts/`.
- Preserve the existing design and unrelated content. Do not create Markdown
  mirrors of articles unless the user asks for them.

### Git

- `master` is the only branch. Do not create branches or tags, force-push,
  rewrite pushed history or use `[skip ci]`. The pre-2026-10 history is kept
  only as the local tags `archive/master-*`.
- Start every task with `git status`. Changes you did not make belong to
  someone else: never stage, commit, revert, stash or overwrite them. Work
  around them and tell the user.
- One commit is one logical change. Stage files by name; never use
  `git add -A`, `git add .` or `git commit -a`.
- Before committing, run `uv run builder build`, `uv run builder check` and
  `git diff --cached --check`. Never commit or push with a failing check, and
  never weaken, skip or disable a check or CI job to get past it. If someone
  else's uncommitted changes are in the tree, run the checks in a temporary
  `git worktree add --detach` of `HEAD` with only your staged diff applied.
- Pushing to `master` publishes the site. Push only when the user has
  authorized publishing this change.

### Dependencies

The build uses only the Python standard library. A new package needs the
user's approval: add it with `uv add --group <group>`, pinned to an exact
version from plain PyPI, and commit `uv.lock` with it.

## Publication workflow

1. Edit the article in `posts/<slug>/`, or in `tg_channel` and sync it. For a
   new article, add its card to `pages/blog.html`, register the page in
   `BASE_PAGES` in `builder/gen_sitemap.py`, and register bilingual metadata in
   `builder/locales.json` when both translations exist.
2. Keep JSON-LD `datePublished` equal to the real first publication date.
   Change `dateModified` for substantive content changes only; template, analytics
   and language build changes must not pretend that the article was rewritten.
3. Run `uv run builder build` (`--drafts` includes draft posts) and
   `uv run builder check`; preview with `uv run builder serve`. The build
   applies the shared template, bakes both languages, adds one GoatCounter
   loader per page, derives the homepage Latest card from the newest article in
   the blog, and writes the sitemap and `llms-full.txt`.
4. Commit by the Git rules above. Pushing to `master` runs the `Site` workflow:
   build, checks, deploy to Pages, sitemap submission to Google and IndexNow.
   Lighthouse runs only when the workflow is started manually.
5. After publishing, verify the deployed pages and assets, the live sitemap,
   Pages deployment and search-submission jobs. A successful API submission is
   not proof of crawling or indexing. Report these states separately.

Sitemap `lastmod` comes from `dateModified` for articles and from Git history
(ignoring pure renames) for other pages. The user has paused test execution:
do not run unit, integration, smoke or browser test suites unless explicitly
requested. The structural checks above stay on.

## Web interface rules

Every page and article builder (including builders in `tg_channel`) follows
these rules, adapted from the Vercel Web Interface Guidelines
(https://vercel.com/design/guidelines) for a static reading site. Check new
pages against them before publication.

- Static HTML carries the page's language. Text, `alt`, `aria-label` and
  `title` are baked in that language; JavaScript may switch languages but must
  never be what puts the page's own language on screen. A page marked
  `lang="ru"` must not ship English text in its markup.
- Russian text binds short words (`в`, `к`, `с`, `и`, `на`, `по`, `не`, ...) and
  numbers to the next word with non-breaking spaces. Use «» quotes, `…` and `—`.
- Headings use `text-wrap: balance`; paragraphs, list items and captions use
  `text-wrap: pretty`.
- Any horizontally scrollable region (wide KaTeX formulas, code, tables) gets
  `tabindex="0"` so keyboard users can scroll it.
- Interactive targets are at least 24px, and 44px under `pointer: coarse`;
  expand padding with a matching negative margin instead of moving the layout.
  Controls set `touch-action: manipulation`.
- Visible `:focus-visible` outlines, a skip link to the article, and
  `scroll-margin-top` on every linked heading so the sticky nav never covers it.
- Set `color-scheme` (light/dark, following `data-theme`) and `theme-color`
  metas for both schemes; a manual theme switch also updates `theme-color`.
- Honour `prefers-reduced-motion`; animate only `transform` and `opacity`;
  never use `transition: all`.
- Images declare `width`/`height`; only above-the-fold images load eagerly.
  Preload the body-text font file for the page's language.
- Navigation uses real links; state worth sharing (language, theme, section)
  lives in the URL. Never block zoom or paste.
- Do not apply Vercel's brand copywriting rules (Title Case, `&` for "and",
  second person) to article prose; the author's editorial rules govern text.

## Language pages and tools

- English `post.html` files hold the bilingual translation data and are the
  source for localized output.
- Keep existing English URLs stable. Russian variants use `.ru.html`, include
  fully baked Russian text/translated attributes, their own canonical and social
  metadata, and reciprocal `hreflang` links. Both variants belong in the sitemap.
- Language selectors are real links and work without JavaScript. Preserve
  section anchors on switching; support old `#ru`, `#en` and `?lang=` links via
  `language-links.js`. Never silently restore English on a Russian page.
- Analytics must not double-count a page. Dynamic loaders count too; local
  validation alone does not prove delivery to the analytics service.
- Calculator sharing must round-trip every selectable model, hardware and video
  input, including hidden branches. Validate query values against allowed
  options/ranges, keep defaults for invalid values, and provide a selectable URL
  when clipboard access is unavailable. Do not change calculation formulas as a
  side effect of sharing UI work.
