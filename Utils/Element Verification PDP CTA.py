import logging
from playwright.sync_api import sync_playwright
from ScreenshotHandler import ScreenshotHandler  # Assuming this is in another file
from playwright.sync_api import Page
from ImageVerifier import ImageVerifier  # Assuming this is in another file
from XHRResponseCapturer import XHRResponseCapturer  # Assuming this is the correct import for your XHR capturer
import json
from ConfigStarted import ConfiguratorStarted  # Playwright version
from ConfigCompleted import ConfiguratorCompleted  # Playwright version
from playwright.sync_api import Page, expect, TimeoutError
from CookiesHandler import CookieHandler  # Assuming this is in another file


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
        page.wait_for_load_state("domcontentloaded")
        logging.info(f"✅ Home Page loaded: {url}")
        
        # Accept cookies if necessary
        cookie_handler = CookieHandler(page)
        cookie_handler.accept_cookies()
        
        page.goto("https://www.mercedes-benz.de/passengercars/models/suv/eqa/overview.html")
        page.wait_for_load_state("domcontentloaded")
        
        
        
        """        
        # Try to find the specific button selector
        button_selector = "#emh-pdp > div > div > div.product-stage > div.product-stage__bottom > div > div > div > div:nth-child(3) > div > button"
        logging.info(f"🔍 Asserting PDP CTA button is enabled: {button_selector}")

        try:
            button_locator = page.locator(button_selector)
            # This will auto-retry until the element is enabled or the timeout is reached.
            expect(button_locator).to_be_enabled(timeout=10000)
            logging.info("✅ PDP CTA button is enabled as expected.")
        except TimeoutError:
            logging.error(f"❌ PDP CTA button did not become enabled within 10 seconds (TimeoutError). Selector: {button_selector}")
        except Exception as e:
            logging.error(f"❌ An unexpected error occurred during assertion for PDP CTA button: {e}")
                
        """        
     
        # Go back to Home Page
        page.goto(url)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)  # Wait for 2 seconds to ensure the page is fully loaded
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
                visible_element.evaluate("el => el.scrollIntoView({block: 'start'})")
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