"""
REST API Tests - Works with Local Mock Server
File: tests/test_users.py

Run mock server first: python src/mock_api_server.py
Then run tests: pytest -v tests/test_users.py
"""

import logging
import os
import time

import pytest
import requests

logger = logging.getLogger(__name__)


def get_available_user(base_url, user_ids=[2, 1, 3, 4, 5]):
    """
    Try to get a user, falling back to different IDs if needed
    Returns (response, user_id) tuple with logging
    """
    logger.info(f"Attempting to find available user from IDs: {user_ids}")

    for user_id in user_ids:
        url = f"{base_url}/api/users/{user_id}"
        logger.debug(f"Trying user ID {user_id}")
        response = requests.get(url)

        if response.status_code == 200:
            logger.info(f"✅ Found available user: ID {user_id}")
            return response, user_id
        else:
            logger.debug(f"User ID {user_id} returned {response.status_code}")

    # If we get here, none worked
    logger.error(f"❌ No available users found from {user_ids}")
    return None, None


# Mark to skip in CI
skip_in_ci = pytest.mark.skipif(
    os.getenv("CI") == "true" and "reqres.in" in os.getenv("API_BASE_URL", ""),
    reason="ReqRes API requires API key for this operation",
)

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")
logger.info(f"Tests configured to use API: {API_BASE_URL}")


