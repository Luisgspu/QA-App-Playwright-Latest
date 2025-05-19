import logging
from playwright.sync_api import sync_playwright
from ScreenshotHandler import ScreenshotHandler  # Assuming this is in another file
from playwright.sync_api import Page


logging.basicConfig(level=logging.INFO, format="%(message)s")

def test_shadow_dom_click():
    url = "https://www.mercedes-benz.de"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            screen={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        page.goto(url)
        page.wait_for_load_state("load")

        shadow_host_selector = "cmm-cookie-banner"
        button_selector = "wb7-button.button--accept-all"

        logging.info(f"🔍 Waiting for shadow host: {shadow_host_selector}")
        try:
            page.wait_for_selector(shadow_host_selector, timeout=10000, state="attached")
            page.wait_for_timeout(2000)  # Wait for 2 seconds to ensure the shadow DOM is ready
            is_hidden = page.locator(shadow_host_selector).evaluate(
                "banner => window.getComputedStyle(banner).display === 'none' || window.getComputedStyle(banner).visibility === 'hidden'"
            )
            logging.info(f"Banner hidden: {is_hidden}")

            logging.info("✅ Shadow host found.")
        except Exception as ex:
            logging.error(f"❌ Shadow host not found: {ex}")
            browser.close()
            return

        logging.info("🔍 Trying to expand shadow root and find the button...")
        # Print all elements in the shadow root for debugging
        buttons = page.locator(shadow_host_selector).evaluate(
             "banner => Array.from(banner.shadowRoot.querySelectorAll('button, wb7-button')).map(e => e.outerHTML)"
        )

        # Try to click any button with 'accept' in text
        found = page.locator(shadow_host_selector).evaluate(
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
        if found:
            logging.info("✅ Accept button inside shadow root found and clicked.")
        else:
            logging.warning("⚠️ Accept button inside shadow root not found.")
        
            
        """
        # Capture screenshot after scrolling to the main campaign element
        try:
            logging.info("🔍 Looking for [data-component-name='hp-campaigns'] element...")
            element = page.locator("[data-component-name='hp-campaigns']")
            element.wait_for(state="attached", timeout=5000)
            count = element.count()
            logging.info(f"Found {count} [data-component-name='hp-campaigns'] elements.")
            if count > 0:
                element.first.scroll_into_view_if_needed()
                page.wait_for_timeout(2000)
                logging.info("✅ Scrolled to [data-component-name='hp-campaigns'].")
                screenshot_path = "campaign_section.png"
                page.screenshot(path=screenshot_path, full_page=False)
                logging.info(f"📸 Screenshot taken and saved as {screenshot_path}")
            else:
                logging.warning("⚠️ [data-component-name='hp-campaigns'] not found.")
        except Exception as e:
            logging.error(f"❌ Error while scrolling to [data-component-name='hp-campaigns']: {e}")
        """        
        screenshot_path = "campaign_section.png"
        
        try:
            ScreenshotHandler.scroll_and_capture_section(page, screenshot_path)
            logging.info(f"✅ Screenshot saved and attached at: {screenshot_path}")
        except Exception as e:
            logging.error(f"❌ Failed to capture or attach screenshot: {e}")

        browser.close()
        
if __name__ == "__main__":
    test_shadow_dom_click()