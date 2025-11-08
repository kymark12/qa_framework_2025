import pytest
import requests
from playwright.sync_api import Page


@pytest.fixture(scope="session")
def base_url():
    """Base URL for API testing"""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture
def api_client(base_url):
    """Custom API client for making requests"""

    class APIClient:
        def __init__(self, base_url):
            self.base_url = base_url
            self.session = requests.Session()

        def get(self, path, **kwargs):
            return self.session.get(f"{self.base_url}{path}", **kwargs)

        def post(self, path, **kwargs):
            return self.session.post(f"{self.base_url}{path}", **kwargs)

        def put(self, path, **kwargs):
            return self.session.put(f"{self.base_url}{path}", **kwargs)

        def delete(self, path, **kwargs):
            return self.session.delete(f"{self.base_url}{path}", **kwargs)

    return APIClient(base_url)


@pytest.fixture
def authenticated_page(page: Page):
    """Fixture that provides an authenticated browser page"""
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    page.wait_for_url("**/inventory.html")
    return page