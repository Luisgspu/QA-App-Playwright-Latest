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

def test_last_seen_srp(setup_browser):
    page = setup_browser
    target_url = "https://example.com/home"  # Replace with the actual URL

    logging.info("🌍 Navigating to HOME_PAGE")
    page.goto(target_url)
    assert page.title() == "Expected Title"  # Replace with the expected title

    # Example of interacting with the page
    logging.info("✅ Interacting with the page")
    page.click("selector-for-element")  # Replace with the actual selector

    # Capture screenshot
    screenshot_path = "screenshot.png"
    page.screenshot(path=screenshot_path)
    allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)

    # Example of verifying an element
    element = page.query_selector("selector-for-verification")  # Replace with the actual selector
    assert element is not None, "Element not found!"

    # Example of capturing XHR responses
    page.on("response", lambda response: logging.info(f"XHR Response: {response.url} - {response.status}"))

    # Final assertions and cleanup
    logging.info("✅ Test completed successfully")