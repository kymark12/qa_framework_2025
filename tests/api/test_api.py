import pytest
import requests


@pytest.mark.api
def test_get_user():
    """Test GET request to retrieve user data"""
    response = requests.get("https://jsonplaceholder.typicode.com/users/1")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Leanne Graham"
    assert "email" in data
    assert "@" in data["email"]


@pytest.mark.api
def test_get_all_users():
    """Test GET request to retrieve all users"""
    response = requests.get("https://jsonplaceholder.typicode.com/users")

    assert response.status_code == 200

    users = response.json()
    assert len(users) == 10
    assert all("id" in user for user in users)
    assert all("email" in user for user in users)


@pytest.mark.api
def test_create_user():
    """Test POST request to create a new user"""
    new_user = {
        "name": "QA Test User",
        "username": "qa_test",
        "email": "qa@example.com"
    }

    response = requests.post(
        "https://jsonplaceholder.typicode.com/users",
        json=new_user
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == new_user["name"]
    assert data["email"] == new_user["email"]
    assert "id" in data


@pytest.mark.api
def test_update_user():
    """Test PUT request to update user data"""
    updated_data = {
        "id": 1,
        "name": "Updated Name",
        "email": "updated@example.com"
    }

    response = requests.put(
        "https://jsonplaceholder.typicode.com/users/1",
        json=updated_data
    )

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == updated_data["name"]


@pytest.mark.api
def test_delete_user():
    """Test DELETE request to remove user"""
    response = requests.delete("https://jsonplaceholder.typicode.com/users/1")

    assert response.status_code == 200


@pytest.mark.api
def test_get_user_posts(api_client):
    """Test GET request using a custom API client fixture"""
    response = api_client.get("/posts?userId=1")

    assert response.status_code == 200

    posts = response.json()
    assert len(posts) > 0
    assert all(post["userId"] == 1 for post in posts)


@pytest.mark.api
def test_invalid_user_id_returns_404():
    """Test that invalid user ID returns 404 - intentional failure demo"""
    response = requests.get("https://jsonplaceholder.typicode.com/users/999999")
    
    # This will fail - API returns 404 but we expect 200
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"


@pytest.mark.api
def test_create_user_with_missing_fields():
    """Test creating user with missing required fields - demonstrates validation failure"""
    incomplete_user = {
        "username": "test_only"
        # Missing name and email
    }
    
    response = requests.post(
        "https://jsonplaceholder.typicode.com/users",
        json=incomplete_user
    )
    
    # This assertion will fail - API doesn't validate, but we expect it to
    assert response.status_code == 400, "Should return 400 for missing fields"


@pytest.mark.api
@pytest.mark.slow
def test_api_rate_limiting():
    """Test API rate limiting - slow test with multiple requests"""
    import time
    
    results = []
    for i in range(10):
        response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{i+1}")
        results.append(response.status_code)
        time.sleep(0.2)  # Simulate rate limiting
    
    assert all(status == 200 for status in results)
    assert len(results) == 10


@pytest.mark.api  
def test_user_data_schema_validation():
    """Test user data structure matches expected schema - partial failure demo"""
    response = requests.get("https://jsonplaceholder.typicode.com/users/1")
    data = response.json()
    
    required_fields = ["id", "name", "username", "email", "phone", "website", "company", "address"]
    
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    # This will fail - testing for field that doesn't exist
    assert "salary" in data, "User should have salary field"


@pytest.mark.api
@pytest.mark.skip(reason="API endpoint temporarily unavailable - demonstrating skip functionality")
def test_deprecated_endpoint():
    """Test deprecated endpoint - skipped to show skip tracking"""
    response = requests.get("https://jsonplaceholder.typicode.com/deprecated")
    assert response.status_code == 200
