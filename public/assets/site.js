// The entire site and language navigation work without JavaScript.
// Keep the matching section when switching language from an anchored homepage.
const languageLink = document.querySelector('[data-language]');
if (languageLink && ['#services', '#approach', '#about'].includes(location.hash)) {
  languageLink.hash = location.hash;
}
window.addEventListener('hashchange', () => {
  if (languageLink) languageLink.hash = ['#services', '#approach', '#about'].includes(location.hash) ? location.hash : '';
});
const copyButton = document.querySelector('[data-copy]');
if (copyButton) {
  copyButton.hidden = false;
  copyButton.addEventListener('click', async () => {
    const status = document.querySelector('.copy-status');
    try {
      if (!navigator.clipboard) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(location.href);
      status.textContent = copyButton.dataset.success;
    } catch {
      status.textContent = copyButton.dataset.failure;
    }
  });
}
