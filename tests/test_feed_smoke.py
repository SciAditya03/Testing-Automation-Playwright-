import pytest
from pages.feed_page import FeedPage

@pytest.mark.smoke
@pytest.mark.feed
def test_feed_loads_with_posts(logged_in_student):
    """Verify Feed page loads and shows posts or empty state"""
    feed = FeedPage(logged_in_student)
    feed.navigate()
    status = feed.wait_for_feed_loaded()
    assert status in ["loaded", "empty"], f"Feed failed to load, status: {status}"
    
@pytest.mark.smoke
@pytest.mark.feed
def test_create_post_flow(logged_in_student):
    """Verify student can create a new post"""
    feed = FeedPage(logged_in_student)
    feed.navigate()
    test_content = f"Test post {pytest.test_id}"  # Unique per run
    feed.create_post(test_content)
    assert test_content in feed.get_first_post_content()