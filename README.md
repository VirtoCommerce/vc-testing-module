# VirtoCommerce Testing Module

## Overview

The VirtoCommerce Testing Module is a comprehensive, enterprise-grade test automation framework designed to ensure the quality, reliability, and performance of VirtoCommerce platform components. Built on Playwright and Python, this framework provides robust end-to-end testing capabilities for both API and UI layers of the VirtoCommerce ecosystem.

### Purpose

This testing module serves as the quality assurance backbone for VirtoCommerce, enabling continuous validation of critical business workflows, API functionality, and user experiences across the platform. It supports both pre-deployment verification and continuous monitoring of production-like environments.

## Key Features

### 🎯 Multi-Layer Testing Strategy
- **GraphQL API Testing** - 54 functional tests covering cart operations, catalog search, order management, organization workflows, and payment processing
- **End-to-End UI Testing** - 25 visual tests validating complete user journeys from product browsing to order completion
- **Web API Testing** - Platform-level API validation for administrative and integration scenarios

### 🔧 Framework Capabilities
- **Flexible Test Configuration** - Custom pytest options for different checkout flows (single-page/multi-step) and UI controls
- **Cross-Browser Support** - Tests execute on Chromium, Firefox, and WebKit browsers
- **Parallel Execution** - High-performance test execution with built-in retry mechanisms
- **Visual Regression Testing** - Automated screenshot comparison with pixelmatch integration
- **Test Data Management** - Automated dataset seeding with configurable test scenarios

### 🚀 Developer Experience
- **Type-Safe GraphQL Client** - Auto-generated Python types from GraphQL schema ensuring compile-time safety
- **Rich Reporting** - Allure integration for comprehensive test reporting and analytics
- **Pre-commit Hooks** - Automated code formatting (Black) and quality checks
- **Interactive Debugging** - Playwright Inspector and trace viewer for test troubleshooting
- **Environment Flexibility** - Easy configuration for multiple environments via `.env` files

### 📊 Test Coverage Areas
- **Cart & Checkout Operations** - Add to cart, cart merging, payment processing, shipping calculations
- **Catalog & Search** - Product discovery, filtering, SEO validation, category navigation
- **Order Management** - Order creation, tracking, history, and quote management
- **User Management** - Authentication, authorization, organization switching, contact management
- **Localization** - Multi-language support, currency handling, regional settings
- **Address Management** - Shipping addresses, billing addresses, address favorites

### 🛡️ Quality Assurance Features
- **Automated Retry Logic** - Built-in retry mechanisms for flaky test scenarios
- **Request Tracking** - Network request monitoring and validation
- **Authentication Management** - Secure token handling and session management
- **CI/CD Integration** - GitHub Actions workflows for automated test execution
- **Code Quality Enforcement** - Pre-commit hooks with Black formatter and linting

## Technology Stack

### Core Framework
- **Playwright** - Modern browser automation with multi-browser support
- **Python 3.7+** - Primary programming language
- **Pytest** - Advanced testing framework with powerful fixtures and plugins

### Testing Libraries
- **pytest-playwright** - Playwright integration for pytest
- **pytest-base-url** - Base URL management for test environments
- **pytest-retry** - Automatic retry logic for flaky tests
- **pytest-image-snapshot** - Visual regression testing capabilities
- **Allure** - Comprehensive test reporting and analytics

### API Testing
- **gql** - GraphQL client library
- **graphql-core** - GraphQL implementation for Python
- **requests** - HTTP library for REST API testing

### Code Quality
- **Black** - Opinionated code formatter
- **pre-commit** - Git hooks for automated quality checks
- **isort** - Import statement organization

### Utilities
- **python-dotenv** - Environment variable management
- **Faker** - Test data generation
- **Pandas** - Data manipulation and analysis
- **Rich** - Terminal output formatting

## Quick Start Summary

This repository contains **80+ automated tests** covering GraphQL APIs, end-to-end user workflows, and platform integration scenarios. The framework is production-ready and actively maintained, with CI/CD integration for continuous quality assurance.

**Test Distribution:**
- 54 GraphQL functional tests
- 25 E2E UI tests  
- 1 Web API test
- Configurable test scenarios for different platform configurations

## Getting Started

### Prerequisites

**Recommended IDE:** Cursor AI or PyCharm

**Required Software:**
- Python (version 3.7 or later)
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/VirtoCommerce/vc-testing-module
   cd vc-testing-module
   ```

2. **Create and activate a virtual environment**

   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**

   ```sh
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Install pre-commit hooks**

   ```sh
   pre-commit install
   ```

   > **Note:** This step needs to be done manually after installing requirements. Pre-commit hooks (including Black formatter) cannot be installed automatically through requirements.txt as this is a Git security feature.

