from playwright.async_api import Locator, Page, expect

BASE_URL = "https://automationexercise.com"


class CartPage:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.product_rows = page.locator("#cart_info_table tbody tr")
        self.empty_cart_message = page.get_by_text("Cart is empty!", exact=False)

    async def open(self) -> None:
        await self.page.goto(
            f"{BASE_URL}/view_cart",
            wait_until="domcontentloaded",
            timeout=60000,
        )
        await expect(self.page).to_have_url("**/view_cart")

    def row_for_product(self, product_name: str) -> Locator:
        return self.product_rows.filter(has_text=product_name).first

    async def get_product_summary(self, product_name: str) -> dict[str, str]:
        row = self.row_for_product(product_name)
        await expect(row).to_be_visible(timeout=15000)
        return {
            "price": (await row.locator(".cart_price p").inner_text()).strip(),
            "quantity": (
                await row.locator(".cart_quantity button").inner_text()
            ).strip(),
            "total": (
                await row.locator(".cart_total p").inner_text()
            ).strip(),
        }

    async def proceed_to_checkout(self) -> None:
        checkout_link = self.page.locator("a.check_out").filter(has_text="Proceed To Checkout")
        await expect(checkout_link).to_be_visible(timeout=15000)
        await checkout_link.click()
        await self.page.wait_for_url("**/checkout", timeout=15000)
