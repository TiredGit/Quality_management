from playwright.async_api import Page


BASE_URL = "https://automationexercise.com"


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        self.email_input = page.locator('input[data-qa="login-email"]')
        self.password_input = page.locator('input[data-qa="login-password"]')

        self.submit_button = page.locator('button[data-qa="login-button"]')

        self.error_message = page.locator("form p").filter(has_text="Your email or password is incorrect!")

        self.logged_in_message = page.get_by_text("Logged in as", exact=False)

    async def open(self):
        await self.page.goto(
            f"{BASE_URL}/login",
            wait_until="domcontentloaded",
            timeout=60000,
        )

        await self.email_input.wait_for(state="visible", timeout=20000)

    async def login(self, email: str, password: str):
        await self.email_input.fill(email)
        await self.password_input.fill(password)
        await self.submit_button.click()