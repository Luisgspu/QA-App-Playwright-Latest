from playwright.sync_api import sync_playwright
import pytest
import allure
import json
import logging

@pytest.fixture(scope="function")
def setup_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()

def test_last_seen_pdp(setup_browser):
    page = setup_browser
    target_url = "https://example.com/last-seen-pdp"  # Replace with the actual URL

    logging.info(f"Navigating to {target_url}")
    page.goto(target_url)

    # Example of interaction with the page
    try:
        page.wait_for_selector("selector-for-element")  # Replace with actual selector
        logging.info("Element found, proceeding with test.")
        
        # Perform actions and assertions here
        # Example: page.click("selector-for-button")
        
        allure.attach(page.screenshot(), name="Last Seen PDP Screenshot", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        logging.error(f"Error during test: {e}")
        allure.attach(f"Error: {str(e)}", name="Test Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Test failed due to error: {e}")

    # Additional assertions can be added here
    assert True  # Replace with actual assertions based on test requirements