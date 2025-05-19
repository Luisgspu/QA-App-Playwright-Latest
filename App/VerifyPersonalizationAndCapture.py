import logging
import allure
import os
import pytest
from playwright.sync_api import Page

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
                logging.info(f"ℹ️ Captured XHR data: {xhr_data}")

                for response in xhr_data:
                    campaigns = response.get("body", {}).get("campaignResponses", [])
                    for campaign in campaigns:
                        campaign_name = campaign.get("campaignName", "Unknown Campaign")
                        user_group = campaign.get("userGroup", "Unknown UserGroup")
                        experience_name = campaign.get("experienceName", "Unknown Experience")

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
            except Exception as e:
                logging.error(f"❌ Failed to check userGroup in XHR responses: {e}")
                allure.attach(f"❌ Failed to check userGroup in XHR responses: {e}", name="XHR Error", attachment_type=allure.attachment_type.TEXT)
                return False

        # Verify the personalized image
        with allure.step("🔍 Verifying personalized image..."):
            try:
                expected_src = "/content/dam/hq/personalization/campaignmodule/" if test_name in ["BFV1", "BFV2", "BFV3"] else "/images/dynamic/europe/"
                selector = "[data-component-name='hp-campaigns']" if ".co.uk" not in urls['HOME_PAGE'] else "body > div.root.responsivegrid.owc-content-container > div > div.responsivegrid.ng-content-root.aem-GridColumn.aem-GridColumn--default--12 > div > div:nth-child(16)"

                # Scroll to the element if the market is UK
                if ".co.uk" in urls['HOME_PAGE']:
                    with allure.step("📜 Scrolling to the UK-specific element..."):
                        element_to_scroll = page.locator(selector)
                        element_to_scroll.scroll_into_view_if_needed()
                        logging.info(f"✅ Scrolled to element: {selector}")

                # Wait for the images to load and check if any match the expected src
                images = page.locator(f"{selector} img")
                images.wait_for(timeout=10000)
                matching_src = None
                for img in images.element_handles():
                    src = img.get_attribute("src")
                    if src and expected_src in src:
                        matching_src = src
                        break

                if not matching_src:
                    raise Exception(f"No matching image found with expected src: {expected_src}")

                # Attach the found src to the Allure report
                found_srcs = [img.get_attribute("src") for img in images.element_handles()]
                allure.attach("\n".join(found_srcs), name="All Found Image Sources", attachment_type=allure.attachment_type.TEXT)
                allure.attach(matching_src, name="Matching Image Source", attachment_type=allure.attachment_type.TEXT)

                with allure.step(f"✅ Personalized image with expected src '{expected_src}' was applied correctly."):
                    logging.info(f"✅ Found matching image with src: {matching_src}")

                # Capture screenshot
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}_attempt_{attempt}.png")
                page.screenshot(path=screenshot_path)
                attach_screenshot_to_allure(screenshot_path)

                test_success = True

            except Exception as e:
                # Capture screenshot on failure
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}_attempt_{attempt}_error.png")
                page.screenshot(path=screenshot_path)
                attach_screenshot_to_allure(screenshot_path)

                with allure.step(f"❌ Image not found in the specified selector. Error: {e}"):
                    logging.error(f"❌ Image not found in the specified selector. Error: {e}")
                    allure.dynamic.label("defect", "Wrong Personalization Image")
                    allure.dynamic.tag("Personalization Issue")
                    allure.attach(f"Expected src: {expected_src}", name="Expected Image Source", attachment_type=allure.attachment_type.TEXT)
                    allure.attach(f"Error: {e}", name="Image Verification Error", attachment_type=allure.attachment_type.TEXT)
                return False

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