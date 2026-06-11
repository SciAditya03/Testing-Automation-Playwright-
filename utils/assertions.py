def soft_assert(condition: bool, message: str, errors: list):
    """Collect assertion errors instead of failing immediately"""
    if not condition:
        errors.append(message)
        
def retry_assert(func, max_retries=3, delay_ms=1000):
    """Retry assertion for flaky React renders"""
    import time
    for attempt in range(max_retries):
        try:
            return func()
        except AssertionError:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay_ms / 1000)