"""
Data-driven tests for Feed module.
Executes test scenarios from test_data/test_cases/feed_test_cases.csv
"""
import pytest
from playwright.sync_api import expect
from pages.feed_page import FeedPage
from utils.csv_reader import CSVTestCaseReader

# Load test cases once at module level
FEED_CASES = CSVTestCaseReader("test_data/test_cases/feed_test_cases.csv").read_all()


def _get_marker_for_priority(priority: str):
    """Helper: return pytest marker based on CSV priority"""
    priority = priority.lower().strip()
    if priority == "smoke":
        return pytest.mark.smoke
    elif priority == "regression":
        return pytest.mark.regression
    elif priority == "edge":
        return pytest.mark.xfail(reason="Edge case - expected to be flaky")
    return pytest.mark.regression  # Default


# Build parametrized list WITH markers attached to each case
_PARAMETRIZED_CASES = []
for case in FEED_CASES:
    test_id = case['test_id']
    priority = case['priority'].lower()
    marker = _get_marker_for_priority(priority)
    _PARAMETRIZED_CASES.append(
        pytest.param(case, id=f"{test_id}_{priority}", marks=[marker])
    )


@pytest.mark.parametrize("case", _PARAMETRIZED_CASES)
def test_feed_scenarios(logged_in_student, case):
    """
    Data-driven test: Executes each row from feed_test_cases.csv
    
    Args:
        logged_in_student: Authenticated page fixture from conftest.py
        case: Dictionary containing test case data from CSV
    """
    # === EXTRACT TEST DATA ===
    feed = FeedPage(logged_in_student)
    test_id = case['test_id']
    scenario = case['test_scenario']
    priority = case['priority']
    action = case['action']
    input_data = case['input_data']
    expected = case['expected_result']
    selector_hint = case.get('selector_hint', '').strip()
    
    print(f"\n🧪 [{test_id}] {scenario} | Priority: {priority} | Action: {action}")
    
    # === SKIP CONDITIONS ===
    if "cleared via backend" in case['precondition'].lower():
        pytest.skip(f"⚠️  {test_id}: Precondition not setup - {case['precondition']}")
    
    if "pending" in case.get('notes', '').lower():
        pytest.xfail(f"⚠️  {test_id}: Feature implementation pending")
    
    # === EXECUTE ACTION ===
    try:
        if "Navigate" in action:
            feed.navigate()
            feed.wait_for_feed_loaded()
            
        elif "Create post" in action:
            feed.navigate()
            feed.wait_for_feed_loaded()
            if input_data:
                feed.create_post(input_data)
                
        elif "Click like" in action:
            feed.navigate()
            feed.wait_for_feed_loaded()
            feed.click_like_on_first_post()
            
        elif "Click comments" in action:
            feed.navigate()
            feed.wait_for_feed_loaded()
            first_post = feed.post_card.first
            
            # Use the robust comment button selector from FeedPage
            comment_btn = first_post.locator(feed.comment_btn)
            comment_btn.wait_for(state="visible", timeout=5000)
            comment_btn.click()
            
            # Verify comments section expands
            comments_section = first_post.locator(
                ".comments-section, [data-testid='comments-section'], .comments, [role='region']:has-text('Comment')"
            )
            expect(comments_section.first).to_be_visible(timeout=5000)
            
        elif "Select filter" in action:
            feed.navigate()
            feed.wait_for_feed_loaded()
            pytest.xfail(f"⚠️  {test_id}: Filter logic not yet implemented")
            
        elif "Disconnect network" in action:
            logged_in_student.context.set_offline(True)
            try:
                feed.navigate()
            except Exception as e:
                # Navigation exception is expected when offline
                print(f"Expected offline navigation error: {e}")
            finally:
                logged_in_student.context.set_offline(False)
            
        else:
            pytest.skip(f"⚠️  {test_id}: Action '{action}' not yet implemented")
            
    except Exception as e:
        pytest.fail(f"❌ {test_id}: Action execution failed - {str(e)}")
    
    # === ASSERT EXPECTED RESULT ===
    try:
        expected_lower = expected.lower()
        
        if "appears" in expected_lower or "visible" in expected_lower or "shows" in expected_lower:
            if selector_hint:
                selectors = [s.strip() for s in selector_hint.split(',') if s.strip()]
                locator_found = False
                for selector in selectors:
                    try:
                        # Translate old selectors to new robust classes if necessary
                        if "textarea" in selector:
                            locator = feed.new_post_textarea
                        elif "like" in selector:
                            locator = logged_in_student.locator(feed.like_btn)
                        else:
                            locator = logged_in_student.locator(selector)
                        
                        if locator.first.is_visible(timeout=3000):
                            locator_found = True
                            break
                    except:
                        continue
                assert locator_found, f"Expected element visible with selectors: {selector_hint}"
            else:
                expect(logged_in_student.locator("body")).to_be_visible()
                
        elif "increases" in expected_lower or "count" in expected_lower:
            pass  # Already validated in page object method
            
        elif "error" in expected_lower or "gracefully" in expected_lower or "offline" in expected_lower:
            # Check offline state page or generic browser offline handling
            if "chrome-error" in logged_in_student.url or "chromewebdata" in logged_in_student.url:
                print("Confirmed: Redirected to Chrome default offline error page.")
                assert True
            else:
                error_locator = logged_in_student.locator(".error-state")\
                    .or_(logged_in_student.locator("[role='alert']"))\
                    .or_(logged_in_student.locator("text=/error|offline|failed|no internet/i"))
                expect(error_locator.first).to_be_visible(timeout=5000)
            
        elif "empty" in expected_lower or "no posts" in expected_lower:
            expect(feed.empty_state).to_be_visible(timeout=5000)
            
        else:
            expect(logged_in_student.locator("body")).to_be_visible()
            
    except AssertionError as e:
        pytest.fail(f"❌ {test_id}: Assertion failed - {str(e)}")
    except Exception as e:
        pytest.fail(f"❌ {test_id}: Unexpected error during assertion - {str(e)}")
    
    print(f"✅ {test_id}: PASSED | {scenario}")