/* Shared contents navigation, heading anchors and equation overflow for published blog posts. */
(() => {
  const RU = () => document.documentElement.lang === 'ru';
  function label(heading) {
    const copy = heading.cloneNode(true);
    copy.querySelectorAll('.anchor').forEach((a) => a.remove());
    return copy.textContent.trim();
  }
  function ensureId(heading, index) {
    if (heading.id) return;
    const base = heading.dataset.i18n || `section-${index + 1}`;
    let id = base;
    let suffix = 2;
    while (document.getElementById(id)) id = `${base}-${suffix++}`;
    heading.id = id;
  }
  function anchors(main) {
    main.querySelectorAll('h2, h3').forEach((heading) => {
      if (!heading.id || heading.closest('.src, nav, .post-contents') || heading.querySelector('.anchor')) return;
      const link = document.createElement('a');
      link.className = 'anchor';
      link.href = `#${heading.id}`;
      link.textContent = '#';
      link.setAttribute('aria-label', RU() ? 'Ссылка на этот раздел' : 'Link to this section');
      link.addEventListener('click', () => {
        const url = location.origin + location.pathname + '#' + heading.id;
        if (navigator.clipboard) navigator.clipboard.writeText(url).then(() => {
          link.classList.add('is-copied');
          link.textContent = '✓';
          setTimeout(() => { link.classList.remove('is-copied'); link.textContent = '#'; }, 1200);
        }, () => {});
      });
      heading.append(link);
    });
  }
  function equations() {
    const blocks = [...document.querySelectorAll('.equation')];
    if (!blocks.length) return;
    function measure() {
      blocks.forEach((block) => {
        const overflow = block.scrollWidth > block.clientWidth + 1;
        block.classList.toggle('is-overflow', overflow);
        block.classList.toggle('is-at-end', overflow && block.scrollLeft + block.clientWidth >= block.scrollWidth - 1);
      });
    }
    blocks.forEach((block) => block.addEventListener('scroll', () => {
      block.classList.toggle('is-at-end', block.scrollLeft + block.clientWidth >= block.scrollWidth - 1);
    }, { passive: true }));
    addEventListener('resize', measure);
    addEventListener('load', measure);
    measure();
    // KaTeX renders after this script; re-measure once the formulas exist.
    setTimeout(measure, 0);
    setTimeout(measure, 300);
  }
  function init() {
    const main = document.querySelector('main') || document.querySelector('.c');
    if (!main) return;
    const chapters = [...main.querySelectorAll('h2, .src h3')].filter((h) => !h.closest('nav, .post-contents'));
    if (!chapters.length) return;
    chapters.forEach(ensureId);
    const nav = document.createElement('nav');
    nav.className = 'post-toc';
    const title = document.createElement('div');
    title.className = 'post-toc-title';
    const list = document.createElement('ol');
    nav.append(title, list);
    // Chapters and sources are always listed; a chapter's h3 subsections show while it is current.
    const entries = chapters.map((heading, index) => {
      heading.classList.add('toc-target');
      const item = document.createElement('li');
      const link = document.createElement('a');
      link.href = `#${heading.id}`;
      item.append(link);
      list.append(item);
      const subs = [];
      if (heading.tagName === 'H2') {
        const next = chapters[index + 1];
        const section = heading.closest('section') || main;
        for (const h3 of section.querySelectorAll('h3')) {
          if (h3.closest('.src, nav, .post-contents, .technical-note, aside')) continue;
          if (!(heading.compareDocumentPosition(h3) & Node.DOCUMENT_POSITION_FOLLOWING)) continue;
          if (next && (next.compareDocumentPosition(h3) & Node.DOCUMENT_POSITION_FOLLOWING)) continue;
          subs.push(h3);
        }
      }
      let subList = null;
      const subLinks = subs.map((h3, i) => {
        if (!h3.id) ensureId(h3, i);
        h3.classList.add('toc-target');
        if (!subList) { subList = document.createElement('ol'); subList.className = 'post-toc-sub'; item.append(subList); }
        const subItem = document.createElement('li');
        const subLink = document.createElement('a');
        subLink.href = `#${h3.id}`;
        subItem.append(subLink);
        subList.append(subItem);
        return subLink;
      });
      return { heading, item, link, subs, subLinks };
    });
    const intro = main.querySelector('header') || main.querySelector('.subtitle') || main.querySelector('h1');
    if (intro) intro.after(nav);
    else main.prepend(nav);
    function translate() {
      const text = RU() ? 'Содержание' : 'Contents';
      title.textContent = text;
      nav.setAttribute('aria-label', text);
      entries.forEach((entry) => {
        entry.link.textContent = label(entry.heading);
        entry.subLinks.forEach((link, i) => { link.textContent = label(entry.subs[i]); });
      });
    }
    translate();
    new MutationObserver(translate).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
    anchors(main);
    // Article scripts that swap heading text (data-i18n) drop the anchors; put them back.
    let anchorsPending = false;
    new MutationObserver(() => {
      if (anchorsPending) return;
      anchorsPending = true;
      requestAnimationFrame(() => { anchorsPending = false; anchors(main); });
    }).observe(main, { childList: true, subtree: true });
    let pending = false;
    let active = -1;
    let activeSub = null;
    function update() {
      pending = false;
      let current = 0;
      entries.forEach((entry, i) => {
        if (entry.heading.getBoundingClientRect().top <= 120) current = i;
      });
      const entry = entries[current];
      let sub = null;
      entry.subs.forEach((h3, i) => {
        if (h3.getBoundingClientRect().top <= 120) sub = i;
      });
      if (current === active && sub === activeSub) return;
      active = current;
      activeSub = sub;
      entries.forEach((e, i) => {
        e.item.classList.toggle('is-current', i === current);
        if (i === current) e.link.setAttribute('aria-current', 'location');
        else e.link.removeAttribute('aria-current');
        e.subLinks.forEach((link, j) => {
          if (i === current && j === sub) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      });
      if (matchMedia('(min-width: 1280px)').matches) {
        const item = sub === null ? entry.link : entry.subLinks[sub];
        const top = item.offsetTop;
        if (top < nav.scrollTop || top + item.offsetHeight > nav.scrollTop + nav.clientHeight) {
          nav.scrollTop = Math.max(0, top - nav.clientHeight / 2);
        }
      }
    }
    addEventListener('scroll', () => {
      if (!pending) { pending = true; requestAnimationFrame(update); }
    }, { passive: true });
    addEventListener('resize', update);
    update();
    equations();
    // IDs are ready before restoring a direct section link.
    let fragment = location.hash.slice(1);
    try { fragment = decodeURIComponent(fragment); } catch { /* Ignore malformed escapes. */ }
    const target = document.getElementById(fragment);
    if (target && target.classList.contains('toc-target')) target.scrollIntoView();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
