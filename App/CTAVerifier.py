class CTAVerifier:
    def __init__(self, page):
        self.page = page

    async def verify_cta_presence(self, cta_selector):
        cta_element = await self.page.query_selector(cta_selector)
        if cta_element is None:
            raise AssertionError(f"CTA element with selector '{cta_selector}' not found.")
        return True

    async def verify_cta_text(self, cta_selector, expected_text):
        cta_element = await self.page.query_selector(cta_selector)
        if cta_element is None:
            raise AssertionError(f"CTA element with selector '{cta_selector}' not found.")
        
        actual_text = await cta_element.inner_text()
        if actual_text != expected_text:
            raise AssertionError(f"Expected CTA text '{expected_text}', but got '{actual_text}'.")
        return True

    async def verify_cta_clickable(self, cta_selector):
        cta_element = await self.page.query_selector(cta_selector)
        if cta_element is None:
            raise AssertionError(f"CTA element with selector '{cta_selector}' not found.")
        
        is_enabled = await cta_element.evaluate("element => !element.disabled")
        if not is_enabled:
            raise AssertionError(f"CTA element with selector '{cta_selector}' is not clickable.")
        return True