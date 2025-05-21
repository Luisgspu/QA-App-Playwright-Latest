import logging
import time
import allure
import uuid
from Utils.ConfigCompleted import ConfiguratorCompleted  # This should use Playwright Page
from playwright.sync_api import Page, sync_playwright


# Generate a consistent UUID for the test using the test name
def generate_test_uuid(test_name):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, test_name))

class BFV3Test:
    def __init__(self, page, urls, test_link=None):
        self.page = page  # Playwright Page
        self.urls = urls
        self.test_link = test_link


    @allure.feature("BFV3 Test Suite")
    @allure.story("Run BFV3 Test")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.id(generate_test_uuid("run_bfv3_test"))
    def run(self):
        """Run the BFV3 test."""
        self.perform_bfv3_test()
        if self.test_link:
            self.navigate_to_salesforce()

    @allure.step("Perform BFV3 Test Logic")
    @allure.id(generate_test_uuid("perform_bfv3_test"))
    def perform_bfv3_test(self):
        """Perform the main BFV3 test logic."""
        configurator = ConfiguratorCompleted(self.page)

        # Navigate to the product page
        with allure.step(f"🌍 Navigated to: {self.urls['PRODUCT_PAGE']}"):
            self.page.goto(self.urls['PRODUCT_PAGE'])
            logging.info(f"🌍 Navigated to: {self.urls['PRODUCT_PAGE']}")
            self.page.wait_for_load_state("networkidle")

        # Navigate to CONFIGURATOR
        with allure.step(f"🌍 Navigated to: {self.urls['CONFIGURATOR']}"):
            self.page.goto(self.urls['CONFIGURATOR'])
            logging.info(f"🌍 Navigated to: {self.urls['CONFIGURATOR']}")
            self.page.wait_for_load_state("networkidle")

        # Execute actions in CONFIGURATOR
        with allure.step("✅ Performing configuration actions"):
            try:
                configurator.perform_configurator_actions()
                self.page.wait_for_timeout(1000)  # Wait for 2 seconds to ensure actions are completed

                logging.info("✅ Successfully performed configuration actions.")
            except Exception as e:
                logging.error(f"❌ Error performing configuration actions: {e}")
                allure.attach(f"Error: {e}", name="Configuration Actions Error", attachment_type=allure.attachment_type.TEXT)
                raise

        # Navigate back to the home page
        with allure.step(f"🌍 Navigated back to: {self.urls['HOME_PAGE']}"):
            self.page.goto(self.urls['HOME_PAGE'])
            logging.info(f"🌍 Navigated back to: {self.urls['HOME_PAGE']}")
            self.page.wait_for_load_state("networkidle")

    @allure.step("Navigate to Salesforce URL")
    @allure.id(generate_test_uuid("navigate_to_salesforce"))
    def navigate_to_salesforce(self):
        """Navigate to the Salesforce URL if test_link is provided."""
        salesforce_url = self.urls['HOME_PAGE'] + self.test_link
        self.page.goto(salesforce_url)
        logging.info(f"🌍 Navigated to Salesforce URL: {salesforce_url}")
        self.page.wait_for_load_state("networkidle")