5. **Install Playwright browsers**

   ```sh
   playwright install
   ```

6. **Configure environment variables**
   
   Create a `.env` file in the project root with your environment-specific settings:
   ```ini
   FRONTEND_BASE_URL=your_frontend_url
   BACKEND_BASE_URL=your_backend_url
   STORE_ID=your_store_id
   ADMIN_USERNAME=your_admin_username
   ADMIN_PASSWORD=your_admin_password
   USERS_PASSWORD=your_users_password
   ```

7. **Verify installation**
   ```sh
   python -c "import playwright; print(playwright.__version__)"
   pytest --collect-only  # Should discover 80+ tests
   ```

## Project Architecture

```
vc-testing-module/
├── tests_graphql/          # GraphQL API functional tests (54 tests)
│   ├── tests/             # Test cases for cart, catalog, orders, etc.
│   └── ...
├── tests_e2e/              # End-to-end UI tests (25 tests)
│   ├── tests/             # User journey and workflow tests
│   └── ...
├── tests_webapi/           # Web API platform tests
├── graphql_client/         # Auto-generated GraphQL client
│   ├── mutations/         # GraphQL mutation operations
│   ├── queries/           # GraphQL query operations
│   └── types/             # Type-safe GraphQL schema
├── dataset/                # Test data seeding and management
│   ├── dataset_seeder.py  # Automated data population
│   └── data/              # Test data configurations
├── fixtures/               # Pytest fixtures for authentication, config, etc.
├── utils/                  # Helper utilities and common functions
├── conftest.py            # Global pytest configuration and custom options
├── pytest.ini             # Pytest settings and markers
└── requirements.txt       # Python dependencies
```

### Key Components

- **GraphQL Client**: Type-safe GraphQL operations with automatic schema synchronization
- **Fixtures**: Reusable test components for authentication, page objects, and configuration
- **Dataset Seeder**: Automated test data generation for reproducible test environments
- **Custom Pytest Options**: Flexible test configuration for different platform scenarios

## Running Tests

### Quick Start Commands

```sh
# Run all GraphQL functional tests
pytest -v -s tests_graphql/tests/

# Run all E2E UI tests (headless)
pytest tests_e2e/tests/ -v -s

# Run E2E tests with visible browser
pytest tests_e2e/tests/ -v -s --show-browser

# Run specific test by name
pytest tests_graphql/tests/test_graphql_add_variation_to_cart.py -k test_add_variation_to_cart

# Run with detailed output
pytest tests_graphql/tests/test_graphql_add_variation_to_cart.py::test_add_variation_to_cart -v -s
```

### Browser Selection

Tests support multiple browsers for cross-browser validation:

```sh
pytest --browser=chromium  # Google Chrome/Edge (default)
pytest --browser=firefox   # Mozilla Firefox
pytest --browser=webkit    # Safari
```

## Custom Pytest Options

This project includes custom pytest options that can be used to configure test behavior:

### Available Options

- `--checkout-mode`: Select checkout flow to test
  - Values: `single-page` (default), `multi-step`
  - Example: `pytest tests_e2e/tests/ --checkout-mode single-page`

- `--product-quantity-control`: Choose quantity selector type
  - Values: `stepper` (default), `button`
  - Example: `pytest tests_e2e/tests/ --product-quantity-control stepper`

- `--show-browser`: Run browser in headed mode (shows browser UI)
  - Boolean flag (no value needed)
  - Example: `pytest tests_e2e/tests/ --show-browser`

### Usage Examples

```sh
# Run with default values
pytest tests_e2e/tests/

# Run with custom checkout mode
pytest tests_e2e/tests/ --checkout-mode multi-step

# Run with custom product quantity control
pytest tests_e2e/tests/ --product-quantity-control button

# Run with headed browser
pytest tests_e2e/tests/ --show-browser

# Combine multiple options
pytest tests_e2e/tests/ --checkout-mode single-page --product-quantity-control stepper --show-browser
```

### Accessing Options in Tests

You can access these options in your test files using the `pytestconfig` fixture:

```python
def test_example(pytestconfig):
    checkout_mode = pytestconfig.getoption("--checkout-mode")
    product_quantity_control = pytestconfig.getoption("--product-quantity-control")
    show_browser = pytestconfig.getoption("--show-browser")
    
    print(f"Checkout mode: {checkout_mode}")
    print(f"Product quantity control: {product_quantity_control}")
    print(f"Show browser: {show_browser}")
```

