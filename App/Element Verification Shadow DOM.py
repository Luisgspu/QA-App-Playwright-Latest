import logging
from playwright.sync_api import sync_playwright
from ScreenshotHandler import ScreenshotHandler  # Assuming this is in another file
from playwright.sync_api import Page
from ImageVerifier import ImageVerifier  # Assuming this is in another file


logging.basicConfig(level=logging.INFO, format="%(message)s")

def test_shadow_dom_click():
    url = "https://www.mercedes-benz.de"
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
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
        page.wait_for_load_state("load")
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
        
        # Open PI Page
        page.goto("https://www.mercedes-benz.de/passengercars/models/suv/eqa/overview.html")
        page.wait_for_load_state("load")    
        logging.info(f"✅ PI Page loaded: {url}")
        
        # Go back to Home Page
        page.goto(url)
        page.wait_for_load_state("load")
        page.wait_for_timeout(2000)  # Espera 4 segundos, ajusta según necesidad
        logging.info(f"✅ Navigated Back to Home Page: {url}")
        
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
        """
        expected_src = "/content/dam/hq/personalization/campaignmodule/"
        
        element = page.locator("[data-component-name='hp-campaigns']")
        element.wait_for(state="attached", timeout=5000)
        count = element.count()
        logging.info(f"Found {count} [data-component-name='hp-campaigns'] elements.")

        if count > 0:
            # Busca todas las imágenes dentro del primer elemento encontrado
            images = element.first.locator("img")
            img_count = images.count()
            logging.info(f"Found {img_count} <img> elements inside [data-component-name='hp-campaigns'].")

            srcs = []
            for i in range(img_count):
                src = images.nth(i).get_attribute("src")
                srcs.append(src)
                print(f"Image {i+1} src: {src}")
                logging.info(f"Image {i+1} src: {src}")
                if src and expected_src in src:
                    found_match = True
                    
            logging.info("All found image srcs:\n" + "\n".join([str(s) for s in srcs]))
            if found_match:
                logging.info(f"✅ Personalized image applied correctly. Expected source found: {expected_src}")
            else:
                logging.warning(f"❌ No image src contains the expected substring: {expected_src}")    

            # Si quieres, también puedes adjuntar todos los srcs a un archivo o reporte aquí

            element.first.scroll_into_view_if_needed()
            page.wait_for_timeout(2000)
            logging.info("✅ Scrolled to [data-component-name='hp-campaigns'].")
        else:
            logging.warning("⚠️ [data-component-name='hp-campaigns'] not found.")
        
        """
        expected_src = "/content/dam/hq/personalization/campaignmodule/"
        verifier = ImageVerifier(page)
        result = verifier.verify_image("[data-component-name='hp-campaigns'] img", expected_src)
        
        # Take screenshot of the visible area
        screenshot_path = "campaign_section.png"
        
        try:
            ScreenshotHandler.scroll_and_capture_section(page, screenshot_path)
            logging.info(f"✅ Screenshot saved and attached at: {screenshot_path}")
        except Exception as e:
            logging.error(f"❌ Failed to capture or attach screenshot: {e}")
            
            

        browser.close()
        
if __name__ == "__main__":
    test_shadow_dom_click()