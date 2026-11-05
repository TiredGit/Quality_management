from datetime import date, timedelta

import pytest
from playwright.sync_api import Page, expect

from pages.contacts_page import ContactsPage


@pytest.mark.e2e
def test_barber_is_preselected_from_url(page: Page, base_url):
    contacts = ContactsPage(page, base_url)
    contacts.open("?barber=artem#booking")
    expect(page.locator("#booking-barber")).to_have_value("artem")


@pytest.mark.e2e
def test_booking_form_is_sent_to_api(page: Page, base_url):
    contacts = ContactsPage(page, base_url)

    contacts.open("#booking")

    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    contacts.fill_booking_form(
        name="Иван",
        phone="+7 900 000-00-00",
        service="Мужская стрижка",
        barber="artem",
        booking_date=tomorrow,
        time="12:00",
    )

    with page.expect_response(
        lambda response: (
            response.url.endswith("/api/bookings") and response.request.method == "POST"
        )
    ) as response_info:
        contacts.submit_booking()

    response = response_info.value

    assert response.status == 200

    (
        expect(page.locator(".form__status")).to_contain_text(
            "Данные формы успешно проверены сервером."
        )
    )
