from playwright.sync_api import Page, expect
import allure

class PersonalizedCTA3Test:
    def __init__(self, page: Page):
        self.page = page

    def run(self):
        with allure.step("🌍 Navigating to the Home Page"):
            self.page.goto("https://example.com")  # Replace with the actual URL

        with allure.step("✅ Verifying the Personalized CTA 3"):
            cta_selector = "selector-for-personalized-cta-3"  # Replace with the actual selector
            expect(self.page.locator(cta_selector)).to_be_visible()
            allure.attach("CTA 3 is visible", name="CTA 3 Verification", attachment_type=allure.attachment_type.TEXT)

        with allure.step("📸 Taking a screenshot of the Personalized CTA 3"):
            screenshot_path = "screenshots/personalized_cta_3.png"  # Adjust the path as needed
            self.page.screenshot(path=screenshot_path)
            allure.attach_file(screenshot_path, name="Personalized CTA 3 Screenshot", attachment_type=allure.attachment_type.PNG)