from playwright.sync_api import Page

class TestDrivePage:
    def __init__(self, page: Page):
        self.page = page
        self.test_drive_button_selector = "selector-for-test-drive-button"  # Update with actual selector
        self.confirmation_message_selector = "selector-for-confirmation-message"  # Update with actual selector

    def navigate_to_test_drive(self):
        self.page.goto("url-for-test-drive-page")  # Update with actual URL

    def click_test_drive_button(self):
        self.page.click(self.test_drive_button_selector)

    def get_confirmation_message(self):
        return self.page.text_content(self.confirmation_message_selector)