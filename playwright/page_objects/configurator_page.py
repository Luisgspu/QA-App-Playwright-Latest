from playwright.sync_api import Page

class ConfiguratorPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://example.com/configurator"  # Replace with the actual configurator URL

    def navigate(self):
        self.page.goto(self.url)

    def select_option(self, option_selector: str):
        self.page.click(option_selector)

    def get_selected_option(self, option_selector: str) -> str:
        return self.page.locator(option_selector).inner_text()

    def submit(self):
        self.page.click("button[type='submit']")  # Adjust the selector as needed

    def is_loaded(self) -> bool:
        return self.page.is_visible("selector-for-loaded-element")  # Replace with an actual selector to check if the page is loaded