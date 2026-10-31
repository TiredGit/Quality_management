import re

import pytest
from playwright.async_api import Page, expect

from pages.login_page import LoginPage


VALID_EMAIL = "test123214234234test@gmail.com"
VALID_PASSWORD = "testpassword"


@pytest.mark.asyncio(loop_scope="session")
async def test_login_with_valid_credentials(page: Page):
    login_page = LoginPage(page)

    await login_page.open()
    await login_page.login(VALID_EMAIL, VALID_PASSWORD)

    await expect(login_page.logged_in_message).to_be_visible(timeout=15000)
    await expect(page).to_have_url(re.compile(r"https://(?:www\.)?automationexercise\.com/?$"))


@pytest.mark.asyncio(loop_scope="session")
async def test_login_with_invalid_credentials(page: Page):
    login_page = LoginPage(page)

    await login_page.open()
    await login_page.login(  "invalid_user_987654321@example.com",  "DefinitelyWrongPassword987!")

    await expect(login_page.logged_in_message).not_to_be_visible(timeout=15000)
    await expect(page).to_have_url(re.compile(r"/login/?$"))


@pytest.mark.asyncio(loop_scope="session")
async def test_login_with_empty_fields(page: Page):
    login_page = LoginPage(page)

    await login_page.open()
    await login_page.submit_button.click()

    await expect(page).to_have_url(re.compile(r"/login/?$"))

    await expect(login_page.email_input).to_be_visible()
    await expect(login_page.password_input).to_be_visible()

    await expect(login_page.email_input).to_have_value("")
    await expect(login_page.password_input).to_have_value("")