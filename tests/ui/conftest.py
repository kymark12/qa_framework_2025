"""
UI Test Configuration - Pytest fixtures for Playwright.

This conftest applies only to tests/ui/ directory.
"""

import pytest

from src.config import get_settings


@pytest.fixture(scope="function")
def page(browser):
    """
    Create a new page for each test using the browser fixture.

    Uses pytest-playwright's browser fixture automatically.
    """
    settings = get_settings()
    context = browser.new_context(
        viewport={
            "width": settings.ui.viewport_width,
            "height": settings.ui.viewport_height,
        }
    )
    page_instance = context.new_page()
    page_instance.set_default_timeout(settings.ui.timeout)

    yield page_instance

    context.close()