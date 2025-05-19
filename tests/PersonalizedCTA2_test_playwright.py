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

def test_personalized_cta_2(setup_browser):
    page = setup_browser
    target_url = "https://example.com"  # Replace with the actual URL for the test

    logging.info(f"🌍 Navigating to: {target_url}")
    page.goto(target_url)

    # Example of interacting with the page
    with allure.step("✅ Interacting with the Personalized CTA 2"):
        # Replace with actual selectors and actions
        page.click("selector-for-personalized-cta-2")
        allure.attach(page.screenshot(), name="Personalized CTA 2 Screenshot", attachment_type=allure.attachment_type.PNG)

    # Example of verifying the result
    with allure.step("✅ Verifying the result of Personalized CTA 2"):
        result = page.inner_text("selector-for-result")
        expected_result = "Expected Result"  # Replace with the actual expected result
        assert result == expected_result, f"Expected '{expected_result}', but got '{result}'"

    logging.info("✅ Test for Personalized CTA 2 completed successfully.")