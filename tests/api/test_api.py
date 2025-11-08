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