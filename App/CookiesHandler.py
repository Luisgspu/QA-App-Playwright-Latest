import logging
import allure
from playwright.sync_api import Page

class CookieHandler:
    """Handles cookie banners across different websites using Playwright."""

    def __init__(self, page):
        self.page = page

    @allure.step("Accept cookies if the cookie banner is present")
    def accept_cookies(self):
        """Handles the cookie banner and accepts cookies if present."""
        try:
            self.page.wait_for_selector("cmm-cookie-banner", timeout=10000)
            logging.info("✅ Cookie banner detected.")
            # Try a more robust selector for the accept button inside the shadow DOM
            result = self.page.locator("cmm-cookie-banner").evaluate(
                """
                banner => {
                    // Try the strict selector first
                    let btn = banner.shadowRoot.querySelector('div > div > div.cmm-cookie-banner__content > cmm-buttons-wrapper > div > div > wb7-button.button.button--accept-all.wb-button.hydrated');
                    // Fallback: try any button with 'accept' in class or text
                    if (!btn) {
                        btn = Array.from(banner.shadowRoot.querySelectorAll('button, wb7-button')).find(
                            el => el.className.includes('accept-all') || (el.textContent && el.textContent.toLowerCase().includes('accept'))
                        );
                    }
                    if (btn) {
                        btn.click();
                        return true;
                    }
                    return false;
                }
                """
            )
            if result:
                logging.info("✅ Clicked on accept cookies.")
                allure.attach("Cookie banner accepted", name="Cookie Handling", attachment_type=allure.attachment_type.TEXT)
            else:
                raise Exception("Accept button not found in cookie banner shadow DOM.")
        except Exception as ex:
            allure.attach("❌ Cookie banner not found or already accepted.", name="Cookie Acceptance Error", attachment_type=allure.attachment_type.TEXT)
            logging.error(f"❌ Failed to accept cookies: {ex}")
            pytest.fail("Failed to accept cookies.")

# Pytest Test Case Example
import pytest

@pytest.fixture
def cookie_handler(page):
    """Fixture to initialize the CookieHandler with Playwright page."""
    return CookieHandler(page)

@allure.feature("Cookie Handling")
@allure.story("Test Cookie Banner Acceptance")
def test_accept_cookies(cookie_handler):
    """Test case to verify cookie banner acceptance."""
    with allure.step("Attempt to accept cookies"):
        cookie_handler.accept_cookies()