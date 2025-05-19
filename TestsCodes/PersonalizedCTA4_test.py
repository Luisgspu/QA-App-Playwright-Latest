from playwright.sync_api import Page, expect
import allure

class PersonalizedCTA4Test:
    def __init__(self, page: Page, urls: dict):
        self.page = page
        self.urls = urls

    def run(self):
        with allure.step("Navigating to HOME_PAGE"):
            self.page.goto(self.urls['HOME_PAGE'])
            expect(self.page).to_have_title("Expected Title")  # Replace with the actual expected title

        with allure.step("Verifying Personalized CTA 4"):
            cta_selector = "selector-for-personalized-cta-4"  # Replace with the actual selector
            expect(self.page.locator(cta_selector)).to_be_visible()
            allure.attach(self.page.screenshot(), name="Personalized CTA 4 Screenshot", attachment_type=allure.attachment_type.PNG)

        with allure.step("Performing action on Personalized CTA 4"):
            self.page.click(cta_selector)
            # Add any additional verification or actions needed after clicking the CTA

        with allure.step("Final verification after CTA action"):
            # Add any final checks or assertions needed after the action
            pass  # Replace with actual verification logic if needed