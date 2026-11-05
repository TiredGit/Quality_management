import os

import pytest
from playwright.sync_api import Browser, sync_playwright


@pytest.fixture(scope="session")
def browser() -> Browser:
    browser_name = os.getenv("PW_BROWSER", "chromium")

    with sync_playwright() as playwright:
        browser_type = getattr(playwright, browser_name)
        browser_instance = browser_type.launch(headless=True)

        yield browser_instance

        browser_instance.close()


@pytest.fixture
def page(browser: Browser):
    context = browser.new_context(viewport={"width": 1365, "height": 900})

    page_instance = context.new_page()

    yield page_instance

    context.close()


@pytest.fixture
def base_url() -> str:
    return os.getenv(
        "BASE_URL",
        "http://127.0.0.1:8000",
    )
