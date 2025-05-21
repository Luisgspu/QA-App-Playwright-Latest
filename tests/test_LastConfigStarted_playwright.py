import logging
import allure
import uuid
from Utils.ConfigStarted import ConfiguratorStarted  # Should accept Playwright Page

def generate_test_uuid(test_name):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, test_name))

class LCStartedTest:
    def __init__(self, page, urls, test_link=None):
        self.page = page  # Playwright Page
        self.urls = urls
        self.test_link = test_link

    @allure.feature("Last Configuration Started Test Suite")
    @allure.story("Run Last Configuration Started Test")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.id(generate_test_uuid("run_LCStarted_test"))
    def run(self):
        """Executes the Last Configuration Started test."""
        try:
            self.perform_LCStarted_test()
            if self.test_link:
                self.navigate_to_salesforce()
        except Exception as e:
            logging.error(f"❌ Error during the Last Configuration Started test: {e}")
            allure.attach(f"Error: {e}", name="Test Error", attachment_type=allure.attachment_type.TEXT)

    @allure.step("Perform Last Configuration Started Test Logic")
    @allure.id(generate_test_uuid("LCCompleted_test"))
    def perform_LCStarted_test(self):
        configurator = ConfiguratorStarted(self.page)
        try:
            # Navigate to the configurator and perform actions
            with allure.step(f"🌍 Navigated to: {self.urls['CONFIGURATOR']}"):
                self.page.goto(self.urls['CONFIGURATOR'])
                logging.info(f"🌍 Navigated to the configurator: {self.urls['CONFIGURATOR']}")
                self.page.wait_for_load_state("networkidle")

            # Call the perform_configurator_actions function from ConfiguratorStarted
            with allure.step("✅ Performing configuration actions"):
                try:
                    configurator.perform_configurator_actions()
                    logging.info("✅ Successfully performed configuration actions.")
                except Exception as e:
                    logging.error(f"❌ Error performing configuration actions: {e}")
                    allure.attach(f"Error: {e}", name="Configuration Actions Error", attachment_type=allure.attachment_type.TEXT)
                    raise

            # Navigate back to the home page
            with allure.step(f"🌍 Navigating back to: {self.urls['HOME_PAGE']}"):
                self.page.goto(self.urls['HOME_PAGE'])
                logging.info(f"🌍 Navigated back to: {self.urls['HOME_PAGE']}")
                self.page.wait_for_load_state("networkidle")

        except Exception as e:
            logging.error(f"❌ Error in configurator: {e}")

    @allure.step("Navigate to Salesforce URL")
    @allure.id(generate_test_uuid("navigate_to_salesforce"))
    def navigate_to_salesforce(self):
        """Navigates to the Salesforce link if provided."""
        try:
            salesforce_url = self.urls['HOME_PAGE'] + self.test_link
            self.page.goto(salesforce_url)
            logging.info(f"🌍 Navigated to Salesforce URL: {salesforce_url}")
            self.page.wait_for_load_state("networkidle")
        except Exception as e:
            logging.error(f"❌ Error navigating to Salesforce URL: {e}")
            allure.attach(f"Error: {e}", name="Salesforce Navigation Error", attachment_type=allure.attachment_type.TEXT)