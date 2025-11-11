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
- ✅ Code style: black
- ✅ Ruff


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

## 🔍 Debugging with Logs

Tests include detailed logging. View logs during test execution:
```bash
# Standard logging
pytest -v --log-cli-level=INFO tests/

# Detailed debugging
pytest -v --log-cli-level=DEBUG tests/

# Save logs to file
pytest -v --log-file=test_run.log tests/
```

**Log levels:**
- `INFO` - Test progress and results ✅
- `WARNING` - Retry attempts and fallbacks ⚠️
- `DEBUG` - Detailed request/response data 🔍
- `ERROR` - Critical failures ❌

Example output:
```
INFO     Attempting to get user ID 2
WARNING  ⚠️  User ID 2 failed with status 404
INFO     ✅ User ID 1 successful

## 🔧 Troubleshooting

### Common Issues

**Tests fail with "Connection refused"**
- Make sure the mock API server is running: `python src/mock_api_server.py`
- Check the server is on port 5000: `http://localhost:5000`

**Intermittent 404 errors for specific user IDs**
- Tests include automatic fallback logic that tries multiple user IDs
- Check logs with `--log-cli-level=INFO` to see which IDs were attempted
- This is normal behavior when testing against external APIs

**All tests skipped in CI**
- This is expected - external API requires authentication
- Local tests should pass with mock server: `22/22 passed ✅`

**Slow test execution**
- Some tests include intentional delays (e.g., `test_delayed_response`)
- Use `-m smoke` to run only quick tests
- Average full suite run: ~1 min

