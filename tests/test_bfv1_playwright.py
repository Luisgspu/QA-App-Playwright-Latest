import logging
import allure
import time
import pytest
from playwright.sync_api import Page

class BFV1Test:
    def __init__(self, page: Page, urls, market_code=None, model_code=None, test_link=None):
        self.page = page
        self.urls = urls
        self.market_code = market_code
        self.model_code = model_code
        self.test_link = test_link
        self.retries = 0
        self.max_retries = 5

    @allure.feature("BFV1 Test Suite")
    @allure.story("Run BFV1 Test")
    @allure.severity(allure.severity_level.CRITICAL)
    def run(self):
        """Run the BFV1 test with retry logic."""
        test_success = False

        for attempt in range(self.max_retries):
            try:
                self.perform_bfv1_test()

                if self.test_link:
                    self.navigate_to_salesforce()

                test_success = True
                break
            except Exception as e:
                logging.error(f"❌ Error during BFV1 test: {e}")
                self.retries += 1
                allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)

        if not test_success:
            raise Exception(f"❌ BFV1 Test failed after {self.max_retries} attempts.")

    @allure.step("Perform BFV1 Test Logic")
    def perform_bfv1_test(self):
        """Perform the main BFV1 test logic."""
        # Navigate to the product page
        with allure.step(f"🌍 Navigating to: {self.urls['PRODUCT_PAGE']}"):
            self.page.goto(self.urls['PRODUCT_PAGE'])
            logging.info(f"🌍 Navigated to: {self.urls['PRODUCT_PAGE']}")
            self.page.wait_for_load_state("networkidle")

        # Navigate back to the home page
        with allure.step(f"🌍 Navigating back to: {self.urls['HOME_PAGE']}"):
            self.page.goto(self.urls['HOME_PAGE'])
            self.page.wait_for_load_state("load")
            logging.info(f"🌍 Navigated back to: {self.urls['HOME_PAGE']}")

    @allure.step("Navigate to Salesforce URL")
    def navigate_to_salesforce(self):
        """Navigate to the Salesforce URL if test_link is provided."""
        salesforce_url = self.urls['HOME_PAGE'] + self.test_link
        with allure.step(f"🌍 Navigating to Salesforce URL: {salesforce_url}"):
            self.page.goto(salesforce_url)
            logging.info(f"🌍 Navigated to Salesforce URL: {salesforce_url}")
            self.page.wait_for_load_state("load")