from playwright.sync_api import expect, Locator
from pages.base_page import BasePage

class FeedPage(BasePage):
    
    def __init__(self, page):
        super().__init__(page)
        # === SELECTORS (Robust CSS selectors matching live DOM) ===
        self.wrapper = page.locator(".posts-page, .feed-layout, main")
        self.new_post_textarea = page.locator("textarea.create-textarea, textarea[placeholder*='What are you building']")
        self.post_submit_btn = page.locator("button.btn-post, button:has-text('Post')")
        self.post_card = page.locator("div.post-card")
        
        # Action buttons inside post cards (defined as selector strings for scoping)
        self.like_btn = "button.post-action-btn:has(i.bi-heart, i.bi-heart-fill)"
        self.comment_btn = "button.post-action-btn:has(i.bi-chat)"
        
        # Page state indicators
        self.empty_state = page.locator(".text-muted:has-text('No posts yet')").or_(page.locator("text=/No posts yet|Be the first/i"))
        self.loading_indicator = page.locator(".spinner, .loading-spinner").or_(page.locator("text=/Loading|Fetching/i"))
        
    def navigate(self):
        self.goto("/student/feed")
        
    def wait_for_feed_loaded(self, timeout=15000):
        """Wait for posts to appear OR empty state"""
        try:
            self.loading_indicator.wait_for(state="hidden", timeout=3000)
        except Exception:
            pass
            
        # Either empty state shows or posts exist
        if self.empty_state.is_visible():
            return "empty"
            
        try:
            self.post_card.first.wait_for(state="visible", timeout=timeout)
            return "loaded"
        except Exception:
            if self.empty_state.is_visible():
                return "empty"
            raise

    def create_post(self, content: str):
        """Create a new feed post and verify it appears at the top"""
        self.new_post_textarea.wait_for(state="visible")
        self.new_post_textarea.fill(content)
        self.post_submit_btn.wait_for(state="visible")
        self.post_submit_btn.click()
        self.page.wait_for_timeout(1000)
        
        # Verify new post appears at top
        first_post_content = self.post_card.first.locator(".post-body")
        expect(first_post_content).to_contain_text(content, timeout=10000)
        
    def click_like_on_first_post(self):
        """Like the first post and verify count increments"""
        first_post = self.post_card.first
        first_post.wait_for(state="visible")
        
        like_btn_locator = first_post.locator(self.like_btn)
        like_btn_locator.wait_for(state="visible")
        
        # If already liked (has class 'liked'), click it to unlike first
        class_attr = like_btn_locator.get_attribute("class") or ""
        if "liked" in class_attr:
            like_btn_locator.click()
            self.page.wait_for_timeout(1000)
            
        initial_count = self._extract_like_count(first_post)
        
        like_btn_locator.click()
        self.page.wait_for_timeout(1000) # Quick wait for React UI sync
        
        new_count = self._extract_like_count(first_post)
        assert new_count == initial_count + 1, f"Like count didn't increment correctly: {initial_count} -> {new_count}"
        
    def _extract_like_count(self, post_locator) -> int:
        """Helper: extract numeric like count from post"""
        # Try Method 1: Extract count from like button span
        try:
            span_locator = post_locator.locator("button.post-action-btn:has(i.bi-heart, i.bi-heart-fill) span")
            if span_locator.is_visible():
                txt = span_locator.text_content().strip()
                if txt.isdigit():
                    return int(txt)
        except Exception:
            pass
            
        # Try Method 2: Extract count from post stats label (e.g. "2 likes")
        try:
            stats_locator = post_locator.locator(".post-stats span:has-text('like')")
            if stats_locator.is_visible():
                text_content = stats_locator.text_content()
                return int(''.join(filter(str.isdigit, text_content)))
        except Exception:
            pass
            
        return 0
        
    def get_first_post_content(self) -> str:
        """Extract content text of first post"""
        self.post_card.first.wait_for(state="visible")
        return self.post_card.first.locator(".post-body").text_content().strip()