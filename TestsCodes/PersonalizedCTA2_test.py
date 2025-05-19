from playwright.sync_api import Page, expect
import allure

class PersonalizedCTA2Test:
    def __init__(self, page: Page):
        self.page = page

    def run(self):
        with allure.step("Navigate to the Home Page"):
            self.page.goto("https://example.com/home")  # Replace with the actual URL

        with allure.step("Verify the presence of Personalized CTA 2"):
            cta_selector = "selector-for-personalized-cta-2"  # Replace with the actual selector
            expect(self.page.locator(cta_selector)).to_be_visible()

        with allure.step("Click on Personalized CTA 2"):
            self.page.locator(cta_selector).click()

        with allure.step("Verify redirection after clicking CTA"):
            expect(self.page).to_have_url("https://example.com/expected-url")  # Replace with the expected URL

        with allure.step("Capture screenshot after clicking CTA"):
            self.page.screenshot(path="screenshot_personalized_cta_2.png")  # Adjust the path as needed

        with allure.step("Verify the content on the redirected page"):
            expect(self.page.locator("selector-for-expected-content")).to_be_visible()  # Replace with the actual selector for expected content