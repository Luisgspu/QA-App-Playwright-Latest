import time
import logging
from playwright.sync_api import Page

class ConfiguratorCompleted:
    def __init__(self, page: Page):
        """Initializes the Configurator with a Playwright Page instance."""
        self.page = page

    def perform_configurator_actions(self):
        """Performs navigation and clicks inside the car configurator menu using Playwright."""
        try:
            logging.info("🔍 Starting configurator interaction.")

            # Wait for the shadow host to be attached
            shadow_host_selector = (
                'body > div.root.responsivegrid.owc-content-container > div > '
                'div.responsivegrid.ng-content-root.aem-GridColumn.aem-GridColumn--default--12 > '
                'div > owcc-car-configurator'
            )
            self.page.wait_for_selector(shadow_host_selector, timeout=10000, state="attached")
            shadow_host = self.page.locator(shadow_host_selector).element_handle()
            logging.info("✅ Shadow host located.")

            # Expand shadow root and access navigation <ul>
            shadow_root = shadow_host.evaluate_handle("el => el.shadowRoot")
            main_frame_selector = (
                '#cc-app-container-main > div.cc-app-container__main-frame.cc-grid-container > '
                'div.cc-app-container__navigation.ng-star-inserted > cc-navigation > nav > div > ul'
            )
            main_frame = shadow_root.as_element().query_selector(main_frame_selector)
            main_frame.hover()
            
            """
            logging.info("✅ Hovered over the main frame (ul element).")
            main_frame.click()
            logging.info("✅ Clicked on the main frame (ul element).")
            """

            # Find the last <li> in the nav
            last_child_selector = (
                '#cc-app-container-main > div.cc-app-container__main-frame.cc-grid-container > '
                'div.cc-app-container__navigation.ng-star-inserted > cc-navigation > nav > div > ul > li:last-child'
            )
            last_child = shadow_root.as_element().query_selector(last_child_selector)
            logging.info("🔍 Found last child element (li:last-child).")

            # Hover over it
            last_child.hover()
            logging.info("✅ Hovered over the last child element.")

            # Try to click a child <a> or <button> within the <li>
            try:
                link_inside = last_child.query_selector('a, button')
                if link_inside:
                    link_inside.click()
                    logging.info("✅ Clicked on inner clickable element (a/button).")
                else:
                    raise Exception("No <a> or <button> found inside <li>.")
            except Exception as e:
                # Fallback: click the <li> itself
                last_child.click()
                logging.info("✅ Fallback click on <li> using Playwright.")

            # Wait for the configurator to load
            self.page.wait_for_timeout(2000)
            
        except Exception as e:
            logging.error(f"❌ Error while performing configurator actions: {e}")