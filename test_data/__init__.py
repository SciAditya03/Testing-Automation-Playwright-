# test_data/__init__.py
# Centralized test data for Student Dashboard automation

# Environment Configuration
BASE_URL = "https://staging-dot-lazyintern-482315.el.r.appspot.com"

# Student Credentials (use test accounts only)
STUDENT_EMAIL = "mogope9036@dyleris.com"
STUDENT_PASSWORD = "Test@123"

# Route Paths
FEED_URL = "/student/feed"
CHATS_URL = "/student/chats"
LOGIN_URL = "/login"

# Timeouts (milliseconds)
DEFAULT_TIMEOUT = 100000
NETWORK_IDLE_TIMEOUT = 30000

# Feature Flags
HEADLESS = False  # Set to True for CI/CD
SLOW_MO = 100     # Slow down actions for debugging (0 = normal speed)