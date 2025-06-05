# Multi-Browser Login Tests

This project includes comprehensive Playwright tests that verify login functionality across multiple browsers including Chrome, Firefox, Safari, and Edge.

## 🎯 Test Objectives

The tests perform the following actions:
1. **Navigate** to the base URL (from .env configuration)
2. **Click** the login button/link
3. **Fill out** the login form with username "test" and password "pass123"
4. **Verify** the welcome message or successful login

## 🌐 Supported Browsers

- **Chrome** (Chromium) - Primary browser for web testing
- **Firefox** - Mozilla's browser engine
- **Safari** (WebKit) - Apple's browser engine (available on all platforms via Playwright)
- **Edge** (Chromium-based) - Microsoft's modern browser

## 📁 Test Files

- `test_cross_browser_login.py` - Simple parameterized multi-browser test
- `run_multi_browser_tests.py` - Test runner script with advanced options
- `pytest_multi_browser.ini` - Pytest configuration for multi-browser testing

## ⚙️ Configuration

### Environment Variables (.env file)

Create a `.env` file in the project root with:

```bash
# Required
BASE_URL=https://your-app-url.com
TEST_USERNAME=test
TEST_PASSWORD=pass123

# Optional
STORE_ID=your_store_id
USER_EMAIL=test@example.com
FRONT_ADMIN=admin@example.com
BACK_URL=https://admin.your-app.com
API_KEY=your_api_key
```

## 🚀 Running the Tests

### Option 1: Using the Test Runner (Recommended)

```bash
# Run all browsers with GUI
python run_multi_browser_tests.py

# Run specific browsers
python run_multi_browser_tests.py --browsers chromium firefox

# Run in headless mode (faster)
python run_multi_browser_tests.py --headless

# Run each browser individually for better error isolation
python run_multi_browser_tests.py --individual

# Verbose output
python run_multi_browser_tests.py --verbose
```

### Option 2: Using pytest directly

```bash
# Run all browser tests
pytest test_cross_browser_login.py -v

# Run specific browser
pytest test_cross_browser_login.py -k "chromium" -v

# Run with headed browsers (show GUI)
pytest test_cross_browser_login.py --headed -v

# Run with custom configuration
pytest test_cross_browser_login.py -v --browser=chromium --browser=firefox
```

### Option 3: Using the existing project structure

```bash
# Run with the existing e2e test structure
pytest e2e/test_login.py -v --browser=chromium --browser=firefox --browser=webkit
```

## 📊 Test Output

The tests generate:
- **Screenshots** for each browser in `screenshots/` directory
- **HTML reports** in `test-results/` directory  
- **Console output** with detailed step-by-step results
- **Test artifacts** for debugging failed tests

## 🐛 Troubleshooting

### Common Issues

1. **Browser not found error**:
   ```bash
   # Install Playwright browsers
   playwright install
   ```

2. **Permission errors on Windows**:
   ```bash
   # Run PowerShell as Administrator
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Port conflicts**:
   - Ensure no other applications are using the test ports
   - Check if the BASE_URL in .env is accessible

4. **Element not found errors**:
   - The test includes multiple selector strategies
   - Check if your login page uses different selectors
   - Customize the selectors in the test file

### Browser-Specific Notes

- **WebKit (Safari)**: May have different behavior on Windows vs macOS
- **Firefox**: Sometimes slower to load, increase timeouts if needed
- **Chromium**: Most reliable for automated testing

## 🔧 Customization

### Adding New Browsers

To test Microsoft Edge specifically:

```python
@pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit", "msedge"])
def test_login_multi_browser(browser_name, config):
    # Add Edge support in the browser launch logic
    if browser_name == "msedge":
        browser = playwright.chromium.launch(channel="msedge", headless=False)
```

### Custom Selectors

Modify the selector lists in the test files to match your application:

```python
login_selectors = [
    "text=Login",           # Your login button text
    "#login-btn",           # Your login button ID
    ".login-button",        # Your login button class
    "[data-testid='login']" # Your login button test ID
]
```

## 📈 Integration with CI/CD

### GitHub Actions Example

```yaml
name: Multi-Browser Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install
      - name: Run multi-browser tests
        run: python run_multi_browser_tests.py --headless
```

## 🎯 Best Practices

1. **Environment Isolation**: Use separate test environments for different browsers
2. **Parallel Execution**: Run browsers in parallel for faster execution
3. **Error Handling**: The tests include comprehensive error handling and fallbacks
4. **Screenshots**: Always capture screenshots for debugging
5. **Timeouts**: Use appropriate timeouts for different browser speeds

## 🤝 Contributing

To add new test scenarios:
1. Follow the existing test structure
2. Add appropriate error handling
3. Include screenshot captures
4. Update this documentation

Happy Testing! 🎭 