from __future__ import annotations

import pytest
from playwright.async_api import Page, expect

from pages.catalog_page import CatalogPage


@pytest.mark.asyncio(loop_scope="session")
async def test_search_product(page: Page) -> None:
    catalog = CatalogPage(page)
    await catalog.open()
    await catalog.search_product("Blue Top")

    await expect(catalog.searched_products_heading).to_be_visible()
    await expect(catalog.product_card("Blue Top")).to_be_visible()
