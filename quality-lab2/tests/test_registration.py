from __future__ import annotations

from uuid import uuid4

import pytest
from playwright.async_api import Page, expect

from pages.catalog_page import BASE_URL


@pytest.mark.asyncio(loop_scope="session")
async def test_register_new_user(page: Page) -> None:
    user_name = "Playwright QA"
    email = f"playwright_{uuid4().hex[:12]}@example.com"

    await page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)
    await page.locator('a[href="/login"]').click()

    await expect(page.get_by_role("heading", name="New User Signup!", exact=False)).to_be_visible()
    await page.locator('input[data-qa="signup-name"]').fill(user_name)
    await page.locator('input[data-qa="signup-email"]').fill(email)
    await page.locator('button[data-qa="signup-button"]').click()

    await expect(page.get_by_text("ENTER ACCOUNT INFORMATION", exact=False)).to_be_visible(timeout=15000)

    # Account information and Address information
    await page.locator("#id_gender1").check()
    await page.locator('input[data-qa="password"]').fill("QaTest!2026Password")
    await page.locator('select[data-qa="days"]').select_option("10")
    await page.locator('select[data-qa="months"]').select_option("5")
    await page.locator('select[data-qa="years"]').select_option("1995")
    await page.locator("#newsletter").check()
    await page.locator("#optin").check()
    await page.locator('input[data-qa="first_name"]').fill("Playwright")
    await page.locator('input[data-qa="last_name"]').fill("Student")
    await page.locator('input[data-qa="company"]').fill("Quality Management Lab")
    await page.locator('input[data-qa="address"]').fill("123 Test Street")
    await page.locator('input[data-qa="address2"]').fill("Apartment 4")
    await page.locator('select[data-qa="country"]').select_option(
        label="United States"
    )
    await page.locator('input[data-qa="state"]').fill("California")
    await page.locator('input[data-qa="city"]').fill("San Francisco")
    await page.locator('input[data-qa="zipcode"]').fill("94105")
    await page.locator('input[data-qa="mobile_number"]').fill("4155550136")

    await page.locator('button[data-qa="create-account"]').click()
    await expect(
        page.get_by_text("ACCOUNT CREATED!", exact=False)
    ).to_be_visible(timeout=20000)

    await page.locator('a[data-qa="continue-button"]').click()
    await expect(page.get_by_text("Logged in as", exact=False)).to_be_visible(
        timeout=15000
    )

    await page.locator('a[href="/delete_account"]').click()
    await expect(
        page.get_by_text("ACCOUNT DELETED!", exact=False)
    ).to_be_visible(timeout=15000)
    await page.locator('a[data-qa="continue-button"]').click()
