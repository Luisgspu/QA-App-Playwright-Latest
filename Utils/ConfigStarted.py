import logging
from playwright.sync_api import Page

class ConfiguratorStarted:
    def __init__(self, page: Page):
        """Initializes the Configurator with a Playwright Page instance."""
        self.page = page

    def expand_shadow_element(self, shadow_host_selector):
        """Returns the shadow root handle for a given shadow host selector."""
        shadow_host = self.page.locator(shadow_host_selector).element_handle()
        if not shadow_host:
            logging.error(f"❌ Shadow host not found for selector: {shadow_host_selector}")
            return None
        shadow_root = self.page.evaluate_handle("el => el.shadowRoot", shadow_host)
        if not shadow_root:
            logging.error(f"❌ Shadow root not found for host: {shadow_host_selector}")
        return shadow_root

    def perform_configurator_actions(self):
        """Performs navigation and clicks inside the car configurator menu using Playwright."""
        try:
            logging.info("🔍 Starting configurator interaction.")

            # Locate shadow host and expand root
            shadow_host_selector = (
                "body > div.root.responsivegrid.owc-content-container > div > main > div > owcc-car-configurator"
            )
            shadow_root = self.expand_shadow_element(shadow_host_selector)
            if not shadow_root:
                logging.error("❌ Could not expand shadow root. Aborting configurator actions.")
                return
            logging.info("✅ Shadow DOM expanded.")

           # Access main <ul> inside navigation
            main_frame = self.page.evaluate_handle(
                """root => root.querySelector(
                    '#cc-app-container-main > div.cc-app-container__main-frame.cc-grid-container > div.cc-app-container__navigation.ng-star-inserted > cc-navigation > div > nav > ul'
                )""",
                shadow_root
            )
            if not main_frame:
                logging.error("❌ Main <ul> element not found in shadow DOM.")
                return
            self.page.evaluate("el => { if (el) el.scrollIntoView(); }", main_frame)
            logging.info("✅ Scrolled to the main frame (ul element).")

            # Instead of clicking the <ul>, click the first <li> or its child <a>/<button>
            first_li = self.page.evaluate_handle(
                "ul => ul ? ul.querySelector('li') : null", main_frame
            )
            if first_li:
                self.page.evaluate("el => { if (el) el.scrollIntoView(); }", first_li)
                clickable = self.page.evaluate_handle(
                    "li => li ? li.querySelector('a, button') : null", first_li
                )
                if clickable:
                    self.page.evaluate("el => { if (el) el.click(); }", clickable)
                    logging.info("✅ Clicked on first <li>'s clickable child (a/button).")
                else:
                    self.page.evaluate("el => { if (el) el.click(); }", first_li)
                    logging.info("✅ Clicked on first <li>.")
            else:
                logging.warning("⚠️ No <li> found inside main <ul>.")

            # Find the second <li> in the nav
            second_child = self.page.evaluate_handle(
                """root => root.querySelector(
                    '#cc-app-container-main > div.cc-app-container__main-frame.cc-grid-container > div.cc-app-container__navigation.ng-star-inserted > cc-navigation > div > nav > ul > li:nth-child(2)'
                )""",
                shadow_root
            )
            if not second_child:
                logging.error("❌ Second <li> element not found in navigation.")
                return
            self.page.evaluate("el => { if (el) el.scrollIntoView(); }", second_child)
            logging.info("✅ Scrolled to the second child element (li:nth-child(2)).")
            self.page.evaluate("el => { if (el) el.focus(); }", second_child)
            logging.info("✅ Focused on the second child element.")

            # Try to click a child <a> or <button> within the <li>
            try:
                link_inside = self.page.evaluate_handle(
                    "el => el ? el.querySelector('a, button') : null", second_child
                )
                if link_inside:
                    self.page.evaluate("el => { if (el) el.click(); }", link_inside)
                    logging.info("✅ Clicked on inner clickable element (a/button).")
                else:
                    raise Exception("No <a> or <button> found inside <li>.")
            except Exception as e:
                # Fallback: click the <li> itself
                self.page.evaluate("el => { if (el) el.click(); }", second_child)
                logging.warning(f"⚠️ Fallback click on <li> using JavaScript. Reason: {e}")

            self.page.wait_for_timeout(3000)

        except Exception as e:
            logging.error(f"❌ Error while performing configurator actions: {e}")