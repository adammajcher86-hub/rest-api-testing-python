"""
Pytest configuration and fixtures
This file is automatically loaded by pytest
"""

import os

import pytest


@pytest.fixture(scope="session")
def base_url():
    """
    Get base URL from environment variable or use default localhost

    For local testing: http://localhost:5000
    For CI/CD: Set API_BASE_URL environment variable
    """
    return os.getenv("API_BASE_URL", "http://localhost:5000")


@pytest.fixture(scope="session")
def api_info(base_url):
    """
    Provide API information for tests
    """
    return {"base_url": base_url, "timeout": 10, "is_local": "localhost" in base_url}


def pytest_configure(config):
    """
    Register custom markers
    """
    config.addinivalue_line(
        "markers", "smoke: Quick smoke tests for critical functionality"
    )
    config.addinivalue_line("markers", "regression: Full regression test suite")
    config.addinivalue_line("markers", "positive: Positive test scenarios (happy path)")
    config.addinivalue_line(
        "markers", "negative: Negative test scenarios (error handling)"
    )
    config.addinivalue_line("markers", "performance: Performance and timing tests")
    config.addinivalue_line("markers", "api: API integration tests")
