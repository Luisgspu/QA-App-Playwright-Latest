from playwright.sync_api import Page
import logging
import os

class ScreenshotHandler:
    def __init__(self, page: Page, screenshot_dir: str):
        self.page = page
        self.screenshot_dir = screenshot_dir
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def take_screenshot(self, name: str):
        screenshot_path = os.path.join(self.screenshot_dir, f"{name}.png")
        try:
            self.page.screenshot(path=screenshot_path)
            logging.info(f"Screenshot saved to {screenshot_path}")
        except Exception as e:
            logging.error(f"Error taking screenshot: {e}")

    def take_full_page_screenshot(self, name: str):
        screenshot_path = os.path.join(self.screenshot_dir, f"{name}_full.png")
        try:
            self.page.screenshot(path=screenshot_path, full_page=True)
            logging.info(f"Full page screenshot saved to {screenshot_path}")
        except Exception as e:
            logging.error(f"Error taking full page screenshot: {e}")