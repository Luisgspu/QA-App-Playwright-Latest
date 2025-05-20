import json
import logging
import allure
from playwright.sync_api import Page

class XHRResponseCapturer:
    """Captures XHR responses, filtering by Daimler's API."""

    def __init__(self, page: Page, target_url_filter: str, target_campaign_name_substring: str = ""):
        self.page = page
        self.TARGET_URL_FILTER = target_url_filter
        self.TARGET_CAMPAIGN_NAME_SUBSTRING = target_campaign_name_substring
        self.captured_data = []
        self._setup_request_interception()

    def _setup_request_interception(self):
        """Sets up request interception to capture XHR responses."""
        with allure.step("Setting up request interception"):
            self.page.on("response", self._capture_response)

    def set_campaign_name_substring(self, test_name: str):
        """Dynamically sets the campaign name substring based on the test name."""
        with allure.step(f"Setting campaign name substring for test: {test_name}"):
            if not test_name:
                allure.attach("Test name is empty or None. Defaulting to no filter.", name="Warning", attachment_type=allure.attachment_type.TEXT)
                self.TARGET_CAMPAIGN_NAME_SUBSTRING = ""
                return

            if "Personalized CTA" in test_name:
                self.TARGET_CAMPAIGN_NAME_SUBSTRING = "personalized cta"
            elif "BFV1" in test_name or "BFV2" in test_name or "BFV3" in test_name:
                self.TARGET_CAMPAIGN_NAME_SUBSTRING = "best-fitting-vehicle"
            elif "Last Configuration Started" in test_name or "Last Configuration Completed" in test_name:
                self.TARGET_CAMPAIGN_NAME_SUBSTRING = "last-configuration"
            elif "Last Seen SRP" in test_name or "Last Seen PDP" in test_name:
                self.TARGET_CAMPAIGN_NAME_SUBSTRING = "dcp-last-seen-pdp-srp"
            else:
                self.TARGET_CAMPAIGN_NAME_SUBSTRING = ""  # Default to no filter
            allure.attach(f"Campaign name substring set to: {self.TARGET_CAMPAIGN_NAME_SUBSTRING}", name="Info", attachment_type=allure.attachment_type.TEXT)
            logging.info(f"Campaign name substring set to: {self.TARGET_CAMPAIGN_NAME_SUBSTRING}")

    def _capture_response(self, response):
        try:
            if self.TARGET_URL_FILTER in response.url and response.status == 200:
                response_body = response.body()
                response_text = response_body.decode("utf-8") if response_body else ""

                try:
                    json_response = json.loads(response_text)
                    if "campaignResponses" in json_response:
                        all_campaigns = json_response["campaignResponses"]
                        filtered_campaigns = [
                            campaign for campaign in all_campaigns
                            if self.TARGET_CAMPAIGN_NAME_SUBSTRING.lower() in campaign.get("campaignName", "").lower()
                        ]
                        if filtered_campaigns:
                            filtered_response = {
                                "url": response.url,
                                "status": response.status,
                                "body": {"campaignResponses": filtered_campaigns}
                            }
                            self.captured_data.append(filtered_response)
                            logging.info(f"Filtered campaigns: {[c.get('campaignName') for c in filtered_campaigns]}")
                except json.JSONDecodeError:
                    logging.warning(f"Could not decode JSON from {response.url}")
        except Exception as e:
            logging.error(f"Error capturing response for {response.url}: {e}")

    
    def get_captured_data(self):
        """Returns the captured XHR responses."""
        return self.captured_data

    @staticmethod
    def attach_xhr_to_allure(xhr_path: str):
        """Attaches XHR data to Allure report."""
        try:
            with open(xhr_path, 'r', encoding='utf-8') as file:
                allure.attach(file.read(), name="XHR Responses", attachment_type=allure.attachment_type.JSON)
        except Exception as e:
            allure.attach(f"Error attaching XHR data to Allure: {e}", name="Error", attachment_type=allure.attachment_type.TEXT)