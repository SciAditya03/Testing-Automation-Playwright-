# Playwright Automation Framework

> **A Production-Ready, CSV-Driven Test Automation Suite**  
> Built with **Playwright + Pytest + Page Object Model** 

---

## 📋 Table of Contents

```
1. 🎯 Project Overview
2. 🛠️ Tech Stack & Dependencies
3. 📁 Folder Structure
4. ⚙️ Quick Setup (5 Minutes)
5. 🚀 Execution Commands
6. 📊 Test Case Management (CSV-Driven)
7. 🧱 Page Object Model (POM) Architecture
8. 🐛 Debugging Guide
9. 🔄 CI/CD Integration
10. 📝 Contributing Guidelines
11. ❓ Troubleshooting FAQ
12. 🎓 Exam-Style Quick Reference
```

---

## 🎯 Project Overview

### Purpose
Automate verification of the **LazyIntern Student Dashboard** (React-based) to ensure:
- ✅ Feed section: Posts load, filters work, like/comment interactions function
- ✅ Active Chats: Real-time messaging, unread badges, typing indicators work
- ✅ Integration: Applying to internships in Feed triggers notifications in Chats

### Why This Framework?
| Problem | Solution |
|---------|----------|
| Manual testing is slow & error-prone | Automated tests run in seconds, consistently |
| React DOM changes break tests | Robust, multi-selector fallbacks in Page Objects |
| Test data scattered in code | Centralized CSV files for easy maintenance |
| Hard to trace tests to requirements | CSV `test_id` + `scenario` columns for full traceability |
| Flaky tests waste time | Explicit waits, retry logic, and stable selectors |

### Key Features
```
🔹 CSV-Driven Testing: Add/edit tests in Excel/CSV — no Python code changes
🔹 Page Object Model: Clean separation of selectors (pages/) vs logic (tests/)
🔹 Flexible Selectors: Tries 5-7 patterns per element to handle React changes
🔹 Parametrized Tests: One function executes 8+ scenarios from CSV
🔹 Marker-Based Filtering: Run `smoke`, `regression`, or `integration` tests independently
🔹 HTML Reports: Embedded screenshots, execution times, pass/fail status
🔹 Headed + Headless Modes: Debug with visible browser, run fast in CI
```

---

## 🛠️ Tech Stack & Dependencies

### Core Technologies
| Tool | Version | Purpose |
|------|---------|---------|
| **Python** | 3.10+ | Core programming language |
| **Playwright** | 1.40.0 | Browser automation engine (Chromium) |
| **Pytest** | 7.4.3+ | Test runner, fixtures, parametrization |
| **pypdf** | 3.17.0 | PDF validation (resume downloads) |
| **pyautogui** | 0.9.54 | OS-level interactions (email client workarounds) |

### Installation
```bash
# 1. Create & activate virtual environment
python -m venv myenv
.\myenv\Scripts\activate  # Windows
# source myenv/bin/activate  # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install chromium
```

### `requirements.txt`
```txt
pytest>=7.4.3
playwright>=1.40.0
pypdf>=3.17.0
pyautogui>=0.9.54
python-dotenv>=1.0.0
pytest-html>=4.1.0
pytest-metadata>=3.0.0
```

---

## 📁 Folder Structure

```
Active Chat Testing/
│
├── 📄 README.md                 # This file
├── 📄 requirements.txt          # Python dependencies
├── 📄 pytest.ini                # Pytest configuration
├── 📄 config.py                 # Optional: env-based config
├── 📄 conftest.py               # Pytest fixtures: browser, login, teardown
│
├── 📁 pages/                    # Page Object Model Layer
│   ├── 📄 __init__.py
│   ├── 📄 base_page.py          # Reusable waits, navigation helpers
│   ├── 📄 student_login_page.py # Login flow selectors + actions
│   ├── 📄 feed_page.py          # Feed section: posts, filters, interactions
│   └── 📄 active_chats_page.py  # Chats section: messaging, real-time indicators
│
├── 📁 tests/                    # Test Script Layer
│   ├── 📄 __init__.py
│   ├── 📄 test_feed_smoke.py            # High-priority Feed smoke tests
│   ├── 📄 test_feed_interactions.py     # Like, comment, create post tests
│   ├── 📄 test_feed_data_driven.py      # CSV-driven Feed tests (8 scenarios)
│   ├── 📄 test_chats_smoke.py           # High-priority Chats smoke tests
│   ├── 📄 test_chats_data_driven.py     # CSV-driven Chats tests
│   ├── 📄 test_chats_messaging.py       # Send/receive message tests
│   └── 📄 test_feed_chats_integration.py# Cross-module: Feed → Chats workflow
│
├── 📁 test_data/                # Static Test Data
│   ├── 📄 __init__.py           # Exports: BASE_URL, credentials, timeouts
│   ├── 📄 credentials.py        # Fallback credentials (if __init__.py fails)
│   └── 📁 test_cases/           # CSV test case repository
│       ├── 📄 feed_test_cases.csv       # Feed module scenarios
│       ├── 📄 chats_test_cases.csv      # Active Chats scenarios
│       └── 📄 integration_test_cases.csv# Cross-module workflows
│
├── 📁 utils/                    # Helper Utilities
│   ├── 📄 __init__.py
│   ├── 📄 csv_reader.py         # Parse CSV → Python dicts for parametrization
│   ├── 📄 assertions.py         # Custom soft assertions, retry logic
│   └── 📄 logger.py             # Structured logging for debugging
│
├── 📁 reports/                  # Auto-generated: HTML reports, logs
├── 📁 screenshots/              # Auto-captured on test failure
├── 📄 test_login_manual.py      # Standalone login validation script
└── 📄 walkthrough.md            # Antigravity session logs + selector discoveries
```