class TestUsersAPI:
    """Test suite for Users API endpoints"""

    @skip_in_ci
    @pytest.mark.smoke
    def test_get_list_users(self):
        """Test retrieving list of users - GET /api/users"""
        url = f"{API_BASE_URL}/api/users"
        params = {"page": 1}

        logger.info(f"Testing GET {url} with params {params}")
        response = requests.get(url, params=params)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        response_data = response.json()
        assert "data" in response_data, "Response should contain 'data' key"
        assert len(response_data["data"]) > 0, "Data array should not be empty"
        assert "page" in response_data, "Response should contain 'page' key"
        assert response_data["page"] == 1, "Page should be 1"
        assert "per_page" in response_data, "Response should contain 'per_page'"
        assert "total" in response_data, "Response should contain 'total'"

        logger.info(
            f"✅ Found {len(response_data['data'])} users on page 1, "
            f"total: {response_data['total']}"
        )

    @skip_in_ci
    @pytest.mark.smoke
    def test_get_list_users_page_2(self):
        """Test retrieving list of users on page 2 - GET /api/users?page=2"""
        url = f"{API_BASE_URL}/api/users"
        params = {"page": 2}

        logger.info(f"Testing GET {url} with params {params}")
        response = requests.get(url, params=params)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        response_data = response.json()
        assert response_data["page"] == 2, "Page should be 2"
        assert len(response_data["data"]) > 0, "Should have users on page 2"

        logger.info(f"✅ Found {len(response_data['data'])} users on page 2")

    @pytest.mark.regression
    def test_get_single_user(self):
        """Test retrieving a single user by ID - GET /api/users/{id}"""
        user_ids_to_try = [2, 1, 3, 4]

        logger.info(
            f"Testing single user retrieval with fallback IDs: {user_ids_to_try}"
        )

        response = None
        successful_user_id = None
        failed_attempts = []

        for user_id in user_ids_to_try:
            url = f"{API_BASE_URL}/api/users/{user_id}"
            logger.info(f"Attempting to get user ID {user_id}")
            response = requests.get(url)

            if response.status_code == 200:
                successful_user_id = user_id
                logger.info(f"✅ User ID {user_id} successful")
                break
            else:
                failed_attempts.append((user_id, response.status_code))
                logger.warning(
                    f"⚠️  User ID {user_id} failed with status {response.status_code}"
                )

        # Log summary
        if failed_attempts:
            failed_summary = ", ".join(
                [f"ID {uid}: {status}" for uid, status in failed_attempts]
            )
            logger.warning(f"Failed attempts before success: {failed_summary}")

        # Assertions
        assert response is not None, "No response received from API"
        assert successful_user_id is not None, f"All user IDs failed: {failed_attempts}"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # Validate response structure
        response_data = response.json()
        assert "data" in response_data, "Response should contain 'data' key"

        user = response_data["data"]
        assert (
            user["id"] == successful_user_id
        ), f"User ID should be {successful_user_id}"
        assert "email" in user, "User should have email"
        assert "first_name" in user, "User should have first_name"
        assert "last_name" in user, "User should have last_name"
        assert "avatar" in user, "User should have avatar"

        logger.info(
            f"✅ Test passed - User: {user['first_name']} {user['last_name']} "
            f"(ID: {successful_user_id}, Email: {user['email']})"
        )

    @skip_in_ci
    @pytest.mark.negative
    def test_get_user_not_found(self):
        """Test that requesting non-existent user returns 404 - GET /api/users/{id}"""
        url = f"{API_BASE_URL}/api/users/999"

        logger.info(f"Testing 404 response for non-existent user: {url}")
        response = requests.get(url)

        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        logger.info("✅ 404 correctly returned for non-existent user")

    @skip_in_ci
    @pytest.mark.regression
    def test_create_user(self):
        """Test creating a new user - POST /api/users"""
        url = f"{API_BASE_URL}/api/users"
        user_data = {"name": "Adam Majcher", "job": "QA Engineer"}

        logger.info(f"Testing POST {url} with data: {user_data}")
        response = requests.post(url, json=user_data)

        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

        response_data = response.json()
        assert response_data["name"] == user_data["name"], "Name should match"
        assert response_data["job"] == user_data["job"], "Job should match"
        assert "id" in response_data, "Response should contain id"
        assert "createdAt" in response_data, "Response should contain createdAt"

        logger.info(f"✅ Created user with ID: {response_data['id']}")

    @skip_in_ci
    @pytest.mark.regression
    def test_update_user(self):
        """Test updating an existing user - PUT /api/users/{id}"""
        user_id = 2
        url = f"{API_BASE_URL}/api/users/{user_id}"
        update_data = {"name": "Adam Updated", "job": "Senior QA Engineer"}

        logger.info(f"Testing PUT {url} with data: {update_data}")
        response = requests.put(url, json=update_data)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        response_data = response.json()
        assert response_data["name"] == update_data["name"], "Name should be updated"
        assert response_data["job"] == update_data["job"], "Job should be updated"
        assert "updatedAt" in response_data, "Response should contain updatedAt"

        logger.info(f"✅ Updated user at: {response_data['updatedAt']}")

    @skip_in_ci
    @pytest.mark.regression
    def test_patch_user(self):
        """Test partially updating a user - PATCH /api/users/{id}"""
        user_id = 2
        url = f"{API_BASE_URL}/api/users/{user_id}"
        patch_data = {"first_name": "someone"}

        logger.info(f"Testing PATCH {url} with data: {patch_data}")
        response = requests.patch(url, json=patch_data)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        response_data = response.json()
        assert (
            response_data["first_name"] == patch_data["first_name"]
        ), "first_name should be updated"
        assert "updatedAt" in response_data, "Response should contain updatedAt"

        logger.info("✅ Patched user successfully")

    @skip_in_ci
    @pytest.mark.regression
    def test_delete_user(self):
        """Test deleting a user - DELETE /api/users/{id}"""
        user_id = 2
        url = f"{API_BASE_URL}/api/users/{user_id}"

        logger.info(f"Testing DELETE {url}")
        response = requests.delete(url)

        assert response.status_code == 204, f"Expected 204, got {response.status_code}"

        logger.info("✅ User deleted successfully")

    @skip_in_ci
    @pytest.mark.regression
    def test_get_all_users(self):
        """Test retrieving multiple users by iterating through pages"""
        url = f"{API_BASE_URL}/api/users"
        all_users = []

        logger.info("Testing pagination - retrieving all users across pages")

        # Act - Get first page to know total pages
        first_response = requests.get(url, params={"page": 1})
        assert first_response.status_code == 200

        first_data = first_response.json()
        total_pages = first_data["total_pages"]
        all_users.extend(first_data["data"])

        logger.info(
            f"First page retrieved: {len(first_data['data'])} users, {total_pages} total pages"
        )

        # Get remaining pages
        for page in range(2, total_pages + 1):
            logger.debug(f"Fetching page {page}/{total_pages}")
            response = requests.get(url, params={"page": page})
            assert response.status_code == 200
            all_users.extend(response.json()["data"])

        # Assert
        assert len(all_users) == first_data["total"], "Should get all users"

        # Verify no duplicate IDs
        user_ids = [user["id"] for user in all_users]
        assert len(user_ids) == len(set(user_ids)), "All user IDs should be unique"

        logger.info(
            f"✅ Retrieved all {len(all_users)} users across {total_pages} pages"
        )

    @pytest.mark.regression
    def test_user_data_structure(self):
        """Test that user data has all required fields"""
        logger.info("Testing user data structure validation")

        # Use the helper function with logging
        response, user_id = get_available_user(API_BASE_URL, [1, 2, 3, 4])

        assert response is not None, "No available user found"
        assert response.status_code == 200

        user = response.json()["data"]

        logger.debug(f"Validating structure for user ID {user_id}")

        # Check all required fields exist
        required_fields = ["id", "email", "first_name", "last_name", "avatar"]
        for field in required_fields:
            assert field in user, f"User should have '{field}' field"
            assert user[field] is not None, f"'{field}' should not be None"
            assert user[field] != "", f"'{field}' should not be empty"

        # Check data types
        assert isinstance(user["id"], int), "ID should be integer"
        assert isinstance(user["email"], str), "Email should be string"
        assert isinstance(user["first_name"], str), "First name should be string"
        assert isinstance(user["last_name"], str), "Last name should be string"
        assert isinstance(user["avatar"], str), "Avatar should be string"

        # Check email format
        assert "@" in user["email"], "Email should contain @"
        assert "." in user["email"], "Email should contain domain"

        logger.info(
            f"✅ User data structure valid - Sample: {user['first_name']} "
            f"{user['last_name']} ({user['email']})"
        )


