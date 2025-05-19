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

def test_last_config_completed(setup_browser):
    page = setup_browser
    target_url = "https://example.com"  # Replace with the actual URL

    logging.info(f"🌍 Navigating to: {target_url}")
    page.goto(target_url)

    # Add your test logic here
    # Example: Check for a specific element
    try:
        page.wait_for_selector("selector-for-element", timeout=10000)
        logging.info("✅ Element found.")
        allure.attach("Element found successfully.", name="Test Result", attachment_type=allure.attachment_type.TEXT)
    except Exception as e:
        logging.error(f"❌ Error: {e}")
        allure.attach(f"Error: {str(e)}", name="Test Failure", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Test failed: {e}")

    # Additional test steps can be added here

    allure.dynamic.description("Test for Last Configuration Completed executed successfully.")