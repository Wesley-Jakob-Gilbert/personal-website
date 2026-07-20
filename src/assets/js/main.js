const toggle = document.getElementById('theme-toggle');
// TODO(portfolio): add a portfolio nav link when the Blender bird animation page exists.

if (toggle) {
  const root = document.documentElement;
  const setLabel = () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    toggle.setAttribute('aria-label', `Switch to ${next} mode`);
  };

  setLabel();
  toggle.addEventListener('click', () => {
    const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = theme;
    localStorage.setItem('theme', theme);
    setLabel();
  });
}
