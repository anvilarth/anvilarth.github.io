/* In-place language switch for longreads: fades, swaps text via setLang, keeps the reading position.
   Without JS (or without setLang) the toggle stays a plain link to the other language page. */
(() => {
  const t = document.getElementById('lang-toggle'); if (!t) return;
  const label = {ru: 'Читать на русском', en: 'Read in English'};
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function sync() {
    const other = document.documentElement.lang === 'ru' ? 'en' : 'ru';
    t.dataset.language = other; t.hreflang = other; t.lang = other;
    t.href = location.pathname.replace(/(?:\.ru)?\.html$/, other === 'ru' ? '.ru.html' : '.html');
    t.setAttribute('aria-label', label[other]); t.title = label[other];
    const nav = document.documentElement.lang === 'ru' ? ['Проекты', 'Блог'] : ['Projects', 'Blog'];
    document.querySelectorAll('.post-nav .nav-links>a:not(.lang-toggle)').forEach((a, i) => { if (nav[i]) a.textContent = nav[i]; });
  }
  function contents(lang) {  // the phone contents list is built at build time in the page's language
    const box = document.querySelector('.post-contents'); if (!box) return;
    const title = lang === 'ru' ? 'В статье' : 'In this article';
    box.setAttribute('aria-label', title);
    const p = box.querySelector('.post-contents-title'); if (p) p.textContent = title;
    box.querySelectorAll('a[href^="#"]').forEach(a => {
      const h = document.getElementById(a.getAttribute('href').slice(1)); if (!h) return;
      const c = h.cloneNode(true); c.querySelectorAll('.anchor, [aria-hidden="true"]').forEach(x => x.remove());
      a.textContent = c.textContent.trim();
    });
  }
  function anchor() {
    const navBottom = document.querySelector('.post-nav').getBoundingClientRect().bottom;
    for (const el of document.querySelectorAll('header h1, #article h2, #article h3, #article p, #article li, #article figure, #article .equation')) {
      const r = el.getBoundingClientRect();
      if (r.bottom > navBottom + 8 && r.height > 0) return {el, top: r.top};
    }
  }
  t.addEventListener('click', e => {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button || typeof setLang !== 'function') return;
    e.preventDefault();
    const to = t.dataset.language, a = anchor(), root = document.documentElement;
    const swap = () => {
      setLang(to);
      contents(to);
      if (a) { const prev = root.style.scrollBehavior; root.style.scrollBehavior = 'auto';
        window.scrollBy(0, a.el.getBoundingClientRect().top - a.top); root.style.scrollBehavior = prev; }
      try { history.replaceState(null, '', t.href); } catch (_) {}
      sync();
      requestAnimationFrame(() => root.classList.remove('lang-swap'));
    };
    if (reduce) return swap();
    root.classList.add('lang-swap'); setTimeout(swap, 160);
  });
  sync();
})();
