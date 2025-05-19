import logging
from playwright.sync_api import Page

class ConfiguratorStarted:
    def __init__(self, page: Page):
        """Initializes the Configurator with a Playwright Page instance."""
        self.page = page

    def expand_shadow_element(self, shadow_host_selector):
        """Returns the shadow root handle for a given shadow host selector."""
        shadow_host = self.page.locator(shadow_host_selector).element_handle()
        shadow_root = self.page.evaluate_handle("el => el.shadowRoot", shadow_host)
        return shadow_root

    def perform_configurator_actions(self):
        """Performs navigation and clicks inside the car configurator menu using Playwright."""
        try:
            logging.info("🔍 Starting configurator interaction.")

            # Locate shadow host and expand root
            shadow_host_selector = (
                "body > div.root.responsivegrid.owc-content-container > div > "
                "div.responsivegrid.ng-content-root.aem-GridColumn.aem-GridColumn--default--12 > div > owcc-car-configurator"
            )
            shadow_root = self.expand_shadow_element(shadow_host_selector)
            logging.info("✅ Shadow DOM expanded.")

            # Access main <ul> inside navigation
            main_frame = self.page.evaluate_handle(
                """root => root.querySelector(
                    '#cc-app-container-main > div.cc-app-container__main-frame.cc-grid-container > '
                    + 'div.cc-app-container__navigation.ng-star-inserted > cc-navigation > nav > div > ul'
                )""",
                shadow_root
            )
            self.page.evaluate("el => el.scrollIntoView()", main_frame)
            logging.info("✅ Scrolled to the main frame (ul element).")
            self.page.evaluate("el => el.click()", main_frame)
            logging.info("✅ Clicked on the main frame (ul element).")

            # Find the second <li> in the nav
            second_child = self.page.evaluate_handle(
                """root => root.querySelector(
                    '#cc-app-container-main > div.cc-app-container__main-frame.cc-grid-container > '
                    + 'div.cc-app-container__navigation.ng-star-inserted > cc-navigation > nav > div > ul > li:nth-child(2)'
                )""",
                shadow_root
            )
            self.page.evaluate("el => el.scrollIntoView()", second_child)
            logging.info("✅ Scrolled to the second child element (li:nth-child(2)).")
            self.page.evaluate("el => el.focus()", second_child)
            logging.info("✅ Focused on the second child element.")

            # Try to click a child <a> or <button> within the <li>
            try:
                link_inside = self.page.evaluate_handle(
                    "el => el.querySelector('a, button')", second_child
                )
                self.page.evaluate("el => el.click()", link_inside)
                logging.info("✅ Clicked on inner clickable element (a/button).")
            except Exception:
                # Fallback: click the <li> itself
                self.page.evaluate("el => el.click()", second_child)
                logging.info("✅ Fallback click on <li> using JavaScript.")

            self.page.wait_for_timeout(2000)

        except Exception as e:
            logging.error(f"❌ Error while performing configurator actions: {e}")