> 🔑 **Key Principle**: Tests don't know HTML selectors. Pages don't know assertions. This separation = maintainability.

---


##  🚀 Execution Commands

### 🔍 Pre-Run: Validate Login Manually
```bash
# Run standalone script to verify credentials + selectors
python test_login_manual.py
```
✅ Watch browser: Should auto-fill login → redirect to `/student/feed` → show posts.

### 🧪 Run Tests: Choose Your Mode

| Goal | Command | Use Case |
|------|---------|----------|
| **Run 1 test, debug mode** | `pytest "tests/test_feed_data_driven.py::test_feed_scenarios[FEED_001_smoke]" -v -s --headed` | Debugging a specific test |
| **Run Feed smoke tests** | `pytest tests/test_feed_data_driven.py -m smoke -v --headed` | Quick validation before coding |
| **Run ALL Feed tests** | `pytest tests/test_feed_*.py -v --headed` | Full Feed module verification |
| **Run Chats tests** | `pytest tests/test_chats_*.py -v --headed` | Validate messaging workflows |
| **Run integration test** | `pytest tests/test_feed_chats_integration.py -v --headed -s` | Cross-module: Feed → Chats flow |
| **Run full suite (CI)** | `pytest -v --headless --html=reports/report.html` | Pre-release validation, fast execution |
| **Re-run failed tests only** | `pytest --last-failed -v` | Fix flaky tests iteratively |
| **Collect tests (dry run)** | `pytest --collect-only -q` | Verify test discovery without execution |

### 📊 View Reports
```bash
# Open HTML report in default browser
start reports/report.html  # Windows
# open reports/report.html  # Mac
```

✅ **Report Includes**:
- 🟢/🔴 Pass/fail status per test
- ⏱️ Execution time per test
- 🖼️ Embedded screenshots on failure
- 📋 Console logs (if `print()` used in tests)
- 🔗 Traceability: Test IDs match CSV rows

---

## 📊 Test Case Management (CSV-Driven)

### How It Works
```
CSV File (Business View)          Pytest (Automation View)          Playwright (Execution View)
─────────────────────────          ───────────────────────          ─────────────────────
test_id: FEED_003                  @pytest.mark.parametrize         page.locator("text=/like[s]?/i")
scenario: Like button increments   case['expected_result']          .click()
priority: regression               → assert new_count == old+1      → wait_for_load_state("networkidle")
selector_hint: text=/like[s]?/i    case['selector_hint']            → expect(like_count).to_change()
api_hint: POST /api/posts/{id}/like  (for debugging/network mock)
```

### CSV Template: `test_data/test_cases/feed_test_cases.csv`
```csv
test_id,module,test_scenario,priority,precondition,action,input_data,expected_result,selector_hint,api_hint,notes
FEED_001,Feed,Verify feed loads with posts,smoke,User logged in,Navigate to /student/feed,,Feed shows posts or empty state,main,GET /api/feed,Initial load test
FEED_002,Feed,Create new post with text,smoke,On feed page,Fill textarea + click Post,"Hello from automation",New post appears at top with correct content,textarea[placeholder*='What are you building'],POST /api/posts,Unique content per run
FEED_003,Feed,Like button increments count,regression,Post exists with likes,Click like button on first post,,Like count increases by 1,text=/like[s]?/i,POST /api/posts/{id}/like,Wait for networkidle after click
```

### Add a New Test Case (No Code Changes!)
1. Open `test_data/test_cases/feed_test_cases.csv` in Excel/VS Code
2. Add a new row with:
   - Unique `test_id` (e.g., `FEED_009`)
   - Clear `test_scenario` description
   - `priority`: `smoke` or `regression`
   - `action` and `input_data` matching Page Object methods
   - `expected_result` for assertion logic
3. Save the file
4. Run pytest — your new test auto-appears! 🎉

```bash
# Verify new test is collected
pytest --collect-only -q | grep FEED_009

# Run it
pytest "tests/test_feed_data_driven.py::test_feed_scenarios[FEED_009_smoke]" -v --headed
```

