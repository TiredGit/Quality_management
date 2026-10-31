from __future__ import annotations

import re
import pytest
from playwright.async_api import Page, expect

from pages.login_page import LoginPage


VALID_EMAIL = "test123214234234test@gmail.com"
VALID_PASSWORD = "testpassword"


@pytest.mark.asyncio(loop_scope="session")
async def test_logout_user(page: Page) -> None:
    email, password = VALID_EMAIL, VALID_PASSWORD

    login = LoginPage(page)
    await login.open()
    await login.login(email, password)
    await expect(login.logged_in_message).to_be_visible(timeout=15000)

    await page.locator('a[href="/logout"]').click()
    await expect(page).to_have_url(re.compile(r"/login/?$"))
    await expect(
        page.get_by_role("heading", name="Login to your account", exact=False)
    ).to_be_visible()
