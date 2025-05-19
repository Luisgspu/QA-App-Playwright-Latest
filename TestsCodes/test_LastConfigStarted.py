from playwright.sync_api import sync_playwright
import pytest
import allure
import json
import logging

@pytest.mark.parametrize("test_case", [
    {"market_code": "DE/de", "model_code": "A236"},
])
def test_last_configuration_started(test_case):
    market_code = test_case["market_code"]
    model_code = test_case["model_code"]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Navigate to the home page
            page.goto("https://example.com/home")  # Replace with actual URL
            logging.info(f"Navigated to HOME_PAGE for model {model_code} in market {market_code}")

            # Perform actions for the Last Configuration Started test
            # Example: Click on a button, fill a form, etc.
            page.click("selector-for-button")  # Replace with actual selector
            logging.info("Clicked on the button for Last Configuration Started test.")

            # Capture and attach screenshot
            screenshot_path = f"screenshots/last_config_started_{model_code}.png"
            page.screenshot(path=screenshot_path)
            allure.attach.file(screenshot_path, name="Last Configuration Started Screenshot", attachment_type=allure.attachment_type.PNG)

            # Validate results
            result = page.inner_text("selector-for-result")  # Replace with actual selector
            expected_result = "Expected Result"  # Replace with actual expected result
            assert result == expected_result, f"Expected '{expected_result}', but got '{result}'"

            logging.info("Last Configuration Started test passed.")

        except Exception as e:
            logging.error(f"Test failed: {e}")
            allure.attach(str(e), name="Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Test failed: {e}")

        finally:
            context.close()
            browser.close()