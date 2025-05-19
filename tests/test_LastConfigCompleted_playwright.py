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

    # Example of interacting with the page
    try:
        page.wait_for_selector("selector-for-element")  # Replace with actual selector
        logging.info("✅ Element found.")
    except Exception as e:
        logging.error(f"❌ Error finding element: {e}")
        allure.attach(f"Error finding element: {str(e)}", name="Element Finding Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Error finding element: {e}")

    # Additional test logic goes here

    # Example of attaching a screenshot
    screenshot_path = "screenshot.png"
    page.screenshot(path=screenshot_path)
    allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)

    # Final assertions and cleanup
    assert True  # Replace with actual assertions as needed