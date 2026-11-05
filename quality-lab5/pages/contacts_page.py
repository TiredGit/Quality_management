from playwright.sync_api import Page

from pages.base_page import BasePage


class ContactsPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

    def open(self, query: str = ""):
        return self.open_path(f"/contacts.html{query}")

    def fill_booking_form(
        self,
        name: str,
        phone: str,
        service: str,
        barber: str,
        booking_date: str,
        time: str,
    ):
        self.page.locator("#booking-name").fill(name)
        self.page.locator("#booking-phone").fill(phone)
        self.page.locator("#booking-service").select_option(label=service)
        self.page.locator("#booking-barber").select_option(barber)
        self.page.locator("#booking-date").fill(booking_date)
        self.page.locator("#booking-time").select_option(label=time)
        self.page.locator("#booking-agree").check()

    def submit_booking(self):
        self.page.get_by_role(
            "button",
            name="Записаться",
        ).click()
