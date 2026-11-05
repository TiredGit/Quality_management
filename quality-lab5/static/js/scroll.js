/* ==========================================================
   scroll.js — анимации при прокрутке
   1) плавное появление блоков (Intersection Observer)
   2) параллакс фона Hero (только на главной)
   3) прогресс-бар прокрутки
   Всё отключается при prefers-reduced-motion: reduce.
   ========================================================== */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  // 1. Плавное появление блоков (Intersection Observer)
  var revealEls = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window && !reduceMotion.matches) {
    var observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);          // анимация срабатывает один раз
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -5% 0px' });

    revealEls.forEach(function (el) { observer.observe(el); });
  } else {
    // нет поддержки или включено «уменьшение движения» — показываем всё сразу
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // 2. Параллакс в Hero и 3. прогресс-бар прокрутки
  var hero = document.querySelector('.hero');
  var heroBg = document.querySelector('.hero__bg');
  var progress = document.querySelector('.progress');
  var ticking = false;

  function updateOnScroll() {
    var scrollY = window.scrollY;

    // Прогресс: доля пройденной страницы от 0 до 1
    var max = document.documentElement.scrollHeight - window.innerHeight;
    if (progress) {
      progress.style.setProperty('--progress', max > 0 ? Math.min(scrollY / max, 1) : 0);
    }

    // Параллакс: фон сдвигается на 20% пройденного расстояния (медленнее контента).
    // 0.2 не должно превышать запас сверху в CSS (top: -20%), иначе появится пустая полоса.
    // На страницах без Hero (Услуги, Мастера, Контакты) параллакса нет.
    if (hero && heroBg && !reduceMotion.matches) {
      var shift = Math.min(scrollY, hero.offsetHeight) * 0.2;
      heroBg.style.setProperty('--parallax', shift + 'px');
    }

    ticking = false;
  }

  // requestAnimationFrame: обновляем не чаще, чем кадр отрисовки
  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(updateOnScroll);
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  updateOnScroll();
})();