class CTAHandler:
    def __init__(self, page):
        self.page = page

    async def click_cta(self, selector):
        await self.page.click(selector)

    async def is_cta_visible(self, selector):
        return await self.page.is_visible(selector)

    async def get_cta_text(self, selector):
        return await self.page.text_content(selector)

    async def wait_for_cta(self, selector, timeout=5000):
        await self.page.wait_for_selector(selector, timeout=timeout)