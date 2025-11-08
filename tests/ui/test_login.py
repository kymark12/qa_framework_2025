import pytest

@pytest.mark.e2e
def test_login(page):
    page.goto("https://staging.web.example.com/login")
    page.fill("input[name='email']", "qa@example.com")
    page.fill("input[name='password']", "password123")
    page.click("button[type='submit']")
    page.wait_for_selector("text=Welcome, QA")
    assert "Dashboard" in page.title()
