from playwright.sync_api import sync_playwright
import logging
import pytest


def build_playwright_options():
    """
    Builds Playwright browser options.
    """
    return {
        "headless": True,  # Set to True for headless mode
        "args": [
            "--start-maximized",
            "--disable-gpu",
            "--enable-webgl",
            "--incognito",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "user-agent=PlaywrightTestBot/1.0"
        ]
    }


def create_driver():
    """
    Creates a Playwright browser, context, and page.
    """
    playwright = sync_playwright().start()
    options = build_playwright_options()
    browser = playwright.chromium.launch(headless=options["headless"], args=options["args"])
    # Set viewport and screen size for maximized effect
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        screen={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    return playwright, browser, context, page


def restart_driver(browser, playwright):
    """
    Restarts the Playwright browser.
    """
    try:
        browser.close()
    except Exception as e:
        logging.warning(f"⚠️ Failed to close the old browser: {e}")
    return create_driver()


@pytest.fixture
def driver():
    """
    Pytest fixture to initialize and clean up the Playwright browser.
    """
    playwright, browser, context, page = create_driver()
    yield page
    try:
        browser.close()
        playwright.stop()
    except Exception as e:
        logging.warning(f"⚠️ Failed to clean up the browser: {e}")