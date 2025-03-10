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
   venv\Scripts\activate     # On Windows
   ```

2. **Install dependencies**
   ```sh
   pip install playwright pytest
   ```

3. **Install Playwright browsers**
   ```sh
   playwright install
   ```

4. **Verify Playwright installation**
   ```sh
   python -c "import playwright; print(playwright.__version__)"
   ```

## Running Tests

To execute your Playwright tests with pytest, run:
```sh
pytest
# Run all tests in the file
# Example:
pytest tests/test_auth.py

# Run a specific test
pytest tests/test_auth.py -k test_user_registration
pytest tests/test_auth.py -k test_user_login

# Run with more detailed output
pytest tests/test_auth.py -v
```

If you want to run Playwright tests in headed mode (with browser UI), use:
```sh
pytest --headed
```

For running tests in a specific browser, specify it as follows:
```sh
pytest --browser=chromium  # or firefox, webkit
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