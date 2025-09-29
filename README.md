# Playwright + Python Project Setup

## Prerequisites

0. Install Cursor AI (recommended IDE)
1. Clone/download project and open with Cursor AI (or PyCharm)

Make sure you have the following installed on your system:

- Python (version 3.7 or later)
- pip (Python package manager)

1. **Create and activate a virtual environment**

   ```sh
   python -m venv .venv
   source venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```

2. **Install dependencies**

   ```sh
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Install pre-commit hooks**

   ```sh
   pre-commit install
   ```

   > **Note:** This step needs to be done manually after installing requirements. Pre-commit hooks (including Black formatter) cannot be installed automatically through requirements.txt as this is a Git security feature.

4. **Install Playwright browsers**

   ```sh
   playwright install
   ```

5. **Verify Playwright installation**
   ```sh
   python -c "import playwright; print(playwright.__version__)"
   ```

## Running Tests

To execute your Playwright tests with pytest, run:

```sh
# To run functional tests:
pytest -v -s  tests_graphql/tests/
# To run visual tests:
pytest tests_e2e/tests/ -v -s --show-browser

# Run a specific test
pytest tests_graphql/tests/test_graphql_add_variation_to_cart.py -k test_add_variation_to_cart

# Run with more detailed output
pytest tests_graphql/tests/test_graphql_add_variation_to_cart.py::test_add_variation_to_cart -v -s

```

For running tests in a specific browser, specify it as follows:

```sh
pytest --browser=chromium  # or firefox, webkit
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
python -m scripts.dataset_seeder
```

## Environment Variables

To store authentication tokens and other secrets securely, create a `.env` file:

```ini
TOKEN=your_auth_token_here
```

Then, load environment variables in your test files using:

```python
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
```

## Debugging Tests

- Use `--slowmo` to slow down execution for debugging:
  ```sh
  pytest --headed --slowmo=500  # 500ms delay between steps
  ```
- Run tests in debug mode:
  ```sh
  pytest --headed --debug
  ```

## Generating Tests Automatically

Playwright can generate tests for you by recording actions:

```sh
playwright codegen example.com
```

This opens a browser where you can perform actions, and Playwright generates the corresponding test script.

## Additional Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/en/latest/)

Happy Testing! 🚀
