import os
import allure
from playwright.sync_api import Page
import logging
import allure

class ScreenshotHandler:
    def __init__(self, page: Page, screenshot_dir: str):
        self.page = page
        self.screenshot_dir = screenshot_dir

    staticmethod
    def scroll_and_capture_section(page, screenshot_path="campaign_section.png"):
        """
        Scrolls to the first [data-component-name='hp-campaigns'] element and takes a screenshot of the visible area.
        """

        with allure.step("📜 Scrolling to [data-component-name='hp-campaigns'] and capturing screenshot"):
            try:
                logging.info("🔍 Looking for [data-component-name='hp-campaigns'] element...")
                page.wait_for_selector("[data-component-name='hp-campaigns']", timeout=5000)
                elements = page.locator("[data-component-name='hp-campaigns']")
                count = elements.count()
                logging.info(f"Found {count} [data-component-name='hp-campaigns'] elements.")
                if count > 0:
                    elements.first.scroll_into_view_if_needed()
                    page.wait_for_timeout(2000)
                    logging.info("✅ Scrolled to [data-component-name='hp-campaigns'].")
                    page.screenshot(path=screenshot_path, full_page=False)
                    logging.info(f"📸 Screenshot taken and saved as {screenshot_path}")
                else:
                    logging.warning("⚠️ [data-component-name='hp-campaigns'] not found.")
                    allure.attach("⚠️ [data-component-name='hp-campaigns'] not found.", name="Scroll Info", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                logging.error(f"❌ Error while scrolling to [data-component-name='hp-campaigns']: {e}")
                allure.attach(f"❌ Error: {e}", name="Scroll Error", attachment_type=allure.attachment_type.TEXT)
                
        with allure.step("✅ Screenshot captured and saved"):
                        try:
                            with open(screenshot_path, "rb") as f:
                                allure.attach(f.read(), name="Campaign Section Screenshot", attachment_type=allure.attachment_type.PNG)
                        except Exception as e:
                            logging.warning(f"Could not attach screenshot to Allure: {e}")        

    def get_language_code(self, url: str) -> str:
        if "/fr" in url:
            return "fr"
        elif "/de" in url:
            return "de"
        elif "/it" in url:
            return "it"
        elif "/nl" in url:
            return "nl"
        else:
            return ""

    def get_market_code(self, url: str) -> str:
        domain_map = {
            ".ro": "ro", ".de": "de", ".at": "at", ".pt": "pt", ".be": "be",
            ".co.uk": "co_UK", ".hu": "hu", ".es": "es", ".it": "it", ".pl": "pl",
            ".nl": "nl", ".fr": "fr", ".lu": "lu", ".dk": "dk", ".cz": "cz",
            ".ch": "ch", ".se": "se", ".sk": "sk"
        }
        for domain, code in domain_map.items():
            if domain in url:
                return code
        return "unknown"

    @staticmethod
    def capture_and_attach(page, screenshot_path="screenshot.png"):
        try:
            page.screenshot(path=screenshot_path)
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            allure.attach(f"Error capturing or attaching screenshot: {e}", name="Screenshot Error", attachment_type=allure.attachment_type.TEXT)