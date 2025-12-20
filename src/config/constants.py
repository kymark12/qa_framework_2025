"""
Application constants (environment-agnostic).

These values don't change across environments and are used
throughout the test framework.
"""

# Test timeouts
DEFAULT_WAIT_TIMEOUT = 10  # seconds
DEFAULT_ELEMENT_TIMEOUT = 5  # seconds
DEFAULT_PAGE_LOAD_TIMEOUT = 30  # seconds

# Retry policy
DEFAULT_RETRIES = 3
DEFAULT_RETRY_BACKOFF = 0.5

# Test user credentials (for demo app)
TEST_USERS = {
    "standard_user": {"username": "standard_user", "password": "secret_sauce"},
    "locked_user": {"username": "locked_out_user", "password": "secret_sauce"},
    "problem_user": {"username": "problem_user", "password": "secret_sauce"},
}

# API endpoints (relative paths)
API_ENDPOINTS = {
    "users": "/users",
    "posts": "/posts",
    "comments": "/comments",
}

# UI selectors (for SauceDemo app)
UI_SELECTORS = {
    "username_input": "#user-name",
    "password_input": "#password",
    "login_button": "#login-button",
}

# Test markers
MARKER_SMOKE = "smoke"
MARKER_REGRESSION = "regression"
MARKER_E2E = "e2e"
MARKER_SLOW = "slow"
MARKER_FLAKY = "flaky"

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"