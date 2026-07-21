const toggle = document.getElementById('theme-toggle');
// TODO(portfolio): add a portfolio nav link when the Blender bird animation page exists.

if (toggle) {
  const root = document.documentElement;

  const currentTheme = () =>
    root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';

  const setLabel = () => {
    const next = currentTheme() === 'dark' ? 'light' : 'dark';
    toggle.setAttribute('aria-label', `Switch to ${next} mode`);
  };

  setLabel();

  toggle.addEventListener('click', () => {
    const next = currentTheme() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (_) {}
    setLabel();
  });
}
