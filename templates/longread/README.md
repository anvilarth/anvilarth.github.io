# Shared longread template

All published longreads use this template: GPU Story, Autoresearch, Preference Optimization.

- `footer.html` and `footer.css`: identical bilingual agent-links block for all four blog articles, including the realtime video calculator. No per-article Markdown links.
- `style.css`: common fonts, palette, navigation, typography, chapters, callouts, sources and footer.
- `nav.html`: navigation markup for new article builders; preserve `setLang`, `btn-ru`, `btn-en`, `theme-btn` when wiring controls.
- `post-toc.js` and `../../static/post-toc.css`: chapter-only sidebar, including sources.
- `../../builder/longread_template.py`: embeds the common styles and renders the same bilingual footer, with exactly the same two links on every article: `/llms.txt` and `/llms-full.txt`.

The template is applied at build time (`uv run builder build`); sources never contain its output. A new longread is registered in `builder/locales.json`.

Use `<aside class="closing-takeaway"><p>…</p><p>…</p></aside>` for an explicitly selected concluding callout. It remains highlighted in both themes and both languages. Do not infer or rewrite a conclusion automatically.

Sources use `<section class="src"><h3>Sources</h3><ul><li>…</li></ul></section>`. Their citation text remains article-specific. The generated agent-links paragraph follows this section inside the article's content container. Its labels follow the root `lang` attribute.

Keep diagrams, equations, interactive demos and their CSS in article-specific files. Do not copy the common styles into a new article. Local build scripts call the same finalizer before reporting success; the finalizer does not publish or push anything.

Language and SEO: English is the static text of every bilingual longread; the build bakes a separate, indexable `/<slug>.ru.html`. Edit both languages in `var T = {...}`. Article `<head>` metadata sits between `<!-- seo-head -->` markers: one `BlogPosting` JSON-LD with full `datePublished` and `dateModified`. `builder/gen_sitemap.py` takes `lastmod` from `dateModified`, so bump it when the content really changes.
