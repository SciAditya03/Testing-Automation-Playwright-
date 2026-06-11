from playwright.sync_api import Page, expect, Locator
from config import Config

class BasePage:
    """Reusable helpers for all page objects"""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = Config.BASE_URL
        
    def goto(self, path: str):
        """Navigate to relative path"""
        self.page.goto(f"{self.base_url}{path}")
        self.page.wait_for_load_state("networkidle")
        
    def wait_for_element(self, locator: Locator, state="visible", timeout=None):
        """Explicit wait with configurable timeout"""
        locator.wait_for(state=state, timeout=timeout or Config.DEFAULT_TIMEOUT)
        
    def click_with_wait(self, locator: Locator, post_click_url=None):
        """Click and optionally wait for navigation"""
        if post_click_url:
            with self.page.expect_navigation(url=f"*{post_click_url}"):
                locator.click()
        else:
            locator.click()
            self.page.wait_for_load_state("networkidle")
            
    def get_text_content(self, locator: Locator) -> str:
        """Safely extract text"""
        self.wait_for_element(locator)
        return locator.text_content().strip()