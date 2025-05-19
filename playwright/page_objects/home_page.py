from playwright.sync_api import Page

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://example.com"  # Replace with the actual home page URL

    def navigate(self):
        self.page.goto(self.url)

    def accept_cookies(self):
        try:
            self.page.locator("cmm-cookie-banner").wait_for()
            self.page.locator("cmm-cookie-banner >> wb7-button.button--accept-all").click()
        except Exception as e:
            print(f"Error accepting cookies: {e}")

    def get_title(self):
        return self.page.title()

    def is_element_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)