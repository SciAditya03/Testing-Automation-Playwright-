from playwright.sync_api import expect, Locator
from pages.base_page import BasePage

class ActiveChatsPage(BasePage):
    
    def __init__(self, page):
        super().__init__(page)
        # === SELECTORS (Robust web elements matching actual DOM) ===
        self.wrapper = page.locator(".app-wrap, .container-fluid")
        
        # Left Panel (Chat List)
        self.chat_list = page.locator("div[style*='border-right'], .chat-list")
        self.chat_item = page.locator("div[style*='border-right'] > div > div:not(:first-child), .chat-item, [data-testid='chat-item']")
        
        # Right Panel (Chat Window)
        self.chat_window = page.locator("div[style*='flex: 1 1 0%'], .chat-window, [data-testid='chat-window']")
        self.message_list = page.locator(".message-list, .messages-container, [role='log'], div[style*='flex-grow: 1']")
        self.message_incoming = page.locator(".message-incoming, .incoming, .message--incoming")
        self.message_outgoing = page.locator(".message-outgoing, .outgoing, .message--outgoing")
        self.message_input = page.locator("textarea[placeholder*='Type a message'], .message-input, textarea.form-control")
        self.send_button = page.locator("button.send-btn, button:has-text('Send'), button[data-testid='send-btn']")
        
        # Indicators & Badges
        self.typing_indicator = page.locator(".typing-indicator").or_(page.locator("text=/is typing/i"))
        self.online_status = page.locator(".online-dot, .online-status, [data-testid='online-status']")
        self.unread_badge = page.locator(".unread-badge, .unread-count, [data-testid='unread-count'], .badge")
        self.empty_state = page.locator("p.text-muted:has-text('No chats found.')").or_(page.locator("text=/No chats found|No active chats/i"))

    def navigate(self):
        self.goto("/student/chats")

    def wait_for_chats_loaded(self, timeout=15000):
        """Wait for chats page to load and resolve either to chats list or empty state"""
        try:
            self.page.locator("text=/Active Chats/i").wait_for(state="visible", timeout=timeout)
        except:
            pass
            
        if self.empty_state.is_visible():
            return "empty"
            
        try:
            self.chat_item.first.wait_for(state="visible", timeout=timeout)
            return "loaded"
        except:
            return "empty"

    def open_first_chat(self):
        """Click on the first active chat in the sidebar list"""
        first_chat = self.chat_item.first
        first_chat.wait_for(state="visible")
        first_chat.click()
        self.page.wait_for_load_state("networkidle")

    def send_message(self, content: str):
        """Type and send a text message in the active chat window"""
        self.message_input.wait_for(state="visible")
        self.message_input.fill(content)
        self.send_button.wait_for(state="visible")
        self.send_button.click()
        self.page.wait_for_load_state("networkidle")

    def get_unread_count(self) -> int:
        """Safely extract unread count from the first available badge"""
        if not self.unread_badge.first.is_visible():
            return 0
        try:
            text = self.unread_badge.first.text_content().strip()
            if not text:
                return 0
            return int(''.join(filter(str.isdigit, text))) if any(char.isdigit() for char in text) else 0
        except Exception:
            return 0