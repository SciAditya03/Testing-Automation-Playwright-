# test_login_manual.py
import time
from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://staging-dot-lazyintern-482315.el.r.appspot.com"
EMAIL = "mogope9036@dyleris.com"
PASSWORD = "Test@123"

def run_validation():
    print("🚀 Starting manual verification script...")
    with sync_playwright() as p:
        print("Launching browser in headed mode...")
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        
        try:
            # 1. Navigate to login
            print(f"Navigating to {BASE_URL}/login...")
            page.goto(f"{BASE_URL}/login")
            
            # 2. Fill Email
            print(f"Filling email: {EMAIL}")
            email_field = page.locator("input[type='email'], input.form-control:not(.password-input)").first
            email_field.wait_for(state="visible", timeout=5000)
            email_field.fill(EMAIL)
            
            # 3. Fill Password
            print("Filling password...")
            password_field = page.locator("input[type='password'], input.password-input").first
            password_field.wait_for(state="visible", timeout=5000)
            password_field.fill(PASSWORD)
            
            # 4. Select Role
            print("Checking for role selection dropdown...")
            role_select = page.locator("select.form-select").first
            if role_select.is_visible(timeout=2000):
                print("Selecting Student role...")
                role_select.select_option("student")
                
            # 5. Click Login
            print("Clicking submit login button...")
            login_btn = page.locator("button[type='submit']").first
            login_btn.wait_for(state="visible", timeout=5000)
            login_btn.click()
            
            # 6. Wait for redirect
            print("Waiting for page redirection to /student/feed...")
            page.wait_for_url("**/student/feed", timeout=15000)
            print("Successfully redirected!")
            
            # 7. Verify Feed loads
            print("Verifying Feed layout loads...")
            feed_layout = page.locator(".feed-layout, .posts-page").first
            expect(feed_layout).to_be_visible(timeout=10000)
            
            print("Verifying Feed posts load...")
            post_card = page.locator("div.post-card").first
            expect(post_card).to_be_visible(timeout=10000)
            
            print("✅ Verification successfully completed! Dashboard is fully functional and selectors match DOM.")
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Verification failed! Error details: {e}")
            input("Press Enter to close browser...")
        finally:
            browser.close()

if __name__ == "__main__":
    run_validation()