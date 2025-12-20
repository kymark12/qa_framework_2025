"""Configuration module for QA Framework."""

from src.config.constants import (
    API_ENDPOINTS,
    DEFAULT_ELEMENT_TIMEOUT,
    DEFAULT_PAGE_LOAD_TIMEOUT,
    DEFAULT_RETRIES,
    DEFAULT_RETRY_BACKOFF,
    DEFAULT_WAIT_TIMEOUT,
    LOG_FORMAT,
    MARKER_E2E,
    MARKER_FLAKY,
    MARKER_REGRESSION,
    MARKER_SLOW,
    MARKER_SMOKE,
    TEST_USERS,
    UI_SELECTORS,
)
from src.config.settings import (
    APISettings,
    Environment,
    LoggingSettings,
    Settings,
    UISettings,
    get_settings,
    load_settings,
)

__all__ = [
    # Settings
    "Settings",
    "APISettings",
    "UISettings",
    "LoggingSettings",
    "Environment",
    "get_settings",
    "load_settings",
    # Constants
    "DEFAULT_WAIT_TIMEOUT",
    "DEFAULT_ELEMENT_TIMEOUT",
    "DEFAULT_PAGE_LOAD_TIMEOUT",
    "DEFAULT_RETRIES",
    "DEFAULT_RETRY_BACKOFF",
    "TEST_USERS",
    "API_ENDPOINTS",
    "UI_SELECTORS",
    "MARKER_SMOKE",
    "MARKER_REGRESSION",
    "MARKER_E2E",
    "MARKER_SLOW",
    "MARKER_FLAKY",
    "LOG_FORMAT",
]