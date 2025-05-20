import logging
from playwright.sync_api import sync_playwright
from ScreenshotHandler import ScreenshotHandler  # Assuming this is in another file
from playwright.sync_api import Page
from ImageVerifier import ImageVerifier  # Assuming this is in another file
from XHRResponseCapturer import XHRResponseCapturer  # Assuming this is the correct import for your XHR capturer
import json
from ConfigStarted import ConfiguratorStarted  # Playwright version


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
        
        # Capture XHR response
        test_name = "Last Configuration Started"
        target_url_filter = "evergage.com/api2/event"
        
        
        
        # Open a Home Page
        page = context.new_page()
        
        # Verify the XHR response
        # 1. Instantiate the capturer
        xhr_capturer = XHRResponseCapturer(page, target_url_filter)
        
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
        page.goto("https://www.mercedes-benz.de/passengercars/mercedes-benz-cars/car-configurator.html/motorization/CCci/DE/de/EQA-KLASSE/OFFROADER?vehicleId=de_DE__2437021__AU-311_LE-L_LU-696_MJ-806_PC-904-P59-PBG-PSA-U59-U62_PS-953%23-B05%23_SA-01U-02B-13U-218-243-258-261-270-286-287-294-310-345-351-355-362-365-367-39U-400-428-475-504-51U-521-537-543-55H-580-5B0-608-632-63B-677-679-70B-72B-73B-79B-7U2-82B-83B-859-873-877-88B-890-942-969-986-9B2-B13-B27-B51-B53-B59-L3E-R05-R31-U01-U10-U12-U22-U35-U55-U60_SC-0S3-0U1-1B3-2U1-2U8-502-51B-5V4-6P5-7B4-7S3-8P3-8S8-8U6-8U8-998-9U8-BAF-EMD-K13-K37-K45-R7H")
        page.wait_for_load_state("networkidle")
        logging.info(f"✅ Config Page loaded: {url}")
        
        # Perform Configurator actions
        configurator = ConfiguratorStarted(page)
        configurator.perform_configurator_actions()
               
        
        # Go back to Home Page
        page.goto(url)
        page.wait_for_load_state("networkidle")
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
       

        # 2. Set the campaign name substring for filtering
        xhr_capturer.set_campaign_name_substring(test_name)
        
        # 4. After actions, get and log the filtered XHR data
        xhr_data = xhr_capturer.get_captured_data()
        logging.info(f"Filtered XHR data: {json.dumps(xhr_data, indent=2, ensure_ascii=False)}")

        # Optionally, iterate and log campaigns for debugging
        for response in xhr_data:
            campaigns = response.get("body", {}).get("campaignResponses", [])
            for campaign in campaigns:
                logging.info(f"Filtered campaign: {campaign.get('campaignName', '')}")
        
        # Verify the personalized image
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