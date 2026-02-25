# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Test automation framework for VirtoCommerce e-commerce platform. Uses Playwright + Python + pytest for GraphQL API and E2E UI testing.

## Common Commands

### Running Tests

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

# Browser selection
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
pre-commit run --all-files  # Run Black formatter (120 char line length)
```

Note: Black is the **only** pre-commit hook (no isort/flake8/mypy in pre-commit despite isort being in requirements.txt).

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
```

## Architecture

### Directory Structure

- **tests_graphql/tests/** - GraphQL API functional tests
- **tests_e2e/tests/** - End-to-end UI tests
- **tests_e2e/pages/** - Page Object Model classes (inherit from `MainLayoutPage`)
- **tests_e2e/components/** - Reusable UI component wrappers (~38 components)
- **tests_webapi/tests/** - Web API platform tests
- **graphql_client/** - Auto-generated type-safe GraphQL client (mutations/, queries/, types/)
- **graphql_operations/** - High-level GraphQL operation wrappers organized by domain
- **fixtures/** - Pytest fixtures (auth, config, graphql_client, dataset, requests_tracker, webapi_client)
- **dataset/data/** - JSON test data configuration files for seeding (29 entity files)

### Declarative Feature Markers (Key Pattern)

Tests declare their required configuration via pytest markers instead of branching on config values at runtime. The `pytest_runtest_setup` hook in `conftest.py` auto-skips tests when their marker doesn't match the current config:

```python
# In conftest.py - maps marker names to config keys
FEATURE_MARKERS = {
    "checkout_mode": "CHECKOUT_MODE",
    "quantity_control": "PRODUCT_QUANTITY_CONTROL",
    "range_filter": "RANGE_FILTER_TYPE",
}
```

**Usage in tests:**
```python
@pytest.mark.e2e
@pytest.mark.checkout_mode("single-page")      # Skipped if CHECKOUT_MODE != "single-page"
@pytest.mark.quantity_control("stepper")        # Skipped if PRODUCT_QUANTITY_CONTROL != "stepper"
def test_example(page, config):
    ...
```

This replaces imperative `if config["CHECKOUT_MODE"] == "single-page"` branching. When writing new tests that depend on a specific checkout mode, quantity control, or range filter type, always use the declarative marker.

### Test Markers

Tests must use appropriate pytest markers:
- `@pytest.mark.graphql` - GraphQL API tests
- `@pytest.mark.e2e` - End-to-end UI tests
- `@pytest.mark.webapi` - Web API tests
- `@pytest.mark.ignore` - Tests to skip
- `@pytest.mark.checkout_mode("single-page"|"multi-step")` - Requires specific checkout mode
- `@pytest.mark.quantity_control("stepper"|"button")` - Requires specific quantity control
- `@pytest.mark.range_filter("slider"|"default")` - Requires specific range filter type

### GraphQL Two-Layer Architecture

**Layer 1 - `graphql_client/`** (auto-generated): Raw query/mutation classes with parametrized `return_fields` string. Each class accepts a GraphQL client and executes a single operation.

**Layer 2 - `graphql_operations/`** (handwritten): Domain operation classes (CartOperations, CatalogOperations, UserOperations, etc.) that compose Layer 1 classes with fragment constants.

**Fragment system:** `graphql_operations/*/fragments/` contains Python string constants for GQL field selection sets. Operations pass these to `return_fields` rather than hardcoding field selections.

**Important:** `graphql_client.execute()` returns plain Python `dict`s, not typed instances. Access fields as `cart["id"]`, not `cart.id`.

```python
# GraphQL test pattern
@pytest.mark.graphql
def test_example(graphql_client, config, dataset):
    operations = CartOperations(graphql_client)
    result = operations.add_item_to_cart(payload)
    assert result["id"] is not None
```

### Page Object Model & Components

**Pages** inherit from `MainLayoutPage` which provides shared header elements (cart link, account menu, search bar, language/currency selectors). Constructor takes `(page, config)`. URL is a `@property` from config. `navigate()` does `goto()` + `wait_for_load_state("networkidle")`.

**Components** wrap a root `Locator` and expose sub-elements as `@property`. They are page-agnostic (no page reference, all locators relative to `self.element`). Key components:
- `QuantityStepperComponent` - for `quantity_control=stepper`
- `AddToCartComponent` - for `quantity_control=button`
- Both appear in `LineItemComponent`, `ProductCardComponent`, `VariationLineItemComponent`

**Locator strategy:** All element locators use `data-test-id` attributes (e.g., `[data-test-id='line-item']`).

### E2E Authentication Patterns

**Full page auth** (checkout/order tests):
```python
auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)
```
Sets HTTP headers + localStorage (`auth` token + `user-id`).

**Headless cart setup + page handoff** (simpler cart tests):
```python
# Set up cart server-side via GraphQL
cart_operations.add_item_to_cart(...)
# Give only user-id to page to find the cart
auth.set_local_storage_user_id(page, user["id"])
```

**GraphQL-only auth** (no page):
```python
auth.authenticate(username, password)  # No page argument
# ... do GraphQL operations ...
auth.clear_token()  # Cleanup
```

### E2E Test Pattern

```python
@pytest.mark.e2e
@allure.title("Test description for Allure report")
def test_example(page, config, auth, dataset, graphql_client):
    with allure.step("Setup"):
        # Auth + data setup
    with allure.step("Action"):
        page_object = SomePage(page, config)
        page_object.navigate()
    with allure.step("Assertion"):
        expect(page).to_have_url(page_object.url)
```

Tests use `@allure.title()` and `with allure.step()` blocks for structured Allure reports.

### Configuration

- Environment variables loaded from `.env` file (OS env vars override `.env`)
- Config fixture provides access: `config["FRONTEND_BASE_URL"]`, `config["BACKEND_BASE_URL"]`, `config["STORE_ID"]`
- Defaults defined in `fixtures/config.py`: `CHECKOUT_MODE=single-page`, `PRODUCT_QUANTITY_CONTROL=stepper`, `RANGE_FILTER_TYPE=slider`
- Required `.env` vars: `FRONTEND_BASE_URL`, `BACKEND_BASE_URL`, `STORE_ID`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `USERS_PASSWORD`

### Dataset System

- JSON files in `dataset/data/` define seed requests with `method`, `endpoint`, `payload_type`, `data`, optional `priority`
- File stems are converted to camelCase keys: `product_inventories.json` → `dataset["productInventories"]`
- Placeholders: `{ENV:VARIABLE_NAME}` (from .env), `{PAYLOAD_ITEM:property}` (from current data item)
- Seeding respects `priority` field for dependency ordering (lower = first)
- `payload_type="single"` sends one request per item; `payload_type="array"` sends all items in one request

### Fixture Scopes

- **Session-scoped:** `config`, `auth`, `graphql_client`, `dataset`, `webapi_client`, `browser_context_args`, `browser_type_launch_args`
- **Function-scoped:** `requests_tracker`, `screenshot_on_failure` (autouse)

### Test Retry and Reporting

- Automatic retry: 1 retry configured in pytest.ini (`--retries=1`)
- Screenshots captured on failure to `screenshots/failures/` and attached to Allure
- Allure reporting: results saved to `allure-results/` (cleaned each run via `--clean-alluredir`)
- Default expect timeout: 30 seconds
- Default viewport: 1440x900
