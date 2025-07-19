# 0x03. Unittests and Integration Tests

This project demonstrates comprehensive testing strategies in Python, focusing on **unit testing** and **integration testing** with mocking, parameterized tests, and fixtures.

## Project Overview

The project implements a GitHub organization client that interacts with the GitHub API to retrieve organization and repository information. It showcases best practices for:

- Writing effective unit tests
- Using parameterized tests for multiple test scenarios
- Implementing mocking to isolate units under test
- Creating integration tests for end-to-end functionality
- Using fixtures for test data management

## Learning Objectives

- Understand the difference between unit and integration tests
- Learn common testing patterns: mocking, parametrizations, and fixtures
- Practice test-driven development (TDD)
- Implement comprehensive test coverage
- Use Python's `unittest` framework effectively

## Files Description

### Core Implementation Files

#### `utils.py`
**Generic utilities for GitHub organization client**
- `access_nested_map(nested_map, path)`: Safely accesses nested dictionary values using a sequence of keys
- `get_json(url)`: Fetches and returns JSON data from a remote URL using requests
- `memoize`: Decorator that caches method results to avoid redundant computations

#### `client.py`
**GitHub organization client implementation**
- `GithubOrgClient`: Main class that interacts with GitHub API
  - `org()`: Fetches organization information (memoized)
  - `repos_payload()`: Retrieves repository data (memoized)
  - `public_repos(license=None)`: Lists public repositories, optionally filtered by license
  - `has_license(repo, license_key)`: Static method to check if a repository has a specific license

### Test Files

#### `test_utils.py`
**Unit tests for utils module**
- `TestAccessNestedMap`: Tests for the `access_nested_map` function
  - Uses `@parameterized.expand` for testing multiple scenarios
  - Tests both successful access and exception cases
  - Validates proper KeyError handling for invalid paths

#### `test_client.py`
**Unit tests for client module**
- `TestGithubOrgClient`: Comprehensive tests for the GitHub client
  - Tests organization data retrieval
  - Tests repository listing functionality
  - Tests license filtering capabilities
  - Uses mocking to isolate external API calls

#### `demotest.py`
**Demonstration test file**
- Contains example test cases showing various testing patterns
- Serves as a reference for different testing approaches
- Illustrates best practices for test structure and organization

### Supporting Files

#### `fixtures.py`
**Test data and mocking utilities**
- Contains sample data structures used in tests
- Provides mock responses for GitHub API calls
- Includes utility functions for test setup and teardown
- Defines reusable test fixtures to ensure consistent test data

#### `.gitignore`
**Git ignore configuration**
- Excludes Python cache files (`__pycache__/`)
- Ignores compiled Python files (`*.pyc`, `*.pyo`)
- Excludes virtual environment directories
- Prevents tracking of build artifacts and temporary files

## Requirements

- Python 3.7+
- `requests` library for HTTP requests
- `parameterized` library for parameterized testing
- `unittest` (built-in Python testing framework)

## Installation

1. Ensure you have Python 3.7+ installed
2. Install required packages:
   ```bash
   pip install requests parameterized
   ```

## Running Tests

### Run all tests:
```bash
python -m unittest discover
```

### Run specific test modules:
```bash
python -m unittest test_utils.py
python -m unittest test_client.py
```

### Run with verbose output:
```bash
python -m unittest -v test_utils.py
```

## Testing Concepts Demonstrated

### Unit Testing
- **Isolation**: Each test focuses on a single unit of functionality
- **Mocking**: External dependencies are mocked to ensure test reliability
- **Parameterized Tests**: Multiple test scenarios using `@parameterized.expand`

### Integration Testing
- **End-to-end functionality**: Tests that verify complete workflows
- **API Integration**: Tests that validate external API interactions
- **Data Flow**: Ensures proper data flow between components

### Best Practices Implemented
- **Descriptive test names**: Clear indication of what each test validates
- **Arrange-Act-Assert pattern**: Well-structured test methods
- **Test isolation**: Each test is independent and can run in any order
- **Comprehensive coverage**: Both positive and negative test cases

