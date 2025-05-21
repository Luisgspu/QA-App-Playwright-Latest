import logging
import allure
import uuid
from playwright.sync_api import Page

def generate_test_uuid(test_name):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, test_name))

class LSeenSRPTest:
    def __init__(self, page: Page, urls, test_link=None):
        self.page = page
        self.urls = urls
        self.test_link = test_link

    @allure.feature("Last Seen SRP")
    @allure.story("Run Last Seen SRP Test")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.id(generate_test_uuid("run_LSeenSRP_test"))
    def run(self):
        """Run the Last Seen SRP test."""
        self.perform_LSSRP_test()
        if self.test_link:
            self.navigate_to_salesforce()
         


    @allure.step("Perform Last Seen SRP Logic")
    @allure.id(generate_test_uuid("perform_LSSRP_test"))
    def perform_LSSRP_test(self):
        """Perform the main Last Seen SRP test logic."""
        try:
            # Navigate to ONLINE STORE
            with allure.step(f"🌍 Navigated to: {self.urls['ONLINE_SHOP']}"):
                self.page.goto(self.urls['ONLINE_SHOP'])
                self.page.wait_for_selector("img.wbx-vehicle-tile__image-img", timeout=20000, state="visible")
                self.page.wait_for_timeout(1000)
                logging.info(f"🌍 Navigated to: {self.urls['ONLINE_SHOP']}")

            # Navigate back to HOME_PAGE
            with allure.step(f"🌍 Navigated back to: {self.urls['HOME_PAGE']}"):
                self.page.goto(self.urls['HOME_PAGE'])
                logging.info(f"🌍 Navigated back to: {self.urls['HOME_PAGE']}")
                self.page.wait_for_load_state("networkidle")
        except Exception as e:
            logging.error(f"❌ Error during Last Seen SRP: {e}")

    @allure.step("Navigate to Salesforce URL")
    @allure.id(generate_test_uuid("navigate_to_salesforce"))
    def navigate_to_salesforce(self):
        """Navigate to the Salesforce URL if test_link is provided."""
        salesforce_url = self.urls['HOME_PAGE'] + self.test_link
        self.page.goto(salesforce_url)
        logging.info(f"🌍 Navigated to Salesforce URL: {salesforce_url}")
        self.page.wait_for_load_state("networkidle")