class TestResourcesAPI:
    """Test suite for Resources API endpoints"""

    @skip_in_ci
    @pytest.mark.smoke
    def test_get_list_resources(self):
        """Test retrieving list of resources - GET /api/unknown"""
        url = f"{API_BASE_URL}/api/unknown"

        logger.info(f"Testing GET {url}")
        response = requests.get(url)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        response_data = response.json()
        assert "data" in response_data, "Response should contain 'data' key"
        assert len(response_data["data"]) > 0, "Data array should not be empty"

        # Check resource structure
        first_resource = response_data["data"][0]
        assert "id" in first_resource, "Resource should have id"
        assert "name" in first_resource, "Resource should have name"
        assert "year" in first_resource, "Resource should have year"
        assert "color" in first_resource, "Resource should have color"

        logger.info(f"✅ Found {len(response_data['data'])} resources")

    @skip_in_ci
    @pytest.mark.regression
    def test_get_single_resource(self):
        """Test retrieving a single resource - GET /api/unknown/{id}"""
        resource_id = 2
        url = f"{API_BASE_URL}/api/unknown/{resource_id}"

        logger.info(f"Testing GET {url}")
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

        logger.info(
            f"✅ Resource retrieved: {resource['name']} "
            f"(Year: {resource['year']}, Color: {resource['color']})"
        )

    @skip_in_ci
    @pytest.mark.negative
    def test_get_resource_not_found(self):
        """Test that requesting non-existent resource returns 404"""
        url = f"{API_BASE_URL}/api/unknown/999"

        logger.info(f"Testing 404 response for non-existent resource: {url}")
        response = requests.get(url)

        assert response.status_code == 404

        logger.info("✅ 404 correctly returned for non-existent resource")


class TestAuthentication:
    """Test suite for Authentication endpoints"""

    @skip_in_ci
    @pytest.mark.regression
    def test_register_successful(self):
        """Test successful user registration - POST /api/register"""
        url = f"{API_BASE_URL}/api/register"
        user_data = {"email": "eve.holt@reqres.in", "password": "pistol"}

        logger.info(f"Testing POST {url} for registration")
        response = requests.post(url, json=user_data)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        response_data = response.json()
        assert "id" in response_data, "Response should contain id"
        assert "token" in response_data, "Response should contain token"

        logger.info(
            f"✅ Registered successfully with token: {response_data['token'][:10]}..."
        )

    @skip_in_ci
    @pytest.mark.negative
    def test_register_unsuccessful(self):
        """Test registration fails without password - POST /api/register"""
        url = f"{API_BASE_URL}/api/register"
        user_data = {"email": "sydney@fife"}

        logger.info(f"Testing POST {url} with missing password (negative test)")
        response = requests.post(url, json=user_data)

        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        response_data = response.json()
        assert "error" in response_data, "Response should contain error message"

        logger.info(f"✅ Registration failed as expected: {response_data['error']}")

    @skip_in_ci
    @pytest.mark.regression
    def test_login_successful(self):
        """Test successful login - POST /api/login"""
        url = f"{API_BASE_URL}/api/login"
        credentials = {"email": "eve.holt@reqres.in", "password": "cityslicka"}

        logger.info(f"Testing POST {url} for login")
        response = requests.post(url, json=credentials)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        response_data = response.json()
        assert "token" in response_data, "Response should contain token"

        logger.info(f"✅ Login successful with token: {response_data['token'][:10]}...")

    @skip_in_ci
    @pytest.mark.negative
    def test_login_unsuccessful(self):
        """Test login fails without password - POST /api/login"""
        url = f"{API_BASE_URL}/api/login"
        credentials = {"email": "peter@klaven"}

        logger.info(f"Testing POST {url} with missing password (negative test)")
        response = requests.post(url, json=credentials)

        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        response_data = response.json()
        assert "error" in response_data, "Response should contain error message"

        logger.info(f"✅ Login failed as expected: {response_data['error']}")


