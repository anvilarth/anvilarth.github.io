# Shared longread template

All published longreads use this template: GPU Story, Autoresearch, Preference Optimization.

- `footer.html` and `footer.css`: identical bilingual agent-links block for all four blog articles, including the realtime video calculator. No per-article Markdown links.
- `style.css`: common fonts, palette, navigation, typography, chapters, callouts, sources and footer.
- `nav.html`: navigation markup for new article builders; preserve `setLang`, `btn-ru`, `btn-en`, `theme-btn` when wiring controls.
- `post-toc.js` and `post-toc.css`: sidebar with chapters and sources; the current chapter's h3 subsections unfold under it. The same script adds a `#` anchor to every h2/h3 (visible on hover, click copies the section URL) and marks display equations that overflow sideways so the template can fade their right edge.
- `../../builder/longread_enhance.py`: build-time additions that need no author markup. Stable heading ids (from `data-i18n` keys or the text), `eq-N` ids on `.equation` blocks and the `eq-numbered` body class when a post has three or more (CSS then numbers them), `fig-N` ids on captioned figures (`.fig .figc`, `figure figcaption`; captions get a `Fig. N.` / `Рис. N.` prefix in the page's language), `data-label` on table cells for the phone card layout, the compact `.post-contents` list before chapter 1 on phones, and the light theme by default (the system scheme no longer picks dark; the switch and `?theme=` still do).
- `../og.html` and `../../builder/og_cards.py`: social cards rendered from article metadata, `uv run builder og`.
- `../../builder/longread_template.py`: embeds the common styles and renders the same bilingual footer, with exactly the same two links on every article: `/llms.txt` and `/llms-full.txt`.

The build strips and re-applies everything between the `<!-- shared-longread-template -->` markers in a post, so never edit that block in a source: edit the files here. To add a longread, follow the publication workflow in `../../AGENTS.md`.

Use `<aside class="closing-takeaway"><p>…</p><p>…</p></aside>` for an explicitly selected concluding callout. It remains highlighted in both themes and both languages. Do not infer or rewrite a conclusion automatically.

Reference equations and figures by their build-time ids: `<a href="#eq-3">(3)</a>`, `<a href="#fig-2">fig. 2</a>`. Numbers count display equations and captioned figures in document order, so count them before writing a reference.

A technical note (`<aside class="technical-note" role="note"><strong>…</strong><p>…</p></aside>`) becomes a margin note beside the text on screens from 1100px and stays an inline box below that.

A series block goes right before the sources:

```html
<section class="series" aria-label="Серия"><p class="series-title">Серия · RL for Diffusion models</p><ol>
<li aria-current="page"><b>Часть 1.</b> Как передать reward генератору. <span class="series-state">вы здесь</span></li>
<li><b>Часть 2.</b> Reward-модели. <span class="series-state">в работе</span></li>
</ol></section>
```

Sources use `<section class="src"><h3>Sources</h3><ul><li>…</li></ul></section>`. Their citation text remains article-specific. The generated agent-links paragraph follows this section inside the article's content container. Its labels follow the root `lang` attribute.

Keep diagrams, equations, interactive demos and their CSS in article-specific files. Do not copy the common styles into a new article. Local build scripts call the same finalizer before reporting success; the finalizer does not publish or push anything.

Language and SEO: English is the static text of every bilingual longread; the build bakes a separate, indexable `/<slug>.ru.html`. Edit both languages in `var T = {...}`. Article `<head>` metadata sits between `<!-- seo-head -->` markers: one `BlogPosting` JSON-LD with full `datePublished` and `dateModified`. `builder/gen_sitemap.py` takes `lastmod` from `dateModified`, so bump it when the content really changes.
