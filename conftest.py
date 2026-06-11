"""
Pytest configuration and fixtures for Student Dashboard automation.
Located in project root to be discovered by all tests.
"""
import pytest
import uuid
from playwright.sync_api import sync_playwright, Page, expect

# Set global test_id on pytest module
pytest.test_id = str(uuid.uuid4())[:8]

# Import test data - handles missing variables gracefully
try:
    from test_data import (
        BASE_URL, 
        STUDENT_EMAIL, 
        STUDENT_PASSWORD, 
        FEED_URL,
        DEFAULT_TIMEOUT,
        HEADLESS,
        SLOW_MO
    )
except ImportError:
    # Fallback defaults if test_data/__init__.py is misconfigured
    BASE_URL = "https://staging-dot-lazyintern-482315.el.r.appspot.com"
    STUDENT_EMAIL = "mogope9036@dyleris.com"
    STUDENT_PASSWORD = "Test@123"
    FEED_URL = "/student/feed"
    DEFAULT_TIMEOUT = 10000
    HEADLESS = False
    SLOW_MO = 0


@pytest.fixture(scope="function")
def page():
    """
    Launch Chromium browser and yield page object.
    Uses playwright's sync API for simpler debugging.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            ignore_https_errors=True,
            locale="en-US"
        )
        page = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)
        
        # Yield page to test execution
        yield page
        
        # Teardown: close browser after test
        browser.close()


@pytest.fixture
def logged_in_student(page: Page) -> Page:
    """
    Login as student and return authenticated page.
    This fixture depends on the 'page' fixture above.
    
    Usage in tests:
        def test_something(logged_in_student):
            logged_in_student.goto("/student/feed")  # Already logged in
    """
    # Navigate to login page
    page.goto(f"{BASE_URL}/login")
    
    # 1. Fill email input using fallback selectors
    email_selectors = [
        "input[type='email']",
        "input.form-control:not(.password-input)",
        "input[placeholder*='email']",
        "input[autocomplete='email']",
        "#id_email",
        "[data-testid='student-email']"
    ]
    email_filled = False
    for selector in email_selectors:
        try:
            loc = page.locator(selector).first
            loc.wait_for(state="visible", timeout=3000)
            loc.fill(STUDENT_EMAIL)
            email_filled = True
            break
        except Exception:
            continue
    if not email_filled:
        raise Exception(f"Failed to find or fill student email input using selectors: {email_selectors}")
        
    # 2. Fill password input using fallback selectors
    password_selectors = [
        "input[type='password']",
        "input.password-input",
        "input[autocomplete='current-password']",
        "#id_password",
        "[data-testid='student-password']"
    ]
    password_filled = False
    for selector in password_selectors:
        try:
            loc = page.locator(selector).first
            loc.wait_for(state="visible", timeout=3000)
            loc.fill(STUDENT_PASSWORD)
            password_filled = True
            break
        except Exception:
            continue
    if not password_filled:
        raise Exception(f"Failed to find or fill student password input using selectors: {password_selectors}")
        
    # 3. Select Student role if dropdown is present
    role_selectors = [
        "select.form-select",
        "select",
        "#loginAs",
        "#role-dropdown"
    ]
    for selector in role_selectors:
        try:
            loc = page.locator(selector).first
            if loc.is_visible(timeout=1000):
                # Try both lowercase and uppercase/value selection
                try:
                    loc.select_option("student")
                except Exception:
                    loc.select_option(label="Student")
                break
        except Exception:
            continue
            
    # 4. Click login button using fallback selectors
    btn_selectors = [
        "button[type='submit']",
        "button.btn-grad",
        "button:has-text('Login')",
        "button:has-text('Log in')",
        "#loginButton",
        "[data-testid='login-btn']"
    ]
    btn_clicked = False
    for selector in btn_selectors:
        try:
            loc = page.locator(selector).first
            loc.wait_for(state="visible", timeout=2000)
            loc.click()
            btn_clicked = True
            break
        except Exception:
            continue
    if not btn_clicked:
        raise Exception(f"Failed to find or click login button using selectors: {btn_selectors}")
        
    # 5. Wait for successful redirect + React hydration
    try:
        page.wait_for_url("**/student/feed", timeout=15000)
    except Exception:
        try:
            page.wait_for_url(f"*{FEED_URL}", timeout=5000)
        except Exception:
            # Fallback: wait for dashboard heading/feed indicators
            expect(
                page.locator(".feed-layout, .posts-page, text=Student Dashboard, text=Feed").first
            ).to_be_visible(timeout=10000)
            
    # Small buffer for React hydration and re-render
    page.wait_for_timeout(1000)
    
    return page


# Optional: Helper fixture for quick smoke tests without full login
@pytest.fixture
def base_page(page: Page) -> Page:
    """
    Returns page object without login.
    Use for testing public pages or when login is handled in test.
    """
    page.set_default_timeout(DEFAULT_TIMEOUT)
    return page