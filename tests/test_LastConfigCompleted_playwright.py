import logging
import allure
import uuid
from Utils.ConfigCompleted import ConfiguratorCompleted  # Should use Playwright Page

def generate_test_uuid(test_name):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, test_name))

class LCCompletedTest:
    def __init__(self, page, urls, test_link=None):
        self.page = page  # Playwright Page
        self.urls = urls
        self.test_link = test_link
        

    @allure.feature("Last Configuration Completed Test Suite")
    @allure.story("Run Last Configuration Completed Test")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.id(generate_test_uuid("run_LCCompleted_test"))
    def run(self):
        """Run the Last Configuration Completed test."""
        self.perform_LCCompleted_test()
        if self.test_link:
            self.navigate_to_salesforce()
  

    @allure.step("Perform Last Configuration Completed Logic")
    @allure.id(generate_test_uuid("perform_LCCompleted_test"))
    def perform_LCCompleted_test(self):
        """Perform the main Last Configuration Completed test logic."""
        configurator = ConfiguratorCompleted(self.page)
        try:
            # Navigate to CONFIGURATOR
            with allure.step(f"🌍 Navigated to: {self.urls['CONFIGURATOR']}"):
                self.page.goto(self.urls['CONFIGURATOR'])
                logging.info(f"🌍 Navigated to: {self.urls['CONFIGURATOR']}")
                self.page.wait_for_load_state("networkidle")

            # Execute actions in CONFIGURATOR
            with allure.step("✅ Performing configuration actions"):
                try:
                    configurator.perform_configurator_actions()
                    logging.info("✅ Successfully performed configuration actions.")
                except Exception as e:
                    logging.error(f"❌ Error performing configuration actions: {e}")
                    allure.attach(f"Error: {e}", name="Configuration Actions Error", attachment_type=allure.attachment_type.TEXT)
                    raise
        except Exception as e:
            logging.error(f"❌ Error in configurator: {e}")

        # Navigate back to the home page
        with allure.step(f"🌍 Navigated back to: {self.urls['HOME_PAGE']}"):
            self.page.goto(self.urls['HOME_PAGE'])
            logging.info(f"🌍 Navigated back to: {self.urls['HOME_PAGE']}")
            self.page.wait_for_load_state("networkidle")

    @allure.step("Navigate to Salesforce URL")
    @allure.id(generate_test_uuid("navigate_to_salesforce"))
    def navigate_to_salesforce(self):
        """Navigate to the Salesforce URL if test_link is provided."""
        try:
            salesforce_url = self.urls['HOME_PAGE'] + self.test_link
            self.page.goto(salesforce_url)
            logging.info(f"🌍 Navigated to Salesforce URL: {salesforce_url}")
            self.page.wait_for_load_state("networkidle")
        except Exception as e:
            logging.error(f"❌ Error navigating to Salesforce URL: {e}")
            allure.attach(f"Error: {e}", name="Salesforce Navigation Error", attachment_type=allure.attachment_type.TEXT)