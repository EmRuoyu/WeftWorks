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

// Native <details> keeps the mobile menu usable without JavaScript.
const menu = document.querySelector('.mobile-menu');
if (menu) {
  menu.addEventListener('click', (event) => {
    if (event.target.closest('a')) menu.open = false;
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu.open) {
      menu.open = false;
      menu.querySelector('summary').focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!menu.contains(event.target)) menu.open = false;
  });
}

// Animate once on entry. Content is never hidden while waiting for JavaScript.
const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
const activeAnimations = new Set();
let entranceObserver;
if (!motionPreference.matches && 'IntersectionObserver' in window && 'animate' in Element.prototype) {
  entranceObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entranceObserver.unobserve(entry.target);
      const animation = entry.target.animate(
        [{ opacity: 0, transform: 'translateY(16px)' }, { opacity: 1, transform: 'translateY(0)' }],
        { duration: 580, easing: 'cubic-bezier(.2,.65,.3,1)' }
      );
      activeAnimations.add(animation);
      animation.finished.then(() => activeAnimations.delete(animation)).catch(() => activeAnimations.delete(animation));
    }
  }, { threshold: 0.08 });
  document.querySelectorAll('.service-card, .case-card, .about-principle, .contact-panel, .fde-step, .step').forEach(el => entranceObserver.observe(el));
}
motionPreference.addEventListener('change', (event) => {
  if (!event.matches) return;
  entranceObserver?.disconnect();
  activeAnimations.forEach(animation => animation.cancel());
  activeAnimations.clear();
});
