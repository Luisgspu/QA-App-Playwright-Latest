from playwright.sync_api import sync_playwright

def create_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        return browser

def create_context(browser):
    context = browser.new_context()
    return context

def create_page(context):
    page = context.new_page()
    return page

def close_browser(browser):
    browser.close()