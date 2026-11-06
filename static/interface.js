/* Progressive enhancement only: all links and forms remain native. */
(() => {
  const menu = document.querySelector('.menu-alternar');
  const navigation = document.querySelector('.navegacao');
  if (menu && navigation) {
    menu.hidden = false;
    const closeMenu = () => {
      menu.setAttribute('aria-expanded', 'false');
      navigation.classList.remove('aberta');
    };
    menu.addEventListener('click', () => {
      const opened = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(opened));
      navigation.classList.toggle('aberta', opened);
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
        closeMenu();
        menu.focus();
      }
    });
    navigation.querySelectorAll('a').forEach(link => {
      const path = new URL(link.href).pathname;
      if (location.pathname === path || location.pathname.startsWith(path + '/')) {
        link.setAttribute('aria-current', 'page');
      }
    });
    const mobile = matchMedia('(max-width: 760px)');
    const adapt = () => {
      closeMenu();
      navigation.classList.toggle('menu-recolhivel', mobile.matches);
    };
    mobile.addEventListener('change', adapt);
    adapt();
  }
})();
