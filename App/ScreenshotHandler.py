import os
import allure
from playwright.sync_api import Page


class ScreenshotHandler:
    def __init__(self, page: Page, screenshot_dir: str):
        """
        Initializes the ScreenshotHandler class.

        Args:
            page (Page): The Playwright Page object.
            screenshot_dir (str): Directory to save screenshots.
        """
        self.page = page
        self.screenshot_dir = screenshot_dir

    def scroll_and_capture_screenshot(self, urls: dict, test_name: str, model_name: str, body_type: str, retries: int, test_success: bool):
        """
        Scrolls through the page, captures screenshots, and handles specific market scrolling logic.

        Args:
            urls (dict): Dictionary containing URLs.
            test_name (str): Name of the test.
            model_name (str): Name of the model.
            body_type (str): Body type of the vehicle.
            retries (int): Number of retries.
            test_success (bool): Whether the test was successful.
        """
        try:
            # Determine the status of the test
            status = "SUCCESSFUL" if test_success else "UNSUCCESSFUL"

            # Extract the market code and language code
            market_code = self.get_market_code(urls['HOME_PAGE'])
            language_code = self.get_language_code(urls['HOME_PAGE'])

            # Construct the filename
            filename = f"{market_code}-{language_code}-{test_name} {model_name} {body_type} {retries + 1} {status}.png"
            filepath = os.path.join(self.screenshot_dir, filename)

            with allure.step("📜 Scrolling to specific elements and capturing screenshot"):
                # Scroll to the main campaign element
                try:
                    element = self.page.locator("[data-component-name='hp-campaigns']")
                    element.scroll_into_view_if_needed()
                    self.page.wait_for_timeout(1000)  # Wait for 1 second
                    allure.attach("✅ Scrolled to [data-component-name='hp-campaigns'].", name="Scroll Info", attachment_type=allure.attachment_type.TEXT)
                except Exception as e:
                    allure.attach(f"❌ Error: {e}", name="Scroll Error", attachment_type=allure.attachment_type.TEXT)

                # Handle specific market scrolling logic
                try:
                    if ".fr" in urls['HOME_PAGE']:
                        hp_element = self.page.locator('body > div.root.responsivegrid.owc-content-container > div > div.responsivegrid.ng-content-root.aem-GridColumn.aem-GridColumn--default--12 > div > div:nth-child(13) > div > div.wb-grid-container > h2')
                        hp_element.scroll_into_view_if_needed()
                        self.page.wait_for_timeout(2000)  # Wait for 2 seconds
                        allure.attach("✅ Scrolled to the French market-specific element.", name="Scroll Info (FR)", attachment_type=allure.attachment_type.TEXT)

                    if ".hu" in urls['HOME_PAGE']:
                        hp_element = self.page.locator('body > div.root.responsivegrid.owc-content-container > div > div.responsivegrid.ng-content-root.aem-GridColumn.aem-GridColumn--default--12 > div > div:nth-child(11) > div > div.wb-grid-container > h2')
                        hp_element.scroll_into_view_if_needed()
                        self.page.wait_for_timeout(2000)  # Wait for 2 seconds
                        allure.attach("✅ Scrolled to the Hungarian market-specific element.", name="Scroll Info (HU)", attachment_type=allure.attachment_type.TEXT)
                except Exception as e:
                    allure.attach(f"Error: {e}", name="Market Scroll Error", attachment_type=allure.attachment_type.TEXT)

            # Capture and save the screenshot
            self.page.screenshot(path=filepath, full_page=True)
            with allure.step("✅ Screenshot captured and saved"):
                allure.attach.file(filepath, name="Final Screenshot", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            with allure.step("❌ Error capturing screenshot"):
                allure.attach(f"Error saving or attaching screenshot: {e}", name="Error", attachment_type=allure.attachment_type.TEXT)

    def get_language_code(self, url: str) -> str:
        """
        Extracts the language code from the URL.

        Args:
            url (str): The URL to extract the language code from.

        Returns:
            str: The language code.
        """
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
        """
        Extracts the market code from the URL.

        Args:
            url (str): The URL to extract the market code from.

        Returns:
            str: The market code.
        """
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
    def attach_screenshot_to_allure(screenshot_path: str):
        """
        Attaches a screenshot to the Allure report.

        Args:
            screenshot_path (str): Path to the screenshot file.
        """
        try:
            with allure.step("Attaching screenshot to Allure"):
                with open(screenshot_path, 'rb') as file:
                    allure.attach(file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            allure.attach(f"Error attaching screenshot to Allure: {e}", name="Error", attachment_type=allure.attachment_type.TEXT)