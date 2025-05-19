from playwright.sync_api import sync_playwright
import pytest
import allure
import json
import logging

@pytest.mark.parametrize("test_case", [
    {"test_name": "BFV3", "market_code": "DE/de", "model_code": "A236"},
])
def test_bfv3(test_case):
    test_name = test_case['test_name']
    market_code = test_case.get('market_code', 'BE/nl')
    model_code = test_case.get('model_code', None)

    logging.info(f"Running test case: {json.dumps(test_case, indent=2)}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Navigate to the home page
            page.goto("https://example.com/home")  # Replace with actual URL
            allure.attach(page.content(), name="Home Page Content", attachment_type=allure.attachment_type.HTML)

            # Perform actions specific to BFV3 test case
            # Example: Click on a button
            page.click("selector-for-button")  # Replace with actual selector
            allure.attach(page.content(), name="Post Button Click Content", attachment_type=allure.attachment_type.HTML)

            # Validate results
            assert page.is_visible("selector-for-validation")  # Replace with actual selector

        except Exception as e:
            logging.error(f"Test failed: {e}")
            allure.attach(str(e), name="Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Test failed: {e}")

        finally:
            context.close()
            browser.close()