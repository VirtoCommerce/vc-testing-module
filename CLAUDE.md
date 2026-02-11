# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an enterprise-grade test automation framework for VirtoCommerce e-commerce platform. It uses Playwright and Python to provide end-to-end testing capabilities for both GraphQL API and UI layers.

## Common Commands

### Running Tests

**Create and activate a virtual environment**

   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```

```bash
# Run all GraphQL tests
pytest -v -s tests_graphql/tests/

# Run all E2E tests (headless)
pytest tests_e2e/tests/ -v -s

# Run E2E tests with visible browser
pytest tests_e2e/tests/ -v -s --show-browser

# Run specific test file
pytest tests_graphql/tests/test_graphql_add_item_to_cart.py -v -s

# Run single test by name
pytest tests_graphql/tests/test_graphql_add_item_to_cart.py::test_add_item_to_anonymous_cart -v -s

# Run by marker (exclude ignored tests)
pytest -m "graphql and not ignore"
pytest -m "e2e and not ignore"
```

### Browser Selection

```bash
pytest --browser=chromium   # Default
pytest --browser=firefox
pytest --browser=webkit
```

### Custom Test Options

```bash
--checkout-mode single-page|multi-step    # Checkout flow type (default: single-page)
--product-quantity-control stepper|button  # Quantity selector type (default: stepper)
--show-browser                             # Run browser in headed mode
```

### Code Quality

```bash
pre-commit run --all-files  # Run Black formatter and other checks
```

### Utility Commands

```bash
# Generate GraphQL types from schema
python graphql_client/python_graphql_codegen.py -s -v

# Seed test data to backend
python -m dataset.dataset_manager --seed

# Seed specific entities only
python -m dataset.dataset_manager --seed currencies languages fulfillment_centers

# Fetch payloads without seeding
python -m dataset.dataset_manager

# Record Playwright tests
playwright codegen https://your-frontend-url.com
```

## Architecture

### Directory Structure

- **tests_graphql/tests/** - GraphQL API functional tests (54 tests)
- **tests_e2e/tests/** - End-to-end UI tests (25 tests)
- **tests_e2e/pages/** - Page Object Model classes
- **tests_e2e/components/** - Reusable UI component wrappers
- **graphql_client/** - Auto-generated type-safe GraphQL client (mutations/, queries/, types/)
- **graphql_operations/** - High-level GraphQL operation wrappers organized by domain (cart, catalog, user, order, etc.)
- **fixtures/** - Pytest fixtures (auth, config, graphql_client, dataset, requests_tracker, webapi_client)
- **dataset/data/** - JSON test data configuration files for seeding

### Key Patterns

**Test Markers:** Tests must use appropriate pytest markers:
- `@pytest.mark.graphql` - GraphQL API tests
- `@pytest.mark.e2e` - End-to-end UI tests
- `@pytest.mark.webapi` - Web API tests
- `@pytest.mark.ignore` - Tests to skip

**GraphQL Test Pattern:**
```python
@pytest.mark.graphql
def test_example(graphql_client, config, dataset):
    operations = SomeOperations(graphql_client)
    response = operations.do_something(payload)
    assert response["field"] is not None
```

**E2E Test Pattern:**
```python
@pytest.mark.e2e
def test_example(page, config):
    page_object = SomePage(page, config)
    page_object.navigate()
    expect(page).to_have_url(page_object.url)
```

### Configuration

- Environment variables loaded from `.env` file
- Config fixture provides access: `config["FRONTEND_BASE_URL"]`, `config["BACKEND_BASE_URL"]`, `config["STORE_ID"]`
- Defaults defined in `fixtures/config.py`: CHECKOUT_MODE, PRODUCT_QUANTITY_CONTROL, RANGE_FILTER_TYPE

### Dataset Placeholders

In `dataset/data/*.json` files:
- `{ENV:VARIABLE_NAME}` - Substitutes value from .env file
- `{PAYLOAD_ITEM:property}` - Substitutes value from current data item

### Code Formatting

Black formatter with 120-character line length (enforced via pre-commit hooks).

## Test Retry and Reporting

- Automatic retry: 1 retry configured in pytest.ini
- Screenshots captured on failure to `screenshots/failures/`
- Allure reporting: results saved to `allure-results/`
- Default expect timeout: 30 seconds
- Default viewport: 1440x900
