## Project Structure
```
rest-api-testing-python/
├── .github/          # GitHub Actions workflows
├── src/              # Source code
│   └── mock_api_server.py
├── tests/            # Test files
│   ├── __init__.py
│   └── test_users.py
├── pytest.ini        # Pytest configuration
├── requirements.txt  # Dependencies
└── README.md
```

### Running Tests

#### Local Testing (Full Suite - 22/22 tests)
```bash/cmd
# Terminal 1: Start the mock API server
python src/mock_api_server.py

# Terminal 2: Run all tests
pytest -v

# Result: ✅ 22 passed in ~1min
```

### Test Coverage

This project includes **22 comprehensive test cases** covering:
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Authentication & authorization
- ✅ Error handling & negative scenarios
- ✅ Pagination & data validation
- ✅ Response time performance
- ✅ HTTP headers validation


#### CI/CD Testing (4/22 tests)

The CI pipeline runs against a public API (ReqRes.in) which has limitations:
- **4 tests pass** ✅ - Basic GET operations
- **18 tests skipped** ⏭️ - Require API authentication (POST/PUT/DELETE)

This demonstrates:
- ✅ Environment-aware test configuration
- ✅ Graceful handling of external API limitations
- ✅ Professional pytest skip markers

**Why the difference?** The full test suite requires write operations which need API keys on public APIs. 
The local mock server provides complete test coverage without these restrictions.

### Test Organization

Tests are organized by functionality:
- `TestUsersAPI` - User CRUD operations
- `TestResourcesAPI` - Resource management
- `TestAuthentication` - Login/registration
- `TestResponseTiming` - Performance validation
- `TestPagination` - Data pagination
- `TestHeaders` - HTTP header validation

### Running Specific Test Groups
```bash/cmd
# Smoke tests only
pytest -v -m smoke

# Regression tests
pytest -v -m regression

# Performance tests
pytest -v -m performance

# Negative scenarios
pytest -v -m negative
```



