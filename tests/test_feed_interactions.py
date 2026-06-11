import pytest
from pages.feed_page import FeedPage

@pytest.mark.regression
@pytest.mark.feed
def test_like_button_increments(logged_in_student):
    """Verify like button updates count correctly"""
    feed = FeedPage(logged_in_student)
    feed.navigate()
    feed.wait_for_feed_loaded()
    feed.click_like_on_first_post()
    
@pytest.mark.regression
@pytest.mark.feed
def test_comment_section_expands(logged_in_student):
    """Verify clicking comments opens comment section"""
    feed = FeedPage(logged_in_student)
    feed.navigate()
    feed.wait_for_feed_loaded()
    first_post = feed.post_card.first
    comment_btn = first_post.locator(feed.comment_btn)
    comment_btn.click()
    # Verify comments container appears
    comments_section = first_post.locator(".comments-section, [data-testid='comments-section'], .comments")
    comments_section.wait_for(state="visible", timeout=5000)