# Site maintenance

Communicate with the user in Russian. Keep repository instructions in English.

## Scope and sources

- `master` is the only branch; GitHub Pages publishes it. Do not create
  long-lived branches. The pre-2026-10 `master` application history is kept only
  as local tags `archive/master-*`. Check working changes before editing.
- Preserve the existing design and unrelated content. Use scoped commits.
- DPO's editorial source and builder live in the adjacent `tg_channel` project,
  under `posts/preference_optimization/`. Follow that project's instructions if
  editing its prose. After importing any rebuilt article, run this site's
  publication build; do not publish the raw builder output directly.
- Repository layout. Only these folders hold site sources:
  - `posts/<slug>/` — one folder per article. `post.html` is published as
    `/<slug>.html`, `post.md` / `post.en.md` as `/<slug>.md` / `/<slug>.en.md`
    (Markdown mirrors for LLMs), every other file under `/assets/<slug>/`.
    An empty `DRAFT` file keeps the post out of the build.
  - `pages/` — hand-made pages (home, blog, projects), published at
    the site root. `static/` — files copied to the root as is (icons, fonts,
    robots, llms.txt, verification files).
  - `templates/` — never published: the shared longread template
    (`longread/`) and the sources of generated images (`og.html` for social
    cards, `apple-touch-icon.svg`, `project-covers.py` for project covers).
    `builder/` — the Python build (`uv run builder ...`).
- `dist/` is the build output: never edit or commit it. GitHub Actions builds it
  and deploys it to Pages. `*.ru.html` and `sitemap.xml` exist only in `dist/`.
- English `post.html` files hold the bilingual translation data and are the
  source for localized output.
- Do not create Markdown mirrors of articles unless the user asks for them.
- Never commit credentials. `.env` is local, ignored, and must have mode `0600`.
  Never echo its contents or private keys in logs, PRs or tool output.

## Required publication workflow

Dependencies are managed with uv (`pyproject.toml`, committed `uv.lock`, plain
PyPI). The build itself needs only the standard library.

1. Edit the post in `posts/<slug>/`. For a new article, add its card to
   `pages/blog.html`, register the page in `BASE_PAGES` in
   `builder/gen_sitemap.py`, and register bilingual metadata in
   `builder/locales.json` when both translations exist. Posts built in
   `tg_channel` are synced by their `publish_build.py` into `posts/<slug>/`.
2. Keep JSON-LD `datePublished` equal to the real first publication date.
   Change `dateModified` for substantive content changes only; template, analytics
   and language build changes must not pretend that the article was rewritten.
3. Run `uv run builder build` (add `--drafts` to include draft posts), then
   `uv run builder check` and `git diff --check`. The build applies the shared
   template, bakes both languages, ensures one GoatCounter loader per public
   page, derives the homepage Latest card from the newest article in the blog
   (never maintain it by hand) and writes the sitemap. Preview with
   `uv run builder serve`.
4. Review the exact diff and stage only the intended files. Publication needs
   user authorization; when already authorized in the conversation, proceed.
5. Pushing to `master` publishes: the `Site` workflow builds `dist/`, deploys
   it to Pages, runs Lighthouse, and submits the sitemap to Google and changed
   URLs to IndexNow.
6. After publishing, verify the deployed pages and assets, the live sitemap,
   Pages deployment and search-submission jobs. A successful API submission is
   not proof of crawling or indexing. Report these states separately.

Sitemap `lastmod` comes from `dateModified` for articles and from Git history
(ignoring pure renames) for other pages.
Do not bypass failing checks.
The user has paused test execution: do not run unit, integration, smoke or
browser test suites unless explicitly requested. Structural/source checks above
remain enabled. Do not disable existing CI as part of unrelated work.

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
