/* Shared contents navigation for published blog posts. */
(() => {
  function init() {
    const main = document.querySelector('main');
    if (!main) return;
    const headings = [...main.querySelectorAll('h2, h3')];
    if (!headings.length) return;
    const nav = document.createElement('nav');
    nav.className = 'post-toc';
    const title = document.createElement('div');
    title.className = 'post-toc-title';
    const list = document.createElement('ol');
    nav.append(title, list);
    const links = headings.map((heading, index) => {
      if (!heading.id) {
        const base = heading.dataset.i18n || `section-${index + 1}`;
        let id = base;
        let suffix = 2;
        while (document.getElementById(id)) id = `${base}-${suffix++}`;
        heading.id = id;
      }
      heading.classList.add('toc-target');
      const item = document.createElement('li');
      if (heading.tagName === 'H3') item.className = 'post-toc-sub';
      const link = document.createElement('a');
      link.href = `#${heading.id}`;
      item.append(link);
      list.append(item);
      return link;
    });
    const intro = main.querySelector('header') || main.querySelector('.subtitle') || main.querySelector('h1');
    if (intro) intro.after(nav);
    else main.prepend(nav);
    function translate() {
      const label = document.documentElement.lang === 'ru' ? 'Содержание' : 'Contents';
      title.textContent = label;
      nav.setAttribute('aria-label', label);
      links.forEach((link, i) => { link.textContent = headings[i].textContent.trim(); });
    }
    translate();
    new MutationObserver(translate).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
    let pending = false;
    let active = -1;
    function update() {
      pending = false;
      let current = 0;
      headings.forEach((heading, i) => {
        if (heading.getBoundingClientRect().top <= 120) current = i;
      });
      if (current === active) return;
      active = current;
      links.forEach((link, i) => {
        if (i === current) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
      if (matchMedia('(min-width: 1280px)').matches) {
        const item = links[current];
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
    // IDs are ready before restoring a direct section link.
    let fragment = location.hash.slice(1);
    try { fragment = decodeURIComponent(fragment); } catch { /* Ignore malformed escapes. */ }
    const target = document.getElementById(fragment);
    if (target && headings.includes(target)) target.scrollIntoView();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
