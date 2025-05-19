import logging
import allure
from playwright.sync_api import Page

class ImageVerifier:
    def __init__(self, page: Page):
        self.page = page

    def verify_image(self, selector: str, expected_path: str, max_images: int = 2) -> bool:
        """
        Verifies if an image with the expected `src` is present among the first `max_images`.

        Args:
            selector (str): The CSS selector to locate the images.
            expected_path (str): The expected substring in the `src` attribute of the image.
            max_images (int): How many images (from the top) to check.

        Returns:
            bool: True if an image with the expected `src` is found, False otherwise.
        """
        try:
            self.page.wait_for_selector(selector, timeout=5000)
            images = self.page.locator(selector).element_handles()
            found_srcs = []
            for img in images[:max_images]:
                src = img.get_attribute("src")
                found_srcs.append(src)
                if src and expected_path in src:
                    logging.info(f"✅ Found matching image with src: {src}")
                    allure.attach(f"Found srcs:\n" + "\n".join([str(s) for s in found_srcs]), name="Checked Image Sources", attachment_type=allure.attachment_type.TEXT)
                    return True
            logging.warning(f"⚠️ No image with the expected path '{expected_path}' was found in the first {max_images} images.")
            allure.attach(f"Checked srcs:\n" + "\n".join([str(s) for s in found_srcs]), name="Checked Image Sources", attachment_type=allure.attachment_type.TEXT)
            return False
        except Exception as e:
            logging.error(f"❌ Could not verify personalized image: {e}")
            allure.attach(f"❌ Could not verify personalized image: {e}", name="Image Verification Error", attachment_type=allure.attachment_type.TEXT)
            return False