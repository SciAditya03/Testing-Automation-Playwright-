from playwright.sync_api import expect
from pages.base_page import BasePage
from test_data import BASE_URL, STUDENT_EMAIL, STUDENT_PASSWORD

class StudentLoginPage(BasePage):
    
    # Locators (stable CSS patterns matching live DOM)
    EMAIL_INPUT = "input[type='email'], input.form-control:not(.password-input)"
    PASSWORD_INPUT = "input[type='password'], input.password-input"
    ROLE_SELECT = "select.form-select"
    LOGIN_BTN = "button[type='submit']"
    DASHBOARD_HEADING = "text=Student Dashboard, text=Dashboard, text=Feed"
    
    def goto(self):
        self.page.goto(f"{BASE_URL}/login")
        self.page.wait_for_load_state("networkidle")
        
    def login_as_student(self, email=None, password=None):
        email = email or STUDENT_EMAIL
        password = password or STUDENT_PASSWORD
        
        # Fill email
        self.page.locator(self.EMAIL_INPUT).first.fill(email)
        # Fill password
        self.page.locator(self.PASSWORD_INPUT).first.fill(password)
        
        # Select role dropdown
        role_select = self.page.locator(self.ROLE_SELECT).first
        if role_select.is_visible():
            try:
                role_select.select_option("student")
            except Exception:
                role_select.select_option(label="Student")
                
        # Click login
        self.page.locator(self.LOGIN_BTN).first.click()
        self.page.wait_for_load_state("networkidle")
        
        # Verify successful login
        expect(
            self.page.locator(self.DASHBOARD_HEADING).first
        ).to_be_visible(timeout=10000)
        self.page.wait_for_timeout(1000)