class TestResponseTiming:
    """Test suite for response time validation"""

    @pytest.mark.performance
    def test_response_time_under_threshold(self):
        """Test that API responds within acceptable time"""
        max_response_time = 5.0  # 5 seconds

        logger.info("Testing response time performance")

        # Use helper to get available user
        response, user_id = get_available_user(API_BASE_URL, [1, 2, 3])

        assert response is not None, "No available user for performance test"
        response_time = response.elapsed.total_seconds()

        assert response.status_code == 200
        assert (
            response_time < max_response_time
        ), f"Response time {response_time:.2f}s exceeds threshold {max_response_time}s"

        logger.info(
            f"✅ Response time: {response_time:.3f}s "
            f"(under {max_response_time}s threshold)"
        )

    @skip_in_ci
    @pytest.mark.performance
    def test_delayed_response(self):
        """Test API with delayed response - GET /api/users?delay=3"""
        url = f"{API_BASE_URL}/api/users"
        params = {"delay": 3}

        logger.info(f"Testing delayed response with {params['delay']}s delay")

        start_time = time.time()
        response = requests.get(url, params=params, timeout=10)
        elapsed_time = time.time() - start_time

        assert response.status_code == 200
        assert (
            elapsed_time >= 2.0
        ), f"Response should be delayed by at least 2 seconds, got {elapsed_time:.2f}s"
        assert (
            elapsed_time < 7.0
        ), f"Response should not take longer than 7 seconds, got {elapsed_time:.2f}s"

        logger.info(f"✅ Delayed response received after {elapsed_time:.2f} seconds")


class TestPagination:
    """Test suite for pagination functionality"""

    @skip_in_ci
    @pytest.mark.regression
    def test_pagination_info(self):
        """Test that pagination information is correct"""
        url = f"{API_BASE_URL}/api/users"

        logger.info("Testing pagination metadata")
        response = requests.get(url, params={"page": 1})
        data = response.json()

        assert "page" in data
        assert "per_page" in data
        assert "total" in data
        assert "total_pages" in data

        # Verify pagination math
        expected_pages = (data["total"] + data["per_page"] - 1) // data["per_page"]
        assert (
            data["total_pages"] == expected_pages
        ), "Total pages calculation should be correct"

        logger.info(
            f"✅ Pagination info correct - Total: {data['total']}, "
            f"Per Page: {data['per_page']}, Total Pages: {data['total_pages']}"
        )

    @skip_in_ci
    @pytest.mark.regression
    def test_last_page_has_correct_number_of_items(self):
        """Test that last page has correct number of items"""
        url = f"{API_BASE_URL}/api/users"

        logger.info("Testing last page item count")

        # Get first page to know total pages
        first_response = requests.get(url, params={"page": 1})
        first_data = first_response.json()

        total_pages = first_data["total_pages"]
        total_items = first_data["total"]
        per_page = first_data["per_page"]

        logger.debug(f"Total pages: {total_pages}, Total items: {total_items}")

        # Act - Get last page
        last_response = requests.get(url, params={"page": total_pages})
        last_data = last_response.json()

        # Calculate expected items on last page
        expected_items_on_last_page = total_items % per_page
        if expected_items_on_last_page == 0:
            expected_items_on_last_page = per_page

        # Assert
        actual_items_on_last_page = len(last_data["data"])
        assert actual_items_on_last_page == expected_items_on_last_page, (
            f"Last page should have {expected_items_on_last_page} items, "
            f"got {actual_items_on_last_page}"
        )

        logger.info(
            f"✅ Last page (page {total_pages}) has correct number of items: "
            f"{actual_items_on_last_page}"
        )


class TestHeaders:
    """Test suite for HTTP headers validation"""

    @pytest.mark.regression
    def test_response_headers(self):
        """Test that response contains expected headers"""
        logger.info("Testing HTTP response headers")

        # Use helper to get available user
        response, user_id = get_available_user(API_BASE_URL, [1, 2, 3])

        assert response is not None, "No available user for header test"
        assert response.status_code == 200

        # Check important headers
        assert "Content-Type" in response.headers
        assert "application/json" in response.headers["Content-Type"]

        logger.info(
            f"✅ Response headers correct - Content-Type: "
            f"{response.headers['Content-Type']}"
        )


if __name__ == "__main__":
    # Run tests with: python test_users.py
    pytest.main([__file__, "-v", "-s", "--log-cli-level=INFO"])
