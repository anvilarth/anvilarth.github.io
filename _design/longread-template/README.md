# Shared longread template

All published longreads use this template: GPU Story, Autoresearch, Preference Optimization.

- `footer.html` and `footer.css`: identical bilingual agent-links block for all four blog articles, including the realtime video calculator. No per-article Markdown links.
- `style.css`: common fonts, palette, navigation, typography, chapters, callouts, sources and footer.
- `nav.html`: navigation markup for new article builders; preserve `setLang`, `btn-ru`, `btn-en`, `theme-btn` when wiring controls.
- `../../post-toc.js` and `../../post-toc.css`: chapter-only sidebar, including sources.
- `../longread_template.py`: embeds the common styles and renders the same bilingual footer, with exactly the same two links on every article: `/llms.txt` and `/llms-full.txt`.

Run `python3 _design/longread_template.py` after template changes, then `python3 _design/longread_template.py --check`. CI checks for drift. A new longread must be added to `POSTS` in that script.

Use `<aside class="closing-takeaway"><p>…</p><p>…</p></aside>` for an explicitly selected concluding callout. It remains highlighted in both themes and both languages. Do not infer or rewrite a conclusion automatically.

Sources use `<section class="src"><h3>Sources</h3><ul><li>…</li></ul></section>`. Their citation text remains article-specific. The generated agent-links paragraph follows this section inside the article's content container. Its labels follow the root `lang` attribute.

Keep diagrams, equations, interactive demos and their CSS in article-specific files. Do not copy the common styles into a new article. Local build scripts call the same finalizer before reporting success; the finalizer does not publish or push anything.

Language and SEO: English is the static, indexable text of every longread (`<html lang="en">`); Russian is a client-side toggle (`#ru`) and is not indexed. In GPU Story and Autoresearch, edit both languages in `var T = {...}` and run `python3 _design/bake_en.py` (CI runs `--check`). Article `<head>` metadata sits between `<!-- seo-head -->` markers: one `BlogPosting` JSON-LD with full `datePublished` and `dateModified`. `gen_sitemap.py` takes `lastmod` from `dateModified`, so bump it when the content really changes.
