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
