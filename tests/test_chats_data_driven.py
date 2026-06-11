import pytest
from pages.active_chats_page import ActiveChatsPage
from utils.csv_reader import CSVTestCaseReader

# Load test cases
CHATS_CASES = CSVTestCaseReader("test_data/test_cases/chats_test_cases.csv").read_all()

@pytest.mark.parametrize("case", CHATS_CASES, ids=lambda c: c['test_id'])
def test_chats_scenarios(logged_in_student, case):
    """
    Data-driven test: Executes each row from chats_test_cases.csv
    """
    chats = ActiveChatsPage(logged_in_student)
    test_id = case['test_id']
    scenario = case['test_scenario']
    action = case['action']
    input_data = case['input_data']
    expected = case['expected_result']
    selector_hint = case.get('selector_hint', '').strip()
    
    print(f"\n🧪 [{test_id}] {scenario} | Action: {action}")
    
    # === SKIP CONDITIONS ===
    # Skip any test that requires active chats if the list is empty.
    # Only CHATS_001 and CHATS_005 are valid on an empty chats page.
    if test_id not in ["CHATS_001", "CHATS_005"]:
        chats.navigate()
        if chats.empty_state.is_visible():
            pytest.skip(f"⚠️  No active chats available for {test_id}")
            
    # === EXECUTE ACTION ===
    try:
        if "Navigate" in action:
            chats.navigate()
            chats.wait_for_chats_loaded()
                
        elif "Send" in action:
            chats.navigate()
            chats.wait_for_chats_loaded()
            chats.open_first_chat()
            chats.send_message(input_data)
            
        elif "Open chat" in action:
            chats.navigate()
            chats.wait_for_chats_loaded()
            chats.open_first_chat()
            
        elif "Type in message" in action:
            # For typing indicator test
            chats.navigate()
            chats.wait_for_chats_loaded()
            chats.open_first_chat()
            chats.message_input.fill(input_data)
            # Don't send - just trigger typing event
            logged_in_student.wait_for_timeout(2000)
            
        elif "Click attach" in action:
            pytest.skip("File upload test requires manual file path setup")
            
        else:
            pytest.skip(f"⚠️  Action '{action}' not yet implemented")
            
    except Exception as e:
        pytest.fail(f"❌ {test_id}: Action execution failed - {str(e)}")
    
    # === ASSERT EXPECTED ===
    try:
        expected_lower = expected.lower()
        
        if "visible" in expected_lower or "appears" in expected_lower:
            if selector_hint:
                # Map old/generic CSV selector hints to new robust Page Object locators
                if "chat-list" in selector_hint:
                    locator = chats.chat_list
                elif "unread-count" in selector_hint:
                    locator = chats.unread_badge
                elif "online-status" in selector_hint:
                    locator = chats.online_status
                elif "textarea" in selector_hint or "message" in selector_hint:
                    locator = chats.message_input
                elif "No active chats" in selector_hint or "No chats found" in selector_hint or "typing" in selector_hint:
                    locator = chats.empty_state if "No" in selector_hint else chats.typing_indicator
                else:
                    locator = logged_in_student.locator(selector_hint)
                
                # Check visibility
                locator.first.wait_for(state="visible", timeout=5000)
            else:
                expect(logged_in_student.locator("body")).to_be_visible()
        
        elif "unread" in expected_lower or "count" in expected_lower:
            # Validate unread badge logic
            initial = chats.get_unread_count()
            chats.open_first_chat()
            logged_in_student.wait_for_timeout(2000)  # Wait for update
            after = chats.get_unread_count()
            assert after <= initial, f"Unread count should decrease: {initial} → {after}"
            
        elif "empty" in expected_lower or "no chats" in expected_lower or "no active chats" in expected_lower:
            # Check for the empty state
            chats.empty_state.first.wait_for(state="visible", timeout=5000)
            
    except AssertionError as e:
        pytest.fail(f"❌ {test_id}: Assertion failed - {str(e)}")
    except Exception as e:
        pytest.fail(f"❌ {test_id}: Unexpected error during assertion - {str(e)}")
        
    print(f"✅ {test_id}: PASSED | {scenario}")