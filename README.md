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

## Running the Project

### Start the Mock API Server
```bash
python src/mock_api_server.py
```

### Run Tests
```bash
pytest -v
```

