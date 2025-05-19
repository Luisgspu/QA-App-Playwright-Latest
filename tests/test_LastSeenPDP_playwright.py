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

    logging.info(f"🌍 Navigating to: {target_url}")
    page.goto(target_url)

    with allure.step("📸 Taking a screenshot of the Last Seen PDP"):
        screenshot_path = "screenshots/last_seen_pdp.png"
        page.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="Last Seen PDP Screenshot", attachment_type=allure.attachment_type.PNG)

    # Example of verifying an element on the page
    with allure.step("✅ Verifying the presence of the product title"):
        product_title_selector = "h1.product-title"  # Replace with the actual selector
        assert page.is_visible(product_title_selector), "Product title is not visible on the page."

    # Example of capturing XHR responses
    with allure.step("📁 Capturing XHR responses"):
        page.on("response", lambda response: logging.info(f"XHR Response: {response.url} - Status: {response.status}"))

    # Additional test logic goes here

    logging.info("✅ Test completed successfully.")