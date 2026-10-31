from playwright.async_api import Locator, Page, expect

BASE_URL = "https://automationexercise.com"


class CatalogPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.searched_products_heading = page.get_by_role("heading", name="Searched Products", exact=False)
        self.product_cards = page.locator(".product-image-wrapper")
        self.added_to_cart_modal = page.locator("#cartModal")

    async def open(self) -> None:
        await self.page.goto(
            f"{BASE_URL}/products",
            wait_until="domcontentloaded",
            timeout=60000,
        )
        await expect(
            self.page.get_by_role("heading", name="All Products", exact=False)).to_be_visible(timeout=20000)

    def product_card(self, product_name: str) -> Locator:
        return self.product_cards.filter(has=self.page.get_by_text(product_name, exact=True)).first

    async def search_product(self, product_name: str) -> None:
        await self.search_input.fill(product_name)
        await self.search_button.click()
        await expect(self.searched_products_heading).to_be_visible(timeout=15000)
        await expect(self.product_card(product_name)).to_be_visible(timeout=15000)

    async def add_product_to_cart(self, product_name: str) -> None:
        card = self.product_card(product_name)
        await expect(card).to_be_visible(timeout=15000)
        await card.hover()

        add_to_cart_link = card.locator("a.add-to-cart").last
        await add_to_cart_link.click(timeout=15000)
        await expect(self.added_to_cart_modal).to_be_visible(timeout=15000)

    async def continue_shopping(self) -> None:
        await self.added_to_cart_modal.get_by_role("button", name="Continue Shopping").click()
        await expect(self.added_to_cart_modal).to_be_hidden(timeout=10000)

    async def open_cart_from_modal(self) -> None:
        await self.added_to_cart_modal.locator('a[href="/view_cart"]').click()
        await self.page.wait_for_url("**/view_cart", timeout=15000)
