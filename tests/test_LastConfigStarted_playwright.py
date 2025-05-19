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

def test_last_configuration_started(setup_browser):
    page = setup_browser
    target_url = "https://example.com"  # Replace with the actual URL

    logging.info(f"🌍 Navigating to: {target_url}")
    page.goto(target_url)

    # Example of interacting with the page
    try:
        with allure.step("✅ Accepting cookies"):
            page.click("text=Accept All Cookies")  # Adjust selector as needed
            logging.info("✅ Clicked on accept cookies.")
    except Exception as e:
        allure.attach("❌ Cookie banner not found or already accepted.", name="Cookie Acceptance Error", attachment_type=allure.attachment_type.TEXT)
        logging.error("❌ Failed to accept cookies.")
        pytest.fail("Failed to accept cookies.")

    # Add more test logic here
    # For example, verifying elements, taking screenshots, etc.
    
    allure.attach(page.screenshot(), name="Screenshot after navigation", attachment_type=allure.attachment_type.PNG)

    # Example of verifying an element
    try:
        with allure.step("✅ Verifying element presence"):
            assert page.is_visible("selector-for-element")  # Replace with actual selector
            logging.info("✅ Element is visible.")
    except AssertionError:
        allure.attach("❌ Element not found.", name="Element Verification Error", attachment_type=allure.attachment_type.TEXT)
        logging.error("❌ Element not found.")
        pytest.fail("Element not found.")

    # Finalize test
    logging.info("✅ Test completed successfully.")