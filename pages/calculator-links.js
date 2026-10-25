/* Share every model/hardware/video control. Query values never become HTML. */
(() => {
  const fields = [...document.querySelectorAll('select[id], input[type="range"][id]')];
  const toggles = [...document.querySelectorAll('.toggle-row[id]')];
  const status = document.getElementById('share-status');
  const fallback = document.getElementById('share-url');

  window.restoreCalculatorState = () => {
    const params = new URLSearchParams(location.search);
    if (params.has('calc') && params.get('calc') !== '1') {
      status.textContent = 'This link uses an unsupported version. Default settings are shown.';
      return;
    }
    let invalid = false;
    fields.forEach(field => {
      if (!params.has(field.id)) return;
      const value = params.get(field.id);
      let valid;
      if (field.tagName === 'SELECT') {
        valid = [...field.options].some(option => option.value === value);
      } else {
        const number = Number(value);
        const steps = (number - Number(field.min)) / Number(field.step || 1);
        valid = value.trim() !== '' && Number.isFinite(number) && number >= Number(field.min) &&
          number <= Number(field.max) && Math.abs(steps - Math.round(steps)) < 1e-8;
      }
      if (valid) field.value = value;
      else invalid = true;
      const label = document.getElementById(field.id + '-val');
      if (label) label.textContent = field.value;
    });
    toggles.forEach(row => {
      if (!params.has(row.id)) return;
      const buttons = [...row.querySelectorAll('[data-val]')];
      const selected = buttons.find(button => button.dataset.val === params.get(row.id));
      if (!selected) { invalid = true; return; }
      buttons.forEach(button => button.classList.toggle('active', button === selected));
    });
    if (invalid) status.textContent = 'Some values in this link are invalid. Defaults are used for those fields.';
  };

  document.getElementById('share-calculation').addEventListener('click', async () => {
    const url = new URL(location.href);
    url.search = '';
    url.hash = '';
    url.searchParams.set('calc', '1');
    fields.forEach(field => url.searchParams.set(field.id, field.value));
    toggles.forEach(row => url.searchParams.set(row.id, row.querySelector('.active').dataset.val));
    fallback.hidden = true;
    try {
      await navigator.clipboard.writeText(url.href);
      status.textContent = 'Link copied. It includes all current settings.';
    } catch (_) {
      fallback.value = url.href;
      fallback.hidden = false;
      fallback.focus();
      fallback.select();
      status.textContent = 'Copy the selected link to share this calculation.';
    }
  });
})();