## Utility Commands

### GraphQL Types Generation
Generate GraphQL types:
```sh
python graphql_client/python_graphql_codegen.py -s -v
```

### Dataset Seeding
Add test data:
```sh
python -m dataset.dataset_seeder

```

## Advanced Configuration

### Environment Variables

Environment variables are loaded automatically from the `.env` file. Access them in your tests:

```python
import os
from dotenv import load_dotenv

load_dotenv()
backend_url = os.getenv("BACKEND_BASE_URL")
frontend_url = os.getenv("FRONTEND_BASE_URL")
```

### CI/CD Integration

The project includes GitHub Actions workflows for automated testing:
- **GraphQL Tests Workflow** (`.github/workflows/graphql-tests.yml`)
- **E2E Tests Workflow** (`.github/workflows/e2e-tests.yml`)

Tests run automatically on pull requests and can be triggered manually for any branch.

## Development Workflow

### Test Development Best Practices

1. **Use Type-Safe GraphQL Operations**
   - Regenerate types after schema changes: `python graphql_client/python_graphql_codegen.py -s -v`
   - Leverage auto-completion and type checking in your IDE

2. **Follow Naming Conventions**
   - Test files: `test_<suite>_<feature>.py`
   - Test functions: `test_<action>_<expected_outcome>`
   - Use descriptive names that explain the test purpose

3. **Leverage Fixtures**
   - Reuse existing fixtures from `conftest.py` and `fixtures/`
   - Create new fixtures for reusable test components
   - Use appropriate fixture scopes (session, module, function)

4. **Write Independent Tests**
   - Tests should not depend on execution order
   - Each test should set up its own data
   - Use the dataset seeder for consistent test data

5. **Handle Flaky Tests**
   - The framework includes automatic retry logic (configured in `pytest.ini`)
   - Add appropriate waits for async operations
   - Use Playwright's auto-waiting features

### Debugging Tests

```sh
# Slow motion mode for visual debugging
pytest tests_e2e/tests/ --headed --slowmo=500

# Show browser while running
pytest tests_e2e/tests/ --show-browser

# Run with detailed output
pytest tests_e2e/tests/ -v -s

# Debug specific test
pytest tests_graphql/tests/test_graphql_add_item_to_cart.py -v -s
```

### Playwright Test Generation

Generate test code by recording browser interactions:

```sh
playwright codegen https://your-frontend-url.com
```

This opens a browser and code generator that creates Playwright commands as you interact with the page.

### Code Quality

Pre-commit hooks automatically enforce code quality:
- **Black** - Code formatting (PEP 8 compliant)
- **isort** - Import statement organization
- All checks run before each commit

Manual code quality check:
```sh
pre-commit run --all-files
```

## Contributing

### Adding New Tests

1. Choose the appropriate test suite:
   - `tests_graphql/` - For API functional tests
   - `tests_e2e/` - For UI and user journey tests
   - `tests_webapi/` - For platform API tests

2. Create a new test file following naming conventions

3. Use existing fixtures and patterns from similar tests

4. Add appropriate pytest markers:
   ```python
   @pytest.mark.graphql  # For GraphQL tests
   @pytest.mark.e2e      # For E2E tests
   @pytest.mark.webapi   # For WebAPI tests
   ```

5. Ensure tests pass locally before submitting

6. Pre-commit hooks will validate code quality

### Test Data Management

Seed test data using the dataset seeder:
```sh
python -m dataset.dataset_seeder
```

Configure test data in `dataset/dataset_config.py` and `dataset/dataset.json`.

## Troubleshooting

### Common Issues

**Tests failing with authentication errors:**
- Verify `.env` file contains correct credentials
- Check token expiration and refresh if needed

**Browser not launching:**
- Reinstall browsers: `playwright install --force`
- Check system dependencies: `playwright install-deps`

**Import errors:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Pre-commit hooks not running:**
- Reinstall hooks: `pre-commit install`
- Check Git configuration

## Documentation

- **Setup Checklist**: See `Setup project checklist.md` for detailed onboarding
- **Developer Onboarding**: See `project-overview.md` for comprehensive training guide
- [Playwright Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/en/latest/)
- [VirtoCommerce Documentation](https://docs.virtocommerce.org/)

## Support

For questions, issues, or contributions:
- Create an issue in the GitHub repository
- Contact the VirtoCommerce testing team
- Review existing tests for patterns and examples

---

**Built with ❤️ by the VirtoCommerce Team**

Happy Testing! 🚀
