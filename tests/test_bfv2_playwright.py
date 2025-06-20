import logging
import allure
import pytest
import uuid
from playwright.sync_api import Page, sync_playwright
from Utils.ConfigStarted import ConfiguratorStarted  # Playwright version

def generate_test_uuid(test_name):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, test_name))

class BFV2Test:
    def __init__(self, page: Page, urls, test_link=None):
        self.page = page
        self.urls = urls
        self.test_link = test_link

    @allure.feature("BFV2 Test Suite")
    @allure.story("Run BFV2 Test")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.id(generate_test_uuid("run_bfv2_test"))
    def run(self):
        """Run the BFV2 test."""
        self.perform_bfv2_test()
        if self.test_link:
            self.navigate_to_salesforce()

    @allure.step("Perform BFV2 Test Logic")
    @allure.id(generate_test_uuid("perform_bfv2_test"))
    def perform_bfv2_test(self):
        configurator = ConfiguratorStarted(self.page)

        # Navigate to the product page
        with allure.step(f"🌍 Navigating to: {self.urls['PRODUCT_PAGE']}"):
            self.page.goto(self.urls['PRODUCT_PAGE'])
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(2000)
            logging.info(f"🌍 Navigating to: {self.urls['PRODUCT_PAGE']}")

        # Navigate to the configurator
        with allure.step(f"🌍 Navigating to: {self.urls['CONFIGURATOR']}"):
            self.page.goto(self.urls['CONFIGURATOR'])
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(4000)  # Wait for 2 seconds to ensure the page is fully loaded
            logging.info(f"🌍 Navigating to: {self.urls['CONFIGURATOR']}")
            

        # Call the perform_configurator_actions function from ConfiguratorStarted
        with allure.step("✅ Performing configuration actions"):
            try:
                configurator.perform_configurator_actions()
                logging.info("✅ Successfully performed configuration actions.")
                self.page.wait_for_timeout(2000) 
            except Exception as e:
                logging.error(f"❌ Error performing configuration actions: {e}")
                allure.attach(f"Error: {e}", name="Configuration Actions Error", attachment_type=allure.attachment_type.TEXT)
                raise

        # Navigate back to the home page
        with allure.step(f"🌍 Navigating back to: {self.urls['HOME_PAGE']}"):
            self.page.goto(self.urls['HOME_PAGE'])
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(3000) 
            logging.info(f"🌍 Navigating back to: {self.urls['HOME_PAGE']}")

    @allure.step("Navigate to Salesforce URL")
    @allure.id(generate_test_uuid("navigate_to_salesforce"))
    def navigate_to_salesforce(self):
        try:
            salesforce_url = self.urls['HOME_PAGE'] + self.test_link
            self.page.goto(salesforce_url)
            logging.info(f"🌍 Navigating to Salesforce URL: {salesforce_url}")
            self.page.wait_for_load_state("load")
            self.page.wait_for_timeout(2000)
        except Exception as e:
            logging.error(f"❌ Error navigating to Salesforce URL: {e}")
            allure.attach(f"Error: {e}", name="Salesforce Navigation Error", attachment_type=allure.attachment_type.TEXT)

