import time
import logging
from playwright.sync_api import Page, TimeoutError

import logging
from playwright.sync_api import Page, TimeoutError

class ConfiguratorCompleted:
    def __init__(self, page: Page):
        """Initializes the Configurator with a Playwright Page instance."""
        self.page = page

    
    def perform_configurator_actions(self):
        """Performs navigation and clicks inside the car configurator menu using Playwright."""
        try:
            logging.info("🔍 Starting configurator interaction.")

            # Define the shadow host selector
            shadow_host_selector = (
                'body > div.root.responsivegrid.owc-content-container > div > main > div > owcc-car-configurator'
            )

            # 1. Wait for the shadow host to be visible using a Locator.
            # Using 'visible' state ensures it's both attached and rendered.
            logging.info(f"🔍 Waiting for shadow host to be visible: {shadow_host_selector}")
            shadow_host_locator = self.page.locator(shadow_host_selector)
            shadow_host_locator.wait_for(timeout=15000, state="visible") # Increased timeout for initial load
            logging.info("✅ Shadow host located and visible.")

            # Get the ElementHandle from the locator to access its shadow DOM.
            # This is necessary because direct Playwright locators don't automatically
            # pierce shadow DOMs if the shadow root itself is not a part of the selector.
            shadow_host_element = shadow_host_locator.element_handle()
            if not shadow_host_element:
                raise Exception("Failed to retrieve ElementHandle for shadow host.")

            # Expand shadow root
            # evaluate_handle returns a JSHandle, which we need to treat as an ElementHandle
            # to use Playwright's waiting methods on it.
            shadow_root_js_handle = shadow_host_element.evaluate_handle("el => el.shadowRoot")
            shadow_root_element = shadow_root_js_handle.as_element() # Convert JSHandle to ElementHandle if it's an element
            if not shadow_root_element:
                raise Exception("Failed to expand shadow root or retrieve its ElementHandle.")
            
            # Define the main frame selector *inside* the shadow root
            main_frame_selector_in_shadow = (
                '#cc-app-container-main > div.cc-app-container__main-frame.cc-grid-container > div.cc-app-container__navigation.ng-star-inserted > cc-navigation > div > nav > ul'
            )

            # 2. Wait for the main_frame element *inside* the shadow root to be visible.
            # This directly addresses the 'NoneType' error by ensuring the element exists
            # within the shadow DOM before attempting to hover.
            logging.info(f"🔍 Waiting for main frame (UL) inside shadow root: {main_frame_selector_in_shadow}")
            main_frame_element = shadow_root_element.wait_for_selector(main_frame_selector_in_shadow, timeout=15000, state="visible")
            if not main_frame_element: # This check should technically be redundant if wait_for_selector throws on timeout
                raise Exception(f"Main frame (UL) not found inside shadow root: {main_frame_selector_in_shadow}")

            # Now, you have a valid ElementHandle for main_frame_element, which you can hover over
            main_frame_element.hover()
            logging.info("✅ Hovered over the main frame (ul element) inside shadow root.")
            
            # Find the last <li> in the nav, also *inside* the shadow root
            last_child_selector_in_shadow = (
                '#cc-app-container-main > div.cc-app-container__main-frame.cc-grid-container > div.cc-app-container__navigation.ng-star-inserted > cc-navigation > div > nav > ul > li:last-child'
            )
            logging.info(f"🔍 Waiting for last child (LI) inside shadow root: {last_child_selector_in_shadow}")
            last_child_element = shadow_root_element.wait_for_selector(last_child_selector_in_shadow, timeout=15000, state="visible")
            if not last_child_element:
                raise Exception(f"Last child (LI) not found inside shadow root: {last_child_selector_in_shadow}")
            logging.info("✅ Found last child element (li:last-child) inside shadow root.")

            # Hover over it
            last_child_element.hover()
            logging.info("✅ Hovered over the last child element inside shadow root.")

            # Try to click a child <a> or <button> within the <li>
            try:
                logging.info("🔍 Trying to find inner clickable element (a/button) inside last LI.")
                # Use query_selector on last_child_element to find children within it.
                # Consider using wait_for_selector here if these children are also dynamic.
                link_inside_element = last_child_element.query_selector('a, button') 
                if link_inside_element:
                    link_inside_element.click()
                    logging.info("✅ Clicked on inner clickable element (a/button) inside last LI.")
                else:
                    raise Exception("No <a> or <button> found inside <li>.")
            except Exception as e:
                logging.warning(f"⚠️ {e}. Fallback: clicking the <li> itself.")
                # Fallback: click the <li> itself
                last_child_element.click()
                logging.info("✅ Fallback click on <li> inside shadow root.")

            # Avoid using fixed wait_for_timeout() unless absolutely necessary (e.g., for animations)
            # Prefer waiting for a specific element or network condition to signal readiness.
            self.page.wait_for_timeout(3000) # Keep this only if you know a specific animation/transition requires it
            logging.info("🏁 Configurator interaction completed.")

        except TimeoutError as te:
            logging.error(f"❌ Timeout error during configurator actions: {te}. Element not found or not in desired state within timeout.")
            raise # Re-raise to indicate test failure
        except Exception as e:
            logging.error(f"❌ General error while performing configurator actions: {e}")
            raise # Re-raise to indicate test failure