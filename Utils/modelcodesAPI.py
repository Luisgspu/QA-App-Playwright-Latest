import requests
import logging
from playwright.sync_api import sync_playwright


class ModelCodesAPI:
    def __init__(self, access_token):
        """
        Initializes the ModelCodesAPI class with an access token for making API requests.
        
        Args:
            access_token (str): The access token for the API.
        """
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def fetch_model_codes(self, market_code):
        """
        Fetches and filters model codes for passenger cars from the API.

        Args:
            market_code (str): The market code to fetch model codes for.

        Returns:
            list: A list of passenger car model codes, or an empty list if an error occurs.
        """
        url = f"https://api.oneweb.mercedes-benz.com/vehicle-deeplinks-api/v1/deeplinks/{market_code}/model-series"
        try:
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                try:
                    data = response.json()
                    if not isinstance(data, dict):
                        logging.error("The API response does not have the expected format.")
                        return []

                    passenger_car_model_codes = []
                    for model_key, model_data in data.items():
                        contains_excluded_keywords = any(
                            keyword in value.get("modelSeriesUrl", "")
                            for key, value in model_data.items()
                            if isinstance(value, dict)
                            for keyword in ["/vans/", "/amg-gt-2-door/", "/amg-gt-4-door/", "/mercedes-maybach-s-class/", "/mercedes-maybach-sl/", "/maybach-eqs/", "/maybach/"]
                        )
                        if not contains_excluded_keywords:
                            passenger_car_model_codes.append(model_key)
                    return passenger_car_model_codes
                except ValueError:
                    logging.error("Error parsing the JSON response.")
                    return []
            else:
                logging.error("Error fetching data. Status code: %s", response.status_code)
                return []
        except requests.exceptions.RequestException as e:
            logging.error("An error occurred while making the request: %s", e)
            return []

    def validate_model_urls_with_playwright(self, market_code):
        """
        Fetches model codes and validates their URLs using Playwright.

        Args:
            market_code (str): The market code to fetch and validate model codes for.

        Returns:
            list: A list of valid model codes.
        """
        model_codes = self.fetch_model_codes(market_code)
        valid_model_codes = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            for model_code in model_codes:
                url = f"https://api.oneweb.mercedes-benz.com/vehicle-deeplinks-api/v1/deeplinks/{market_code}/model-series/{model_code}"
                try:
                    page.goto(url)
                    page.wait_for_load_state("networkidle")
                    logging.info(f"✅ Successfully validated URL for model code: {model_code}")
                    valid_model_codes.append(model_code)
                except Exception as e:
                    logging.error(f"❌ Failed to validate URL for model code: {model_code}. Error: {e}")

            browser.close()

        return valid_model_codes


# Usage of the class
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Replace with your access token and market code
    access_token = "YOUR_ACCESS_TOKEN"  # Replace with the actual access token
    market_code = "IT/it"

    # Create an instance of the class
    api = ModelCodesAPI(access_token)

    # Fetch and validate model codes
    valid_model_codes = api.validate_model_urls_with_playwright(market_code)

    if valid_model_codes:
        print("Valid Passenger Car Model Codes:", valid_model_codes)
    else:
        print("No valid model codes found or an error occurred.")