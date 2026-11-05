import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
@pytest.mark.parametrize(
    ("path", "heading"),
    [
        ("/", "Лучшая стрижка в центре города"),
        ("/services.html", "Услуги и цены"),
        ("/barbers.html", "Наши мастера"),
        ("/contacts.html", "Контакты"),
    ],
)
def test_site_pages_open(page: Page, base_url, path, heading):
    page.goto(f"{base_url}{path}")

    expect(page.locator("h1")).to_contain_text(heading)


@pytest.mark.e2e
def test_logo_image_is_loaded(page: Page, base_url):
    page.goto(base_url)

    logo = page.locator(".logo__img")

    expect(logo).to_be_visible()

    is_loaded = logo.evaluate("(image) => image.complete && image.naturalWidth > 0")

    assert is_loaded
