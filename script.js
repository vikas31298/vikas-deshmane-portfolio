// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
navToggle.addEventListener('click', () => {
  const open = navLinks.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(open));
});
navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  navLinks.classList.remove('open');
  navToggle.setAttribute('aria-expanded', 'false');
}));

// Reveal on scroll
const revealEls = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.05, rootMargin: '0px 0px -5% 0px' });
revealEls.forEach(el => revealObserver.observe(el));
// Fallback: reveal anything in the viewport on scroll/resize in case the observer misses it
const revealFallback = () => {
  const vh = window.innerHeight;
  document.querySelectorAll('.reveal:not(.is-visible)').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.top < vh && r.bottom > 0) el.classList.add('is-visible');
  });
};
window.addEventListener('scroll', revealFallback, { passive: true });
window.addEventListener('resize', revealFallback);
window.addEventListener('load', revealFallback);

// Animated counters in hero card
const counters = document.querySelectorAll('.stat__num[data-count]');
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const target = parseFloat(el.dataset.count);
    const decimals = parseInt(el.dataset.decimals || '0', 10);
    const suffix = el.dataset.suffix || '';
    const duration = 1200;
    const start = performance.now();
    const tick = (now) => {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = (target * eased).toFixed(decimals) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    counterObserver.unobserve(el);
  });
}, { threshold: 0.5 });
counters.forEach(c => counterObserver.observe(c));

// Active nav link highlighting
const sections = [...document.querySelectorAll('section[id]')];
const navAnchors = [...navLinks.querySelectorAll('a')];
const activeObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navAnchors.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + entry.target.id));
    }
  });
}, { rootMargin: '-40% 0px -55% 0px' });
sections.forEach(s => activeObserver.observe(s));

// Footer year
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// Hide gallery tiles whose photo is missing, so empty slots never show
document.querySelectorAll('.gallery img').forEach(img => {
  img.addEventListener('error', () => { img.closest('figure').style.display = 'none'; });
});

// Product page tabs
const tabBar = document.getElementById('productTabs');
if (tabBar) {
  const buttons = [...tabBar.querySelectorAll('.tabs__btn')];
  const show = (key, scroll) => {
    if (!document.getElementById('tab-' + key)) key = 'overview';
    buttons.forEach(b => b.setAttribute('aria-selected', String(b.dataset.tab === key)));
    document.querySelectorAll('.tabpanel').forEach(p => {
      const on = p.id === 'tab-' + key;
      p.hidden = !on;
      if (on) p.querySelectorAll('.reveal').forEach(el => el.classList.add('is-visible'));
    });
    if (scroll) window.scrollTo({ top: tabBar.offsetTop - 68, behavior: 'smooth' });
  };
  buttons.forEach(b => b.addEventListener('click', () => {
    history.replaceState(null, '', '#' + b.dataset.tab);
    show(b.dataset.tab, true);
  }));
  const initial = location.hash.replace('#', '');
  if (initial) show(initial, true);
}
