# Standard Library Imports
import os
import time
import json
import logging
import hashlib
import pytest
import allure
from playwright.sync_api import sync_playwright

# Local Module Imports
from Utils.vehicle_api import VehicleAPI
from Utils.VerifyPersonalizationAndCapture import verify_personalization_and_capture
from Utils.CreateAPIandXHR import create_api_and_xhr
from Utils.CookiesHandler import CookieHandler
from Utils.XHRResponseCapturer import XHRResponseCapturer
from Tests import test_bfv1_playwright
from Tests import test_bfv2_playwright
from Tests import test_bfv3_playwright
from Tests import test_LastConfigStarted_playwright
from Tests import test_LastConfigCompleted_playwright
from Tests import test_LastSeenSRP_playwright
from Tests import test_LastSeenPDP_playwright


# Test mapping
test_mapping = {
    "BFV1": test_bfv1_playwright.BFV1Test,
    "BFV2": test_bfv2_playwright.BFV2Test,
    "BFV3": test_bfv3_playwright.BFV3Test,
    "Last Configuration Started": test_LastConfigStarted_playwright.LCStartedTest,
    "Last Configuration Completed": test_LastConfigCompleted_playwright.LCCompletedTest,
    "Last Seen SRP": test_LastSeenSRP_playwright.LSeenSRPTest,
    "Last Seen PDP": test_LastSeenPDP_playwright.LSeenPDPTest
  
}

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(message)s")

@pytest.fixture(scope="function")
def screenshot_dir():
    screenshot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Tests")
    os.makedirs(screenshot_dir, exist_ok=True)
    return screenshot_dir

