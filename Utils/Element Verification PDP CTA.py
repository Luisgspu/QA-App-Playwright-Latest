import logging
from playwright.sync_api import sync_playwright
from ScreenshotHandler import ScreenshotHandler  # Assuming this is in another file
from playwright.sync_api import Page
from ImageVerifier import ImageVerifier  # Assuming this is in another file
from XHRResponseCapturer import XHRResponseCapturer  # Assuming this is the correct import for your XHR capturer
import json
from ConfigStarted import ConfiguratorStarted  # Playwright version
from ConfigCompleted import ConfiguratorCompleted  # Playwright version


logging.basicConfig(level=logging.INFO, format="%(message)s")

def test_shadow_dom_click():
    url = "https://www.mercedes-benz.de"
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--start-maximized",
                "--disable-gpu",
                "--enable-webgl",
                "--incognito",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--window-size=1920,1080",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--disable-extensions",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "--disable-features=IsolateOrigins,site-per-process",
                "--blink-settings=imagesEnabled=true"
            ],
        )
        context = browser.new_context(
           
            viewport={"width": 1920, "height": 1080},
            screen={"width": 1920, "height": 1080}
        )
        
        

        # Open a Home Page
        page = context.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")
        logging.info(f"✅ Home Page loaded: {url}")
        
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
        
        page.goto("https://www.mercedes-benz.de/passengercars/buy/new-car/product.html/EQS-450-4MATIC-SUV_0-20133945_DE_354ae2f5")
        page.wait_for_load_state("networkidle")

        # Try to find the specific button selector
        button_selector = "#emh-pdp > div > div > div.product-stage > div.product-stage__bottom > div > div > div > div:nth-child(3) > div > button"
        logging.info(f"🔍 Trying to find PDP CTA button: {button_selector}")
        try:
            # Wait until the button is attached and visible
            page.wait_for_selector(button_selector, timeout=10000, state="visible")
            cta_button = page.locator(button_selector).first

            # Wait until the button is enabled (not disabled)
            for _ in range(20):  # Try for up to 2 seconds (20 x 100ms)
                if cta_button.is_enabled():
                    break
                page.wait_for_timeout(100)
            else:
                logging.warning("⚠️ PDP CTA button is visible but not enabled after waiting.")

            if cta_button.is_visible() and cta_button.is_enabled():
                logging.info("✅ PDP CTA button found, visible, and enabled (clickable).")
            else:
                logging.warning("⚠️ PDP CTA button found but is not clickable.")
        except Exception as e:
            logging.error(f"❌ PDP CTA button not found or not clickable: {e}")
        
         # Go back to Home Page
        page.goto(url)
        page.wait_for_load_state("networkidle")
        logging.info(f"✅ Home Page loaded: {url}")
        
        
        # Capture screenshot after scrolling to the main campaign element
        try:
            logging.info("🔍 Looking for [data-component-name='hp-campaigns'] element...")
            # Wait for at least one such element to appear (not strict)
            page.wait_for_selector("[data-component-name='hp-campaigns']", timeout=5000)
            elements = page.locator("[data-component-name='hp-campaigns']")
            count = elements.count()
            logging.info(f"Found {count} [data-component-name='hp-campaigns'] elements.")

            # Use the first visible element
            visible_element = None
            for i in range(count):
                el = elements.nth(i)
                if el.is_visible():
                    visible_element = el
                    break

            if visible_element:
                visible_element.scroll_into_view_if_needed()
                page.wait_for_timeout(2000)
                logging.info("✅ Scrolled to first visible [data-component-name='hp-campaigns'].")
                screenshot_path = "campaign_section.png"
                page.screenshot(path=screenshot_path)  # Use full_page=True for a larger screenshot
                logging.info(f"📸 Screenshot taken and saved as {screenshot_path}")
            else:
                logging.warning("⚠️ No visible [data-component-name='hp-campaigns'] found.")
        except Exception as e:
            logging.error(f"❌ Error while scrolling to [data-component-name='hp-campaigns']: {e}")    
    
        browser.close()
        
if __name__ == "__main__":
    test_shadow_dom_click()