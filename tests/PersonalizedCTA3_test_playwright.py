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

def test_personalized_cta_3(setup_browser):
    page = setup_browser
    target_url = "https://example.com"  # Replace with the actual URL for the test

    logging.info(f"🌍 Navigating to: {target_url}")
    page.goto(target_url)

    # Example of interacting with the page
    with allure.step("✅ Interacting with the Personalized CTA"):
        cta_selector = "selector-for-personalized-cta"  # Replace with the actual selector
        page.click(cta_selector)

    # Example of verifying the result
    with allure.step("✅ Verifying the result"):
        result_selector = "selector-for-result"  # Replace with the actual selector
        result_text = page.inner_text(result_selector)
        expected_text = "Expected Result"  # Replace with the expected result
        assert result_text == expected_text, f"Expected '{expected_text}', but got '{result_text}'"

    # Attach a screenshot to Allure
    screenshot_path = "screenshot.png"
    page.screenshot(path=screenshot_path)
    allure.attach.file(screenshot_path, name="Personalized CTA 3 Screenshot", attachment_type=allure.attachment_type.PNG)

    logging.info("✅ Test completed successfully.")