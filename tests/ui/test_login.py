import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_login_success(page: Page):
    """Test successful login on SauceDemo"""
    # Navigate to the login page
    page.goto("https://www.saucedemo.com/")

    # Fill in credentials
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")

    # Click login button
    page.click("#login-button")

    # Verify successful login
    expect(page.locator(".title")).to_have_text("Products")
    assert page.url == "https://www.saucedemo.com/inventory.html"


@pytest.mark.e2e
def test_login_invalid_credentials(page: Page):
    """Test login with invalid credentials"""
    page.goto("https://www.saucedemo.com/")

    page.fill("#user-name", "invalid_user")
    page.fill("#password", "wrong_password")
    page.click("#login-button")

    # Verify error message appears
    error_message = page.locator("[data-test='error']")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text("Username and password do not match")


@pytest.mark.e2e
def test_login_locked_user(page: Page):
    """Test login with locked out user"""
    page.goto("https://www.saucedemo.com/")

    page.fill("#user-name", "locked_out_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    # Verify locked out error message
    error_message = page.locator("[data-test='error']")
    expect(error_message).to_contain_text("Sorry, this user has been locked out")


@pytest.mark.smoke
def test_add_to_cart(page: Page):
    """Test adding product to cart"""
    # Login first
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    # Add item to the cart
    page.click("#add-to-cart-sauce-labs-backpack")

    # Verify cart badge shows 1 item
    cart_badge = page.locator(".shopping_cart_badge")
    expect(cart_badge).to_have_text("1")