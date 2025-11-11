"""
REST API Tests - Works with Local Mock Server
File: tests/test_users.py

Run mock server first: python mock_api_server.py
Then run tests: pytest -v tests/test_users.py
"""

import requests
import pytest
import time
import os

# Mark to skip in CI
skip_in_ci = pytest.mark.skipif(
    os.getenv("CI") == "true" and "reqres.in" in os.getenv("API_BASE_URL", ""),
    reason="ReqRes API requires API key for this operation"
)

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")

class TestUsersAPI:
    """Test suite for Users API endpoints"""
    

    @pytest.mark.smoke
    def test_get_list_users(self):
        """Test retrieving list of users - GET /api/users"""
        url = f"{API_BASE_URL}/api/users"
        params = {"page": 1}
        
        response = requests.get(url, params=params)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain 'data' key"
        assert len(response_data["data"]) > 0, "Data array should not be empty"
        assert "page" in response_data, "Response should contain 'page' key"
        assert response_data["page"] == 1, "Page should be 1"
        assert "per_page" in response_data, "Response should contain 'per_page'"
        assert "total" in response_data, "Response should contain 'total'"
        
        print(f"\n✅ Found {len(response_data['data'])} users on page 1")
        print(f"   Total users in system: {response_data['total']}")

    @skip_in_ci
    @pytest.mark.smoke
    def test_get_list_users_page_2(self):
        """Test retrieving list of users on page 2 - GET /api/users?page=2"""
        url = f"{API_BASE_URL}/api/users"
        params = {"page": 2}
        
        response = requests.get(url, params=params)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        response_data = response.json()
        assert response_data["page"] == 2, "Page should be 2"
        assert len(response_data["data"]) > 0, "Should have users on page 2"
        
        print(f"\n✅ Found {len(response_data['data'])} users on page 2")
    
    @pytest.mark.regression
    def test_get_single_user(self):
        """Test retrieving a single user by ID - GET /api/users/{id}"""
        user_id = 2
        url = f"{API_BASE_URL}/api/users/{user_id}"
        
        response = requests.get(url)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        print("*************\n")
        print(response_data)
        assert "data" in response_data, "Response should contain 'data' key"
        
        user = response_data["data"]
        assert user["id"] == user_id, f"User ID should be {user_id}"
        assert "email" in user, "User should have email"
        assert "first_name" in user, "User should have first_name"
        assert "last_name" in user, "User should have last_name"
        assert "avatar" in user, "User should have avatar"
        
        print(f"\n✅ User: {user['first_name']} {user['last_name']}")
        print(f"   Email: {user['email']}")

    @skip_in_ci
    @pytest.mark.negative
    def test_get_user_not_found(self):
        """Test that requesting non-existent user returns 404 - GET /api/users/{id}"""
        url = f"{API_BASE_URL}/api/users/999"
        
        response = requests.get(url)
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        
        print("\n✅ 404 correctly returned for non-existent user")

    @skip_in_ci
    @pytest.mark.regression
    def test_create_user(self):
        """Test creating a new user - POST /api/users"""
        url = f"{API_BASE_URL}/api/users"
        user_data = {
            "name": "Adam Majcher",
            "job": "QA Engineer"
        }
        
        response = requests.post(url, json=user_data)

        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        response_data = response.json()
        assert response_data["name"] == user_data["name"], "Name should match"
        assert response_data["job"] == user_data["job"], "Job should match"
        assert "id" in response_data, "Response should contain id"
        assert "createdAt" in response_data, "Response should contain createdAt"
        
        print(f"\n✅ Created user with ID: {response_data['id']}")

    @skip_in_ci
    @pytest.mark.regression
    def test_update_user(self):
        """Test updating an existing user - PUT /api/users/{id}"""
        user_id = 2
        url = f"{API_BASE_URL}/api/users/{user_id}"
        update_data = {
            "name": "Adam Updated",
            "job": "Senior QA Engineer"
        }
        
        response = requests.put(url, json=update_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert response_data["name"] == update_data["name"], "Name should be updated"
        assert response_data["job"] == update_data["job"], "Job should be updated"
        assert "updatedAt" in response_data, "Response should contain updatedAt"
        
        print(f"\n✅ Updated user at: {response_data['updatedAt']}")

    @skip_in_ci
    @pytest.mark.regression
    def test_patch_user(self):
        """Test partially updating a user - PATCH /api/users/{id}"""
        user_id = 2
        url = f"{API_BASE_URL}/api/users/{user_id}"
        patch_data = {
            "job": "Lead QA Engineer"
        }
        
        response = requests.patch(url, json=patch_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert response_data["job"] == patch_data["job"], "Job should be updated"
        assert "updatedAt" in response_data, "Response should contain updatedAt"
        
        print(f"\n✅ Patched user successfully")

    @skip_in_ci
    @pytest.mark.regression
    def test_delete_user(self):
        """Test deleting a user - DELETE /api/users/{id}"""
        user_id = 2
        url = f"{API_BASE_URL}/api/users/{user_id}"
        
        response = requests.delete(url)
        
        assert response.status_code == 204, f"Expected 204, got {response.status_code}"
        
        print("\n✅ User deleted successfully")

    @skip_in_ci
    @pytest.mark.regression
    def test_get_all_users(self):
        """Test retrieving multiple users by iterating through pages"""
        url = f"{API_BASE_URL}/api/users"
        all_users = []
        
        first_response = requests.get(url, params={"page": 1})
        assert first_response.status_code == 200
        
        first_data = first_response.json()
        total_pages = first_data["total_pages"]
        all_users.extend(first_data["data"])
        
        for page in range(2, total_pages + 1):
            response = requests.get(url, params={"page": page})
            assert response.status_code == 200
            all_users.extend(response.json()["data"])
        
        assert len(all_users) == first_data["total"], "Should get all users"
        
        user_ids = [user["id"] for user in all_users]
        assert len(user_ids) == len(set(user_ids)), "All user IDs should be unique"
        
        print(f"\n✅ Retrieved all {len(all_users)} users across {total_pages} pages")
    
    @pytest.mark.regression
    def test_user_data_structure(self):
        """Test that user data has all required fields"""
        url = f"{API_BASE_URL}/api/users/1"
        
        response = requests.get(url)
        
        assert response.status_code == 200
        user = response.json()["data"]
        
        required_fields = ["id", "email", "first_name", "last_name", "avatar"]
        for field in required_fields:
            assert field in user, f"User should have '{field}' field"
            assert user[field] is not None, f"'{field}' should not be None"
            assert user[field] != "", f"'{field}' should not be empty"
        
        assert isinstance(user["id"], int), "ID should be integer"
        assert isinstance(user["email"], str), "Email should be string"
        assert isinstance(user["first_name"], str), "First name should be string"
        assert isinstance(user["last_name"], str), "Last name should be string"
        assert isinstance(user["avatar"], str), "Avatar should be string"
        
        assert "@" in user["email"], "Email should contain @"
        assert "." in user["email"], "Email should contain domain"
        
        print(f"\n✅ User data structure is valid")
        print(f"   Sample user: {user['first_name']} {user['last_name']}")


class TestResourcesAPI:
    """Test suite for Resources API endpoints"""

    @skip_in_ci
    @pytest.mark.smoke
    def test_get_list_resources(self):
        """Test retrieving list of resources - GET /api/unknown"""
        url = f"{API_BASE_URL}/api/unknown"
        
        response = requests.get(url)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain 'data' key"
        assert len(response_data["data"]) > 0, "Data array should not be empty"
        
        first_resource = response_data["data"][0]
        assert "id" in first_resource, "Resource should have id"
        assert "name" in first_resource, "Resource should have name"
        assert "year" in first_resource, "Resource should have year"
        assert "color" in first_resource, "Resource should have color"
        
        print(f"\n✅ Found {len(response_data['data'])} resources")

    @skip_in_ci
    @pytest.mark.regression
    def test_get_single_resource(self):
        """Test retrieving a single resource - GET /api/unknown/{id}"""
        resource_id = 2
        url = f"{API_BASE_URL}/api/unknown/{resource_id}"
        
        response = requests.get(url)
        
        assert response.status_code == 200
        response_data = response.json()
        
        assert "data" in response_data
        resource = response_data["data"]
        assert resource["id"] == resource_id
        assert "name" in resource
        assert "year" in resource
        assert "color" in resource
        assert "pantone_value" in resource
        
        print(f"\n✅ Resource: {resource['name']}")
        print(f"   Year: {resource['year']}, Color: {resource['color']}")

    @skip_in_ci
    @pytest.mark.negative
    def test_get_resource_not_found(self):
        """Test that requesting non-existent resource returns 404"""
        url = f"{API_BASE_URL}/api/unknown/999"
        
        response = requests.get(url)
        
        assert response.status_code == 404
        
        print("\n✅ 404 correctly returned for non-existent resource")


class TestAuthentication:
    """Test suite for Authentication endpoints"""

    @skip_in_ci
    @pytest.mark.regression
    def test_register_successful(self):
        """Test successful user registration - POST /api/register"""
        url = f"{API_BASE_URL}/api/register"
        user_data = {
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
        
        response = requests.post(url, json=user_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert "id" in response_data, "Response should contain id"
        assert "token" in response_data, "Response should contain token"
        
        print(f"\n✅ Registered with token: {response_data['token'][:10]}...")

    @skip_in_ci
    @pytest.mark.negative
    def test_register_unsuccessful(self):
        """Test registration fails without password - POST /api/register"""
        url = f"{API_BASE_URL}/api/register"
        user_data = {
            "email": "sydney@fife"
        }
        
        response = requests.post(url, json=user_data)
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        response_data = response.json()
        assert "error" in response_data, "Response should contain error message"
        
        print(f"\n✅ Registration failed as expected: {response_data['error']}")

    @skip_in_ci
    @pytest.mark.regression
    def test_login_successful(self):
        """Test successful login - POST /api/login"""
        url = f"{API_BASE_URL}/api/login"
        credentials = {
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }
        
        response = requests.post(url, json=credentials)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert "token" in response_data, "Response should contain token"
        
        print(f"\n✅ Login successful with token: {response_data['token'][:10]}...")

    @skip_in_ci
    @pytest.mark.negative
    def test_login_unsuccessful(self):
        """Test login fails without password - POST /api/login"""
        url = f"{API_BASE_URL}/api/login"
        credentials = {
            "email": "peter@klaven"
        }
        
        response = requests.post(url, json=credentials)
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        response_data = response.json()
        assert "error" in response_data, "Response should contain error message"
        
        print(f"\n✅ Login failed as expected: {response_data['error']}")


class TestResponseTiming:
    """Test suite for response time validation"""


    @pytest.mark.performance
    def test_response_time_under_threshold(self):
        """Test that API responds within acceptable time"""
        url = f"{API_BASE_URL}/api/users/1"
        max_response_time = 5.0  # 5 seconds
        
        response = requests.get(url)
        response_time = response.elapsed.total_seconds()
        
        assert response.status_code == 200
        assert response_time < max_response_time, \
            f"Response time {response_time:.2f}s exceeds threshold {max_response_time}s"
        
        print(f"\n✅ Response time: {response_time:.3f}s (under {max_response_time}s threshold)")

    @skip_in_ci
    @pytest.mark.performance
    def test_delayed_response(self):
        """Test API with delayed response - GET /api/users?delay=3"""
        url = f"{API_BASE_URL}/api/users"
        params = {"delay": 3}
        
        start_time = time.time()
        response = requests.get(url, params=params, timeout=10)
        elapsed_time = time.time() - start_time
        
        assert response.status_code == 200
        assert elapsed_time >= 2.0, f"Response should be delayed by at least 2 seconds, got {elapsed_time:.2f}s"
        assert elapsed_time < 7.0, f"Response should not take longer than 7 seconds, got {elapsed_time:.2f}s"
        
        print(f"\n✅ Delayed response received after {elapsed_time:.2f} seconds")


class TestPagination:
    """Test suite for pagination functionality"""

    @skip_in_ci
    @pytest.mark.regression
    def test_pagination_info(self):
        """Test that pagination information is correct"""
        url = f"{API_BASE_URL}/api/users"
        
        response = requests.get(url, params={"page": 1})
        data = response.json()
        
        assert "page" in data
        assert "per_page" in data
        assert "total" in data
        assert "total_pages" in data
        
        expected_pages = (data["total"] + data["per_page"] - 1) // data["per_page"]
        assert data["total_pages"] == expected_pages, "Total pages calculation should be correct"
        
        print(f"\n✅ Pagination info correct:")
        print(f"   Total: {data['total']}, Per Page: {data['per_page']}, Total Pages: {data['total_pages']}")

    @skip_in_ci
    @pytest.mark.regression
    def test_last_page_has_correct_number_of_items(self):
        """Test that last page has correct number of items"""
        url = f"{API_BASE_URL}/api/users"

        first_response = requests.get(url, params={"page": 1})
        first_data = first_response.json()
        
        total_pages = first_data["total_pages"]
        total_items = first_data["total"]
        per_page = first_data["per_page"]
        

        last_response = requests.get(url, params={"page": total_pages})
        last_data = last_response.json()
        
        expected_items_on_last_page = total_items % per_page
        if expected_items_on_last_page == 0:
            expected_items_on_last_page = per_page
        
        actual_items_on_last_page = len(last_data["data"])
        assert actual_items_on_last_page == expected_items_on_last_page, \
            f"Last page should have {expected_items_on_last_page} items, got {actual_items_on_last_page}"
        
        print(f"\n✅ Last page (page {total_pages}) has correct number of items: {actual_items_on_last_page}")


class TestHeaders:
    """Test suite for HTTP headers validation"""
    
       
    @pytest.mark.regression
    def test_response_headers(self):
        """Test that response contains expected headers"""
        url = f"{API_BASE_URL}/api/users/1"
        
        response = requests.get(url)
        
        assert response.status_code == 200
        
        assert "Content-Type" in response.headers
        assert "application/json" in response.headers["Content-Type"]
        
        print(f"\n✅ Response headers are correct")
        print(f"   Content-Type: {response.headers['Content-Type']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
