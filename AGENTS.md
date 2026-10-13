# Site maintenance

Communicate with the user in Russian. Keep repository instructions in English.

## Scope and sources

- GitHub Pages publishes `gh-pages`. `master` is an older application, not the
  current website. Check the branch and working changes before editing.
- Preserve the existing design and unrelated content. Use scoped commits.
- DPO's editorial source and builder live in the adjacent `tg_channel` project,
  under `posts/preference_optimization/`. Follow that project's instructions if
  editing its prose. After importing any rebuilt article, run this site's
  publication build; do not publish the raw builder output directly.
- Root English HTML files contain the bilingual translation data and are the
  source for localized output. `*.ru.html` files are generated: never edit them.
- Do not create Markdown mirrors of articles unless the user asks for them.
- Never commit credentials. `.env` is local, ignored, and must have mode `0600`.
  Never echo its contents or private keys in logs, PRs or tool output.

## Required publication workflow

1. Edit the relevant source HTML / translation data. For a new article, add its
   card to `blog.html`, register the page in `_design/gen_sitemap.py`, and register
   bilingual metadata in `_design/locales.json` when both translations exist.
2. Keep JSON-LD `datePublished` equal to the real first publication date.
   Change `dateModified` for substantive content changes only; template, analytics
   and language build changes must not pretend that the article was rewritten.
3. Run `python3 -B _design/build_publication.py`. This applies the shared template,
   bakes both languages, ensures one GoatCounter loader per public page, and
   derives homepage Latest from the most recently published article in the blog.
   Never maintain the homepage Latest card by hand.
4. Run `python3 -B _design/gen_sitemap.py`, then the read-only checks:
   `python3 -B _design/build_publication.py --check`,
   `python3 -B _design/bake_en.py --check`,
   `python3 -B _design/longread_template.py --check`,
   `python3 -B _design/check_site.py`, and `git diff --check`.
   Sitemap dates for non-articles depend on Git history: regenerate after the
   content commit and commit the resulting sitemap before pushing.
5. Review the exact diff and stage only the intended files. Publication needs
   user authorization; when already authorized in the conversation, proceed.
6. After publishing, verify the deployed pages and assets, the live sitemap,
   Pages deployment and search-submission jobs. A successful API submission is
   not proof of crawling or indexing. Report these states separately.

CI rejects stale generated publication files. Do not bypass failing checks.
The user has paused test execution: do not run unit, integration, smoke or
browser test suites unless explicitly requested. Structural/source checks above
remain enabled. Do not disable existing CI as part of unrelated work.

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
