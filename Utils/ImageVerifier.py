import logging
import allure
from playwright.sync_api import Page
import pytest


class ImageVerifier:
    def __init__(self, page: Page):
        self.page = page

    def verify_image(self, selector: str, expected_path: str, test_name: str = None) -> bool:
        """
        Verifies if an image with the expected `src` is present among all images matching the selector.
        """
        try:
            self.page.wait_for_selector(selector, timeout=6000)
            images = self.page.locator(selector)
            img_count = images.count()
            logging.info(f"Found {img_count} <img> elements inside {selector}.")

            srcs = []
            found_match = False
            for i in range(img_count):
                src = images.nth(i).get_attribute("src")
                srcs.append(src)
                logging.info(f"Image {i+1} src: {src}")
                if src and expected_path in src:
                    found_match = True

            logging.info("All found image srcs:\n" + "\n".join([str(s) for s in srcs]))
            allure.attach(
                "All found image srcs:\n" + "\n".join([str(s) for s in srcs]),
                name="Checked Image Sources",
                attachment_type=allure.attachment_type.TEXT
            )
            if found_match:
                # Find the first matching src
                matching_src = next((src for src in srcs if src and expected_path in src), None)
                with allure.step(f"✅ Personalized image with expected src '{expected_path}' was applied correctly."):
                    if matching_src:
                        allure.attach(
                            f"Matching image src:\n{matching_src}",
                            name="Matching Image Src",
                            attachment_type=allure.attachment_type.TEXT
                        )
                    return True
            else:
                with allure.step(f"❌ Image not found in the specified selector. Expected src: {expected_path}"):
                    logging.warning(f"❌ Image not found in the specified selector. Expected src: {expected_path}")
                    message = f"❌ Test '{test_name}' failed due to image verification error."
                    pytest.fail(message)
                    return False
        except Exception as e:
            message = f"❌ Test '{test_name}' failed due to image verification error: {e}" if test_name else f"❌ Image verification error: {e}"
            logging.error(message)
            pytest.fail(message)
            return False