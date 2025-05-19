from playwright.sync_api import sync_playwright

def fetch_api_data(url, headers=None):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        response = page.request.get(url, headers=headers)
        data = response.json()
        browser.close()
    return data

def post_api_data(url, data, headers=None):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        response = page.request.post(url, json=data, headers=headers)
        result = response.json()
        browser.close()
    return result

def put_api_data(url, data, headers=None):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        response = page.request.put(url, json=data, headers=headers)
        result = response.json()
        browser.close()
    return result

def delete_api_data(url, headers=None):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        response = page.request.delete(url, headers=headers)
        result = response.json()
        browser.close()
    return result