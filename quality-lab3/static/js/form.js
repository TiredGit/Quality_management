/* ==========================================================
   form.js — форма записи (только страница «Контакты»)
   ========================================================== */
(function () {
  'use strict';

  var form = document.querySelector('.booking-form');
  if (!form) return;

  var dateInput = form.querySelector('input[type="date"]');
  var barberSelect = form.querySelector('#booking-barber');
  var statusEl = form.querySelector('.form__status');

  // Нельзя выбрать дату в прошлом
  if (dateInput) {
    var now = new Date();
    var month = String(now.getMonth() + 1).padStart(2, '0');
    var day = String(now.getDate()).padStart(2, '0');
    dateInput.min = now.getFullYear() + '-' + month + '-' + day;
  }

  // Переход со страницы «Мастера» (contacts.html?barber=artem) — выбираем мастера заранее
  var wantedBarber = new URLSearchParams(window.location.search).get('barber');
  if (wantedBarber && barberSelect) {
    Array.prototype.forEach.call(barberSelect.options, function (option) {
      if (option.value === wantedBarber) barberSelect.value = wantedBarber;
    });
  }

  // Отправки на сервер нет: показываем сообщение об успехе.
  // Обязательные поля браузер проверяет сам (required) ещё до этого события.
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = form.querySelector('#booking-name').value.trim();
    statusEl.textContent = 'Спасибо, ' + name + '! Заявка принята, мы перезвоним в течение 15 минут.';
    form.reset();
  });
})();