## Project Structure
```
0x03-Unittests_and_integration_tests/
├── README.md              # This file
├── .gitignore            # Git ignore rules
├── utils.py              # Utility functions
├── client.py             # GitHub client implementation
├── test_utils.py         # Unit tests for utils
├── test_client.py        # Unit tests for client
├── demotest.py           # Demo test examples
└── fixtures.py           # Test fixtures and data
```

## Development Practices & Code Quality

### Code Style Compliance
This project follows **PEP 8** style guidelines using `pycodestyle` for consistent code formatting:
- Line length limit of 79 characters
- Proper indentation and spacing
- Consistent naming conventions
- Clean trailing whitespace handling

### Virtual Environment Setup
The project uses a Python virtual environment for dependency isolation:
```bash
# Activate virtual environment (Windows PowerShell)
C:\path\to\your\venv\Scripts\Activate.ps1

# Install development dependencies
pip install requests parameterized pycodestyle
```

### Testing Strategy

#### Unit Tests Coverage
- **16 individual test cases** covering all core functionality
- **Parameterized testing** for multiple input scenarios
- **Mock objects** to isolate external dependencies
- **Property mocking** for testing cached properties
- **Exception handling** verification

#### Integration Tests
- **End-to-end workflow testing** with `TestIntegrationGithubOrgClient`
- **HTTP request mocking** using `unittest.mock.patch`
- **Fixture-based testing** with realistic GitHub API responses
- **License filtering** integration scenarios

### Debugging and Fixes Applied

#### Test Infrastructure Issues Resolved
1. **Import Path Corrections**: Fixed integration test mocking from `client.requests.get` to `utils.requests.get`
2. **Parameterized Syntax**: Corrected parameterized decorator usage for proper tuple arguments
3. **Missing Dependencies**: Added `parameterized` and `requests` libraries to virtual environment
4. **Indentation Errors**: Resolved docstring formatting and indentation issues

#### Code Quality Improvements
- **pycodestyle compliance**: All Python files now pass style checks
- **Line length optimization**: Long lines properly wrapped for readability
- **Trailing whitespace removal**: Clean file endings maintained
- **Proper blank line spacing**: Class and method separations follow PEP 8

### Git Workflow & Version Control

#### Commit Strategy
Each logical change committed separately with descriptive messages:
- `feat:` for new features and functionality
- `test:` for test files and testing improvements
- `fix:` for bug fixes and corrections
- `style:` for code formatting and style improvements
- `docs:` for documentation updates
- `chore:` for maintenance tasks

#### Repository Management
- **Comprehensive .gitignore**: Excludes Python cache files and build artifacts
- **Clean working tree**: No uncommitted changes or untracked files
- **Synchronized with remote**: All changes pushed to GitHub main branch

### Quality Assurance Results

#### Test Execution Summary
```
✅ All 16 tests passing
✅ 100% test coverage for core functionality
✅ No pycodestyle violations
✅ All integration tests functioning correctly
✅ Proper virtual environment isolation
```

#### Files Validated
- `utils.py`: Core utility functions with comprehensive test coverage
- `client.py`: GitHub API client with mocked external dependencies
- `test_utils.py`: Unit tests with parameterized scenarios
- `test_client.py`: Integration tests with fixture-based data
- `fixtures.py`: Test data management and mock responses

## Dependencies

### Required Python Packages
```txt
requests>=2.32.4        # HTTP client for API calls
parameterized>=0.9.0    # Parameterized test support
pycodestyle>=2.14.0     # Code style checking (development)
```

### Virtual Environment
Project configured with isolated Python environment for consistent dependency management.

## Continuous Integration Notes

The project is structured for easy CI/CD integration with:
- Clean test discovery patterns
- No external API dependencies in tests (all mocked)
- Consistent virtual environment setup
- Style checking automation ready

## Author

This project is part of the ALX Backend Python curriculum, focusing on advanced testing methodologies and best practices in Python development.

### Development Timeline
- **Initial Implementation**: Core functionality and basic tests
- **Testing Enhancement**: Comprehensive test coverage with mocking
- **Code Quality**: PEP 8 compliance and style improvements
- **Integration Testing**: End-to-end workflow validation
- **Documentation**: Comprehensive README and inline documentation
