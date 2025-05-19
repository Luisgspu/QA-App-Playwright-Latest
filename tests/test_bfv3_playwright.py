from playwright.sync_api import sync_playwright
import pytest
import json
import logging
from App.VerifyPersonalizationAndCapture import verify_personalization_and_capture
from App.CreateAPIandXHR import create_api_and_xhr

@pytest.fixture(scope="function")
def setup_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()

def run_test(page, test_name, urls):
    test_success = False

    if not urls or 'HOME_PAGE' not in urls or not urls['HOME_PAGE']:
        logging.error(f"❌ Missing HOME_PAGE URL for test '{test_name}'.")
        pytest.fail(f"Missing HOME_PAGE URL for test '{test_name}'")

    try:
        logging.info(f"🌍 Navigating to HOME_PAGE: {urls['HOME_PAGE']}")
        page.goto(urls['HOME_PAGE'])
        page.wait_for_load_state("networkidle")
    except Exception as e:
        logging.error(f"❌ Error navigating to HOME_PAGE: {e}")
        pytest.fail(f"Error navigating to HOME_PAGE: {e}")

    # Additional test logic goes here...

    # Example of verifying personalization
    test_success = verify_personalization_and_capture(page, test_name)

    if not test_success:
        failure_message = f"❌ Test '{test_name}' failed."
        logging.error(failure_message)
        pytest.fail(failure_message)

@pytest.mark.parametrize("test_case", [
    {"test_name": "BFV3", "urls": {"HOME_PAGE": "https://example.com/home"}}  # Replace with actual URLs
])
def test_bfv3_playwright(test_case, setup_browser):
    test_name = test_case['test_name']
    urls = test_case.get('urls', {})
    
    logging.info(f"Running test case: {json.dumps(test_case, indent=2)}")
    
    run_test(setup_browser, test_name, urls)