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


@pytest.mark.e2e
@pytest.mark.xfail(reason="Known bug: Checkout requires at least 2 items (intentional failure demo)")
def test_checkout_with_single_item_fails(page: Page):
    """Test checkout process fails with single item - demonstrating intentional failure"""
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # Add single item
    page.click("#add-to-cart-sauce-labs-backpack")
    page.click(".shopping_cart_link")
    page.click("#checkout")
    
    # This assertion will fail intentionally - demonstrates failure tracking
    assert page.locator(".checkout_info").is_visible() == False, "Single item checkout should fail"


@pytest.mark.e2e  
@pytest.mark.slow
def test_complete_shopping_workflow(page: Page):
    """Test complete e-commerce workflow - demonstrating slow test"""
    import time
    
    # Login
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # Browse and add multiple items (slow operation)
    time.sleep(1)  # Simulate user thinking
    page.click("#add-to-cart-sauce-labs-backpack")
    time.sleep(0.5)
    page.click("#add-to-cart-sauce-labs-bike-light")
    time.sleep(0.5)
    page.click("#add-to-cart-sauce-labs-bolt-t-shirt")
    
    # Go to cart
    page.click(".shopping_cart_link")
    expect(page.locator(".shopping_cart_badge")).to_have_text("3")
    
    # Proceed to checkout
    page.click("#checkout")
    
    # Fill checkout info
    time.sleep(0.5)
    page.fill("#first-name", "John")
    page.fill("#last-name", "Doe")
    page.fill("#postal-code", "12345")
    page.click("#continue")
    
    # Complete order
    time.sleep(0.5)
    page.click("#finish")
    
    # Verify success
    expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")


@pytest.mark.e2e
def test_product_sorting_fails(page: Page):
    """Test product sorting - intentionally fails to demonstrate failure tracking"""
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # Select sort option
    page.select_option(".product_sort_container", "lohi")
    
    # This will fail - wrong expected text to demonstrate failure
    first_item_price = page.locator(".inventory_item_price").first
    expect(first_item_price).to_have_text("$99.99")  # Wrong price - will fail!
