/* ==========================================================
   menu.js — мобильное меню-бургер
   Открытие/закрытие, блокировка прокрутки, aria-expanded, Esc.
   ========================================================== */
(function () {
  'use strict';

  var burger = document.querySelector('.burger');
  var nav = document.getElementById('site-nav');
  var closeBtn = document.querySelector('.nav__close');
  if (!burger || !nav || !closeBtn) return;

  var desktop = window.matchMedia('(min-width: 768px)');

  function setMenu(open, returnFocus) {
    nav.classList.toggle('is-open', open);                  // плавное открытие через CSS
    document.body.classList.toggle('no-scroll', open);      // блокируем прокрутку страницы
    burger.setAttribute('aria-expanded', String(open));     // состояние для доступности

    if (open) {
      closeBtn.focus();
    } else if (returnFocus) {
      burger.focus();
    }
  }

  burger.addEventListener('click', function () { setMenu(true); });
  closeBtn.addEventListener('click', function () { setMenu(false, true); });

  // Закрываем меню при клике на любую ссылку внутри него
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) setMenu(false);
  });

  // Закрываем по клавише Esc
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) setMenu(false, true);
  });

  // Если окно растянули до планшета/десктопа, снимаем блокировку прокрутки
  desktop.addEventListener('change', function (e) {
    if (e.matches) setMenu(false);
  });
})();