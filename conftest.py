
"""
Root conftest.py - Pytest configuration and fixtures.

Provides global fixtures for settings, logging, and test organization.
"""

import logging

import pytest
import requests
from playwright.sync_api import Page

from src.config import Settings, get_settings, load_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    """
    Load and provide application settings.

    Returns:
        Settings: Global settings object

    Usage:
        def test_example(settings):
            print(settings.api.base_url)
    """
    return get_settings()


@pytest.fixture(scope="session")
def logger() -> logging.Logger:
    """
    Configure and provide a logger for tests.

    Returns:
        logging.Logger: Configured logger instance

    Usage:
        def test_example(logger):
            logger.info("Test message")
    """
    logger_instance = logging.getLogger("qa_framework")
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger_instance.addHandler(handler)
    logger_instance.setLevel(logging.DEBUG)
    return logger_instance


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Add custom command-line options to pytest.

    Options:
        --env: Environment to run tests against (local, ci, staging, prod)
    """
    parser.addoption(
        "--env",
        action="store",
        default="local",
        help="Environment to run tests against: local, ci, staging, prod",
    )


def pytest_configure(config: pytest.Config) -> None:
    """
    Configure pytest before test collection.

    Loads settings based on --env CLI argument.
    """
    env = config.getoption("--env")
    load_settings(environment=env)
    print(f"\n🔧 Running tests against {env} environment")
    print(f"📍 API: {get_settings().api.base_url}")
    print(f"🌐 UI: {get_settings().ui.base_url}")


@pytest.fixture(scope="session")
def base_url():
    """Base URL for API testing"""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture
def api_client(base_url):
    """Custom API client for making requests"""

    class APIClient:
        def __init__(self, base_url: str):
            self.base_url = base_url
            self.session = requests.Session()

        def get(self, path: str, **kwargs):
            return self.session.get(f"{self.base_url}{path}", **kwargs)

        def post(self, path: str, **kwargs):
            return self.session.post(f"{self.base_url}{path}", **kwargs)

        def put(self, path: str, **kwargs):
            return self.session.put(f"{self.base_url}{path}", **kwargs)

        def delete(self, path: str, **kwargs):
            return self.session.delete(f"{self.base_url}{path}", **kwargs)

    return APIClient(base_url)


@pytest.fixture
def authenticated_page(page: Page, settings: Settings) -> Page:
    """
    Fixture that provides an authenticated browser page.

    The 'page' fixture is provided by pytest-playwright automatically.
    This fixture logs in and returns the authenticated page.
    """
    page.goto(settings.ui.base_url)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    page.wait_for_url("**/inventory.html")
    return page