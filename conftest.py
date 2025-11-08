import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    return "https://staging.api.example.com"

@pytest.fixture
def api_client(base_url):
    class Client:
        def get(self, path, **kwargs):
            return requests.get(base_url + path, **kwargs)
    return Client()
