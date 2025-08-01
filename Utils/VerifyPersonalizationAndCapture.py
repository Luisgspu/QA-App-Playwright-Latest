import logging
import allure
import os
import pytest
from Utils.ScreenshotHandler import ScreenshotHandler
from playwright.sync_api import Page
from Utils.ImageVerifier import ImageVerifier
from Utils.XHRResponseCapturer import XHRResponseCapturer  # Assuming this is the correct import for your XHR capturer

def verify_personalization_and_capture(
        page: Page, test_name: str, model_name: str, body_type: str, attempt: int, screenshot_dir: str,
        test_success: bool, xhr_capturer, urls: dict):
    """
    Verifies the personalized image and captures XHR responses and screenshots.
    """
    try:
        # Check userGroup in XHR responses
        with allure.step("🔍 Checking userGroup in XHR responses..."):
            try:
                xhr_data = xhr_capturer.get_captured_data()
                if xhr_data:
                    import json
                    allure.attach(json.dumps(xhr_data, indent=2, ensure_ascii=False), name="XHR Responses", attachment_type=allure.attachment_type.JSON)
                    # Iterate over all campaigns in all responses and log the full campaign response
                    for response in xhr_data:
                        campaigns = response.get("body", {}).get("campaignResponses", [])
                        for campaign in campaigns:
                            campaign_name = campaign.get("campaignName", "Unknown Campaign")
                            user_group = campaign.get("userGroup", "Unknown UserGroup")
                            experience_name = campaign.get("experienceName", "Unknown Experience")

                            # Log the full campaign response
                            logging.info(f"Full campaign response: {json.dumps(campaign, indent=2, ensure_ascii=False)}")

                            if "Control Group" in experience_name or user_group.lower() == "control":
                                with allure.step(f"❌ Campaign '{campaign_name}' is in the Control Group. Retrying test."):
                                    message = f"❌ Test '{test_name}' failed because the campaign was identified as part of the Control Group."
                                    allure.dynamic.label("defect", "Control Group Fail")
                                    allure.dynamic.tag("Control Group Issue")
                                    pytest.fail(message)
                                    return False
                            else:
                                with allure.step(f"✅ Campaign '{campaign_name}' has userGroup: {user_group} and experienceName: {experience_name}."):
                                    logging.info(f"✅ Campaign '{campaign_name}' has userGroup: {user_group} and experienceName: {experience_name}.")
                else:
                    message = (
                        f"❌ No XHR campaign data was captured for test '{test_name}'.\n"
                        f"Expected campaign substring: '{xhr_capturer.TARGET_CAMPAIGN_NAME_SUBSTRING}'"
                    )
                    allure.attach(message, name="No XHR Data", attachment_type=allure.attachment_type.TEXT)
                    logging.error(message)
                    return False
            except Exception as e:
                logging.error(f"❌ Failed to check userGroup in XHR responses: {e}")
                allure.attach(f"❌ Failed to check userGroup in XHR responses: {e}", name="XHR Error", attachment_type=allure.attachment_type.TEXT)
                return False

        # Verify the personalized image
        with allure.step("🔍 Verifying personalized image..."):
            try:
                expected_src = "/content/dam/hq/personalization/campaignmodule/" if test_name in ["BFV1", "BFV2", "BFV3"] else "/images/dynamic/europe/"
                selector = "[data-component-name='hp-campaigns']" 
                
                # Scroll to the element if the market is UK
                if ".co.uk" in urls['HOME_PAGE']:
                    with allure.step("📜 Scrolling to the UK-specific element..."):
                        element_to_scroll = page.locator(selector)
                        element_to_scroll.scroll_into_view_if_needed()
                        logging.info(f"✅ Scrolled to element: {selector}")

                # Capture screenshot
                logging.info("📸 Taking screenshot...")
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}_attempt_{attempt}.png")

                try:
                    ScreenshotHandler.scroll_and_capture_section(page, screenshot_path)
                    logging.info(f"✅ Screenshot saved and attached at: {screenshot_path}")
                except Exception as e:
                    logging.error(f"❌ Failed to capture or attach screenshot: {e}")
                    
                verifier = ImageVerifier(page)
                found = verifier.verify_image("[data-component-name='hp-campaigns'] img", expected_src, test_name)
                if not found:
                    raise Exception(f"No matching image found with expected src: {expected_src} in the first two images.")

                
                test_success = True

            except Exception as e:
                # Capture screenshot
                logging.info("📸 Taking screenshot...")
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}_attempt_{attempt}.png")

                try:
                    ScreenshotHandler.scroll_and_capture_section(page, screenshot_path)
                    logging.info(f"✅ Screenshot saved and attached at: {screenshot_path}")
                except Exception as e2:
                    logging.error(f"❌ Failed to capture or attach screenshot: {e2}")

        return test_success

    except Exception as e:
        logging.error(f"❌ Error in verify_personalization_and_capture: {e}")
        allure.attach(f"❌ Error in verify_personalization_and_capture: {e}", name="Verify Personalization Error", attachment_type=allure.attachment_type.TEXT)
        return False


def attach_screenshot_to_allure(screenshot_path):
    try:
        logging.info(f"📸 Attaching screenshot to Allure: {screenshot_path}")
        with open(screenshot_path, 'rb') as file:
            allure.attach(file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        logging.error(f"❌ Error attaching screenshot to Allure: {e}")