import pytest
from pages.active_chats_page import ActiveChatsPage

@pytest.mark.smoke
@pytest.mark.chats
def test_chats_page_loads(logged_in_student):
    """Verify Active Chats page loads"""
    chats = ActiveChatsPage(logged_in_student)
    chats.navigate()
    # Either chat list or empty state should be visible
    if chats.empty_state.is_visible():
        assert True  # Valid empty state
    else:
        chats.wait_for_chats_loaded()
        assert chats.chat_item.count() > 0
        
@pytest.mark.smoke
@pytest.mark.chats
def test_send_message_flow(logged_in_student):
    """Verify sending a message works"""
    chats = ActiveChatsPage(logged_in_student)
    chats.navigate()
    if chats.empty_state.is_visible():
        pytest.skip("No active chats to test messaging")
    chats.wait_for_chats_loaded()
    chats.open_first_chat()
    test_msg = f"Test message {pytest.test_id}"
    chats.send_message(test_msg)
    # Verify message appears in chat
    assert chats.message_list.locator(f":has-text('{test_msg}')").is_visible()