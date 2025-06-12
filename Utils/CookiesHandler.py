import logging
import allure
import pytest
from playwright.sync_api import Page, TimeoutError
import time

class CookieHandler:
    """Handles cookie banners across different websites using Playwright."""

    def __init__(self, page):
        self.page = page

    @allure.step("Accept cookies if the cookie banner is present")
    def accept_cookies(self):
        """Handles the cookie banner and accepts cookies if present."""
        shadow_host_selector = "cmm-cookie-banner"
        try:
            self.page.wait_for_selector(shadow_host_selector, timeout=10000, state="attached")
            self.page.wait_for_timeout(3000)  # Wait for 2 seconds to ensure the shadow DOM is ready
            logging.info("✅ Cookie banner detected (attached).")
            # Optional: log if hidden
            is_hidden = self.page.locator(shadow_host_selector).evaluate(
                "banner => window.getComputedStyle(banner).display === 'none' || window.getComputedStyle(banner).visibility === 'hidden'"
            )
            logging.info(f"Banner hidden: {is_hidden}")

            # Print all buttons for debug
            buttons = self.page.locator(shadow_host_selector).evaluate(
                "banner => Array.from(banner.shadowRoot.querySelectorAll('button, wb7-button')).map(e => e.outerHTML)"
            )
            logging.info(f"Buttons in the shadow root:\n{buttons}")

            # Try to click the accept-all button using data-test attribute
            result = self.page.locator(shadow_host_selector).evaluate(
                """
                banner => {
                    const btn = banner.shadowRoot.querySelector('[data-test="handle-accept-all-button"]');
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
            error_screenshot = f"cookie_error_{int(time.time())}.png"
            try:
                self.page.screenshot(path=error_screenshot, full_page=True)
                allure.attach.file(error_screenshot, name="Cookie Error Screenshot", attachment_type=allure.attachment_type.PNG)
            except Exception as screenshot_ex:
                logging.error(f"❌ Failed to take screenshot: {screenshot_ex}")
                allure.attach(f"Failed to take screenshot: {screenshot_ex}", name="Screenshot Error", attachment_type=allure.attachment_type.TEXT)
            logging.error(f"❌ Failed to accept cookies: {ex}")
            pytest.fail("Failed to accept cookies.")
