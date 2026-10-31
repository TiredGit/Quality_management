from __future__ import annotations

import pytest
from playwright.async_api import Page, expect

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


VALID_EMAIL = "test123214234234test@gmail.com"
VALID_PASSWORD = "testpassword"


@pytest.mark.asyncio(loop_scope="session")
async def test_add_products_to_cart(page: Page) -> None:
    catalog = CatalogPage(page)
    cart = CartPage(page)

    await catalog.open()
    await catalog.add_product_to_cart("Blue Top")
    await catalog.continue_shopping()
    await catalog.add_product_to_cart("Men Tshirt")
    await catalog.open_cart_from_modal()

    await expect(cart.product_rows).to_have_count(2, timeout=15000)
    blue_top = await cart.get_product_summary("Blue Top")
    men_tshirt = await cart.get_product_summary("Men Tshirt")

    assert blue_top == {
        "price": "Rs. 500",
        "quantity": "1",
        "total": "Rs. 500",
    }
    assert men_tshirt == {
        "price": "Rs. 400",
        "quantity": "1",
        "total": "Rs. 400",
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_checkout_and_place_order(page: Page) -> None:
    email, password = VALID_EMAIL, VALID_PASSWORD

    login = LoginPage(page)
    await login.open()
    await login.login(email, password)
    await expect(login.logged_in_message).to_be_visible(timeout=15000)

    catalog = CatalogPage(page)
    await catalog.open()
    await catalog.add_product_to_cart("Blue Top")
    await catalog.open_cart_from_modal()

    cart = CartPage(page)
    await expect(cart.row_for_product("Blue Top")).to_be_visible()
    await cart.proceed_to_checkout()

    await expect(
        page.get_by_role("heading", name="Address Details", exact=False)
    ).to_be_visible(timeout=15000)
    await expect(
        page.get_by_role("heading", name="Review Your Order", exact=False)
    ).to_be_visible()

    comment = page.locator('textarea[name="message"], #textarea').first
    await comment.fill("Automated test order created by Playwright.")
    await page.locator('a[href="/payment"]').click()
    await page.wait_for_url("**/payment", timeout=15000)

    await page.locator('input[name="name_on_card"]').fill("Playwright Test")
    await page.locator('input[name="card_number"]').fill("4242424242424242")
    await page.locator('input[name="cvc"]').fill("123")
    await page.locator('input[name="expiry_month"]').fill("12")
    await page.locator('input[name="expiry_year"]').fill("2030")
    await page.locator('button[data-qa="pay-button"]').click()

    await expect(
        page.get_by_text("Congratulations! Your order has been confirmed!", exact=False)
    ).to_be_visible(timeout=20000)
