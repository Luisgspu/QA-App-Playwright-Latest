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

def test_bfv2(setup_browser):
    page = setup_browser
    target_url = "https://example.com"  # Replace with the actual URL for the BFV2 test

    logging.info(f"🌍 Navigating to: {target_url}")
    page.goto(target_url)

    # Example of interacting with the page
    with allure.step("✅ Interacting with the page"):
        page.click("selector-for-element")  # Replace with actual selector
        allure.attach(page.screenshot(), name="Screenshot after interaction", attachment_type=allure.attachment_type.PNG)

    # Example of verifying a condition
    assert page.title() == "Expected Title"  # Replace with the expected title

    # Attach any additional information to Allure
    allure.attach(json.dumps({"key": "value"}, indent=2), name="Test Data", attachment_type=allure.attachment_type.JSON)

    logging.info("✅ BFV2 test completed successfully.")