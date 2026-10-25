/* Static language URLs, with compatibility for previously shared #ru links. */
(() => {
  const url = new URL(location.href);
  const legacy = ['#ru', '#en'].includes(url.hash) ? url.hash.slice(1) : url.searchParams.get('lang');
  const current = document.documentElement.lang;
  function destination(lang, input) {
    const result = new URL(input);
    result.pathname = result.pathname.replace(/(?:\.ru)?\.html$/, lang === 'ru' ? '.ru.html' : '.html');
    result.searchParams.delete('lang');
    if (['#ru', '#en'].includes(result.hash)) result.hash = '';
    return result;
  }
  if (legacy === 'ru' || legacy === 'en') {
    const target = destination(legacy, url);
    if (legacy !== current) location.replace(target.href);
    else history.replaceState(null, '', target.href);
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('a[data-language]');
    if (!link) return;
    // Update the real link so modified clicks also preserve the current section.
    link.href = destination(link.dataset.language, location.href).href;
  });
})();
