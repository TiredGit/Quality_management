/* ==========================================================
   theme.js — переключатель светлой / тёмной темы
   JS только ставит атрибут data-theme на <html>.
   Сами цвета меняют CSS-переменные (css/tokens.css).

   Примечание: сохранённая тема применяется ещё до отрисовки страницы
   маленьким скриптом в <head> каждого HTML-файла (чтобы не было «мигания»).
   ========================================================== */
(function () {
  'use strict';

  var root = document.documentElement;
  var themeBtn = document.querySelector('.theme-toggle');
  if (!themeBtn) return;

  var systemLight = window.matchMedia('(prefers-color-scheme: light)');

  // Какая тема сейчас реально включена:
  // выбранная вручную (data-theme) или, если не выбирали, системная
  function currentTheme() {
    return root.getAttribute('data-theme') || (systemLight.matches ? 'light' : 'dark');
  }

  // Подпись кнопки для скринридеров: что произойдёт при нажатии
  function updateThemeLabel() {
    var label = currentTheme() === 'light' ? 'Включить тёмную тему' : 'Включить светлую тему';
    themeBtn.setAttribute('aria-label', label);
  }

  themeBtn.addEventListener('click', function () {
    var next = currentTheme() === 'light' ? 'dark' : 'light';
    root.setAttribute('data-theme', next);                      // CSS-переменные меняются сами
    try { localStorage.setItem('theme', next); } catch (e) {}   // запоминаем выбор
    updateThemeLabel();
  });

  // Если пользователь не выбирал тему вручную и поменял её в системе
  systemLight.addEventListener('change', updateThemeLabel);
  updateThemeLabel();
})();