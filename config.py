import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file if exists

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://staging-dot-lazyintern-482315.el.r.appspot.com")
    STUDENT_EMAIL = os.getenv("STUDENT_EMAIL", "teststudent@lazyintern.com")
    STUDENT_PASSWORD = os.getenv("STUDENT_PASSWORD", "Test@123")
    
    # Timeouts (ms)
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10000"))
    NETWORK_IDLE_TIMEOUT = int(os.getenv("NETWORK_IDLE_TIMEOUT", "30000"))
    
    # Feature flags
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # For debugging