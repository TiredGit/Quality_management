(function () {
  'use strict';

  var form = document.querySelector('.booking-form');
  if (!form) return;

  var dateInput = form.querySelector('input[type="date"]');
  var barberSelect = form.querySelector('#booking-barber');
  var statusEl = form.querySelector('.form__status');
  var submitButton = form.querySelector('button[type="submit"]');

  // Запрещаем выбирать дату в прошлом.
  if (dateInput) {
    var now = new Date();
    var month = String(now.getMonth() + 1).padStart(2, '0');
    var day = String(now.getDate()).padStart(2, '0');

    dateInput.min = now.getFullYear() + '-' + month + '-' + day;
  }

  // Предварительный выбор мастера из URL.
  var wantedBarber = new URLSearchParams(window.location.search).get('barber');

  if (wantedBarber && barberSelect) {
    Array.prototype.forEach.call(barberSelect.options, function (option) {
      if (option.value === wantedBarber) {
        barberSelect.value = wantedBarber;
      }
    });
  }

  // Отправка заявки на FastAPI.
  form.addEventListener('submit', async function (event) {
    event.preventDefault();

    var payload = {
      name: form.querySelector('#booking-name').value,
      phone: form.querySelector('#booking-phone').value,
      service: form.querySelector('#booking-service').value,
      barber: form.querySelector('#booking-barber').value,
      date: form.querySelector('#booking-date').value,
      time: form.querySelector('#booking-time').value,
      comment: form.querySelector('#booking-comment').value,
      agree: form.querySelector('#booking-agree').checked
    };

    submitButton.disabled = true;
    statusEl.textContent = 'Проверяем данные...';

    try {
      var response = await fetch('/api/bookings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      var result = await response.json();

      if (!response.ok) {
        var message = Array.isArray(result.detail)
          ? result.detail.map(function (item) {
              return item.msg;
            }).join(' ')
          : result.detail;

        throw new Error(message || 'Не удалось проверить заявку');
      }

      statusEl.textContent = result.message;
      form.reset();

    } catch (error) {
      statusEl.textContent = 'Ошибка: ' + error.message;

    } finally {
      submitButton.disabled = false;
    }
  });
})();
