import logging
import allure
import uuid
from playwright.sync_api import Page

def generate_test_uuid(test_name):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, test_name))

class LSeenPDPTest:
    def __init__(self, page: Page, urls, test_link=None):
        self.page = page
        self.urls = urls
        self.test_link = test_link
        self.retries = 0
        self.max_retries = 5

    @allure.feature("Last Seen PDP")
    @allure.story("Run Last Seen PDP Test")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.id(generate_test_uuid("run_LSeenPDP_test"))
    def run(self):
        test_success = False
        while self.retries < self.max_retries:
            try:
                self.perform_LSPDP_test()
                if self.test_link:
                    self.navigate_to_salesforce()
                test_success = True
                break
            except Exception as e:
                logging.error(f"❌ Error during Last Seen PDP test: {e}")
                self.retries += 1
                continue

        if not test_success:
            logging.error(f"❌ Last Seen PDP Test failed after {self.max_retries} attempts.")

    @allure.step("Perform Last Seen PDP Logic")
    @allure.id(generate_test_uuid("perform_LSeenPDP_test"))
    def perform_LSPDP_test(self):
        """Perform the main Last Seen PDP test logic."""
        try:
            with allure.step(f"🌍 Navigated to: {self.urls['ONLINE_SHOP']}"):
                self.page.goto(self.urls['ONLINE_SHOP'])
                logging.info(f"🌍 Navigated to: {self.urls['ONLINE_SHOP']}")
                self.page.wait_for_selector("img.wbx-vehicle-tile__image-img", timeout=20000, state="visible")

            with allure.step("Extracted PDP URL"):
                element = self.page.locator("img.wbx-vehicle-tile__image-img").first
                parent = element.locator("xpath=ancestor::a").first
                pdp_url = parent.get_attribute("href")
                logging.info(f"🌍 Extracted PDP URL: {pdp_url}")
                allure.attach(pdp_url or "None", name="Extracted PDP URL", attachment_type=allure.attachment_type.TEXT)

            with allure.step(f"🌍 Opened PDP URL: {pdp_url}"):
                self.page.goto(pdp_url)
                logging.info(f"🌍 Opened PDP URL: {pdp_url}")
                self.page.wait_for_load_state("networkidle")
                self.page.wait_for_timeout(6500)

            with allure.step(f"🌍 Navigated back to: {self.urls['HOME_PAGE']}"):
                self.page.goto(self.urls['HOME_PAGE'])
                logging.info(f"🌍 Navigated back to: {self.urls['HOME_PAGE']}")
                self.page.wait_for_load_state("networkidle")
        except Exception as e:
            with allure.step("Handle exception during Last Seen PDP test"):
                logging.error(f"❌ Error during Last Seen PDP test: {e}")
                allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)

    @allure.step("Navigate to Salesforce URL")
    @allure.id(generate_test_uuid("navigate_to_salesforce"))
    def navigate_to_salesforce(self):
        """Navigate to the Salesforce URL if test_link is provided."""
        salesforce_url = self.urls['HOME_PAGE'] + self.test_link
        self.page.goto(salesforce_url)
        logging.info(f"🌍 Navigated to Salesforce URL: {salesforce_url}")
        self.page.wait_for_load_state("networkidle")