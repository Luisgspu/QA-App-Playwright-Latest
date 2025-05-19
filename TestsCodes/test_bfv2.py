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
    target_url = "https://example.com"  # Replace with the actual URL for the test

    logging.info(f"🌍 Navigating to: {target_url}")
    page.goto(target_url)

    # Example of interacting with the page
    page.fill("input[name='search']", "Test Search")
    page.click("button[type='submit']")

    # Wait for results to load
    page.wait_for_selector(".result")

    # Capture screenshot
    screenshot_path = "screenshot_bfv2.png"
    page.screenshot(path=screenshot_path)
    allure.attach.file(screenshot_path, name="BFV2 Screenshot", attachment_type=allure.attachment_type.PNG)

    # Validate results
    results = page.query_selector_all(".result")
    assert len(results) > 0, "No results found."

    logging.info("✅ BFV2 test completed successfully.")