def run_test(page, test_name, market_code, model_code, model_name, body_type, attempt, urls, api_and_xhr, screenshot_dir):
    vehicle_api, xhr_capturer = api_and_xhr
    test_success = False

    if not urls or 'HOME_PAGE' not in urls or not urls['HOME_PAGE']:
        allure.attach(f"❌ Could not fetch valid URLs for test '{test_name}' (market: {market_code}, model: {model_code})")
        pytest.fail(f"Missing HOME_PAGE URL for test '{test_name}'")


    # BFV Logic
    if 'CONFIGURATOR' not in urls or not urls['CONFIGURATOR']:
        if test_name in ["BFV1", "BFV2", "BFV3", "Last Configuration Started", "Last Configuration Completed"]:
            message = f"❌ Skipping test '{test_name}' due to lack of CONFIGURATOR URL."
            allure.dynamic.description(message)
            pytest.skip(message)

    if 'ONLINE_SHOP' not in urls or not urls['ONLINE_SHOP']:
        if test_name in ["BFV2", "BFV3", "Last Seen PDP", "Last Seen SRP"]:
            message = f"❌ Skipping test '{test_name}' due to lack of ONLINE_SHOP URL."
            allure.dynamic.description(message)
            pytest.skip(message)

    if 'TEST_DRIVE' not in urls or not urls['TEST_DRIVE']:
        if test_name == "BFV3":
            message = f"❌ Skipping test '{test_name}' due to lack of TEST_DRIVE URL."
            allure.dynamic.description(message)
            pytest.skip(message)
    
    try:
        with allure.step(f"🌍 Navigating to HOME_PAGE: {urls['HOME_PAGE']}"):
            page.goto(urls['HOME_PAGE'])
            page.wait_for_load_state("domcontentloaded")
            logging.info(f"🌍 Navigated to: {urls['HOME_PAGE']}")
    except Exception as e:
        logging.error(f"❌ Error navigating to HOME_PAGE: {e}")
        pytest.fail(f"Error navigating to HOME_PAGE: {e}")

    # Accept cookies if necessary
    cookie_handler = CookieHandler(page)
    cookie_handler.accept_cookies()

    # Execute test
    if test_name in test_mapping:
        test_instance = test_mapping[test_name](page, urls)
        test_instance.run()
        allure.step(f"✅ {test_name} test Started.")

        test_success = verify_personalization_and_capture(
            page, test_name, model_name, body_type, attempt, screenshot_dir,
            test_success, xhr_capturer, urls
        )

    if not test_success:
        failure_message = f"❌ Test '{test_name}' failed."

        # Dynamically determine the failure reason
        if "Control Group Fail" in failure_message:
            allure.dynamic.issue("Control Group Fail")
            allure.dynamic.severity(allure.severity_level.CRITICAL)
            logging.error("❌ Categorized as Control Group Fail.")
        elif "Wrong Personalization Image" in failure_message:
            allure.dynamic.issue("Wrong Personalization Image")
            allure.dynamic.severity(allure.severity_level.BLOCKER)
            logging.error("❌ Categorized as Wrong Personalization Image.")
        elif "Cookie Acceptance Failure" in failure_message:
            allure.dynamic.issue("Cookie Acceptance Failure")
            allure.dynamic.severity(allure.severity_level.MINOR)
            logging.error("❌ Categorized as Cookie Acceptance Failure.")
        else:
            allure.dynamic.issue("General Test Failure")
            allure.dynamic.severity(allure.severity_level.NORMAL)
            logging.error("❌ Categorized as General Test Failure.")

        logging.error(failure_message)
        allure.attach(failure_message, name="Test Failure", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(failure_message)

# Manually defined test cases
manual_test_cases = [

    
{"test_name": "Last Configuration Completed", "market_code": "DE/de", "model_code": "H243-fl"},

        
       
        

]

# Fetch dynamic test cases for manual model codes
dynamic_test_cases = []
vehicle_api = VehicleAPI("YOUR_ACCESS_TOKEN")  # Replace with your actual access token

for manual_case in manual_test_cases:
    market_code = manual_case["market_code"]
    test_name = manual_case["test_name"]
    model_code = manual_case.get("model_code", None)

    fetched_cases = vehicle_api.fetch_models_for_market(market_code, test_name, model_code=model_code)
    if fetched_cases:
        for case in fetched_cases:
            if "urls" in case:
                for key, url in case["urls"].items():
                    if url and key == "HOME_PAGE":
                        case["urls"][key] = f"{url}?usecaselivetest=true"

        if model_code:
            manual_case["urls"] = fetched_cases[0].get("urls", {})
            manual_case["model_name"] = fetched_cases[0].get("model_name", None)
            manual_case["body_type"] = fetched_cases[0].get("body_type", None)
        else:
            dynamic_test_cases.extend(fetched_cases)
    else:
        logging.warning(f"⚠️ No URLs found for manual case: {manual_case}")

# Combine manual and dynamic test cases
all_test_cases = manual_test_cases + dynamic_test_cases

# Mapping for campaign substring filters
CAMPAIGN_FILTERS = {
    "BFV1": "best-fitting-vehicle",
    "BFV2": "best-fitting-vehicle",
    "BFV3": "best-fitting-vehicle",
    "Last Configuration Started": "last-configuration",
    "Last Configuration Completed": "last-configuration",
    "Last Seen SRP": "dcp-last-seen-pdp-srp",
    "Last Seen PDP": "dcp-last-seen-pdp-srp",
    
    # Add more as needed
}

@pytest.mark.parametrize("test_case", all_test_cases)
def test_run(test_case, screenshot_dir):
    """
    Runs a test for each test case, either manually defined or dynamically fetched.
    """
    test_name = test_case['test_name']
    market_code = test_case.get('market_code', 'BE/nl')
    model_code = test_case.get('model_code', None)
    model_name = test_case.get('model_name', None)
    body_type = test_case.get('body_type', None)
    urls = test_case.get('urls', {})

    logging.info(f"Running test case: {json.dumps(test_case, indent=2)}")

    if not urls or 'HOME_PAGE' not in urls or not urls['HOME_PAGE']:
        logging.error(f"❌ Missing HOME_PAGE URL for test '{test_name}' (market: {market_code}, model: {model_code}).")
        allure.attach(f"❌ Missing HOME_PAGE URL for test '{test_name}' (market: {market_code}, model: {model_code}).")
        return

    uid_raw = f"{test_name}_{market_code}_{model_code or 'unknown'}"
    uid_hashed = hashlib.md5(uid_raw.encode()).hexdigest()
    allure.dynamic.id(uid_hashed)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # or False for headed
            args=[
                "--start-maximized",
                "--disable-gpu",
                "--enable-webgl",
                "--incognito",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--window-size=2560,1440",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--disable-extensions",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "--disable-features=IsolateOrigins,site-per-process",
                "--blink-settings=imagesEnabled=true"
            ]
        )
        context = browser.new_context(
            viewport={"width": 2560, "height": 1440},
            screen={"width": 2560, "height": 1440}
        )
        
        page = context.new_page()
        # Use the mapping to get the correct substring for filtering
        substring = CAMPAIGN_FILTERS.get(test_name, "")
        xhr_capturer = XHRResponseCapturer(
            page,
            target_url_filter="evergage.com/api2/event",
            target_campaign_name_substring=substring
        )

        try:
            allure.dynamic.parent_suite(f"{market_code}")
            allure.dynamic.suite(f"{test_name}")
            allure.dynamic.sub_suite(f"{model_code or 'N/A'} - {model_name or 'N/A'} ({body_type or 'N/A'})")

            allure.dynamic.tag(test_name)
            allure.dynamic.tag(market_code)
            if model_code:
                allure.dynamic.tag(model_code)
            if body_type:
                allure.dynamic.tag(body_type)
            if model_name:
                allure.dynamic.tag(model_name)

            with allure.step(f"🌐 Fetched URLs for {model_name or 'N/A'} ({body_type or 'N/A'})"):
                allure.attach(
                    json.dumps(urls, indent=2),
                    name=f"URLs for {model_name or 'N/A'} ({body_type or 'N/A'})",
                    attachment_type=allure.attachment_type.JSON
                )

            base_test_name = test_name.split(" - ")[0]

            try:
                # If you use create_api_and_xhr, update it to accept and use xhr_capturer if needed
                api_and_xhr = (VehicleAPI("YOUR_ACCESS_TOKEN"), xhr_capturer)
                if api_and_xhr is None or api_and_xhr[1] is None:
                    logging.error("❌ Failed to initialize API and XHR capturer.")
                    allure.attach("❌ Failed to initialize API and XHR capturer.", name="Initialization Error", attachment_type=allure.attachment_type.TEXT)
                    return
                if base_test_name in test_mapping:
                    run_test(page, base_test_name, market_code, model_code, model_name, body_type, 1, urls, api_and_xhr, screenshot_dir)
                else:
                    raise ValueError(f"❌ Test logic for '{test_name}' is not defined in test_mapping.")
            except Exception as e:
                logging.error(f"❌ Test failed for model: {model_name or 'N/A'} ({body_type or 'N/A'}). Error: {e}")
                allure.attach(
                    f"Error: {str(e)}",
                    name=f"Error for {model_name or 'N/A'} ({body_type or 'N/A'})",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise
        finally:
            browser.close()
            logging.info("✅ Browser closed after test.")