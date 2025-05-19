import time
import logging
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page


class ImageVerifier:
    def __init__(self, page: Page):
        """Initializes the ImageVerifier with a WebDriver instance."""
        self.page = page

    def verify_image(self, selector: str, expected_path: str) -> bool:
        """
        Verifies if an image with the expected `src` is present.

        Args:
            selector (str): The CSS selector to locate the images.
            expected_path (str): The expected substring in the `src` attribute of the image.

        Returns:
            bool: True if an image with the expected `src` is found, False otherwise.
        """
        try:
            # Wait for the images to load
            self.page.wait_for_selector(selector, timeout=5000)

            # Locate all images matching the selector
            images = self.page.locator(selector).element_handles()

            # Check if any image's `src` contains the expected path
            for img in images:
                src = img.get_attribute("src")
                if src and expected_path in src:
                    logging.info(f"✅ Found matching image with src: {src}")
                    return True

            logging.warning(f"⚠️ No image with the expected path '{expected_path}' was found.")
            return False
        except Exception as e:
            logging.error(f"❌ Could not verify personalized image: {e}")
            return False