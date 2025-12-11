# VirtoCommerce E2E Test Automation - Developer Onboarding

## Executive Summary

The VirtoCommerce Testing Module is an enterprise-grade test automation framework that ensures the quality, reliability, and performance of the VirtoCommerce e-commerce platform. This comprehensive testing solution provides:

- **80 Automated Tests** across GraphQL APIs, end-to-end UI workflows, and platform integration scenarios
- **Multi-Browser Support** for Chromium, Firefox, and WebKit ensuring cross-browser compatibility
- **Type-Safe Development** with auto-generated GraphQL client types for robust API testing
- **CI/CD Integration** with GitHub Actions for continuous quality assurance
- **Flexible Configuration** supporting multiple checkout flows and UI control variations

The framework leverages modern technologies (Playwright + Python + Pytest) to deliver fast, reliable, and maintainable test automation that scales with the VirtoCommerce platform.

---

**Duration:** 90-120 minutes  
**Framework:** Playwright + Python + Pytest  
**Project:** vc-testing-module

## 📋 Session Overview

This onboarding session will equip developers with everything needed to work with the VirtoCommerce E2E test automation project. We'll cover the complete workflow from initial setup through writing and running tests, with hands-on exercises throughout. By the end, each developer will have a working environment and understand how to work with both GraphQL functional tests and E2E visual tests.

### What You'll Learn
- Setting up the complete test automation environment
- Understanding the multi-layer testing architecture (GraphQL, E2E, WebAPI)
- Writing and executing tests with custom configuration options
- Debugging test failures and using Playwright's powerful tools
- Following best practices for test development and maintenance
- Integrating tests into the CI/CD pipeline

---

## 1. Introduction (10 minutes)

### Project Overview and Goals
The VirtoCommerce Testing Module ensures platform quality through comprehensive automated testing:

**Primary Objectives:**
- Validate critical business workflows (cart, checkout, order management)
- Ensure API contract compliance and data integrity
- Verify UI functionality across multiple browsers and configurations
- Enable rapid feedback during development and deployment
- Prevent regressions and maintain platform stability

**Business Value:**
- **Reduced Time-to-Market** - Automated tests provide fast feedback for faster releases
- **Increased Confidence** - Comprehensive coverage ensures platform reliability
- **Cost Efficiency** - Early bug detection reduces expensive production fixes
- **Scalability** - Framework grows with platform features and complexity

### Testing Strategy

**Two Primary Test Suites:**
1. **GraphQL Functional Tests (54 tests)** - Fast API-level validation of business logic
2. **E2E Visual Tests (25 tests)** - Complete user journey validation with real browsers

**Coverage Areas:**
- Cart operations, checkout flows, payment processing
- Catalog search, product discovery, category navigation
- Order management, tracking, and history
- User authentication, authorization, and organization management
- Multi-language support and localization
- Address management and shipping calculations

### Custom Pytest Options
Our framework includes flexible configuration options:
- `--checkout-mode` - Test single-page or multi-step checkout flows
- `--product-quantity-control` - Test stepper or button quantity controls
- `--show-browser` - Visual debugging with browser UI

### Q&A Expectations
- Ask questions anytime during the session
- Hands-on exercises throughout
- Follow-up support available after onboarding

---

## 2. Environment Setup (25 minutes)

### Prerequisites
- **Python 3.7+** installed
- **Git** access to the repository
- **Cursor AI** (recommended) or PyCharm
- pip (Python package manager)

### Installation Steps (Hands-on)

1. **Clone the repository**
   ```bash
   git clone https://github.com/VirtoCommerce/vc-testing-module
   cd vc-testing-module
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Install pre-commit hooks** ⚠️ Important
   ```bash
   pre-commit install
   ```
   *Note: This includes Black formatter and must be done manually for Git security*

5. **Install Playwright browsers**
   ```bash
   playwright install
   ```

6. **Verify installation**
   ```bash
   python -c "import playwright; print(playwright.__version__)"
   ```

7. **Environment configuration**
   - Create `.env` file for secrets:
   ```bash
   TOKEN=your_auth_token_here
   ```

8. **Add test data (optional)**
   ```bash
   python -m dataset.dataset_seeder
   ```

**Hands-on:** Everyone sets up their environment (15 min)

---

## 3. Project Structure Overview (15 minutes)

### Two Main Test Suites

```
vc-testing-module/
├── tests_graphql/          # Functional GraphQL API tests
│   └── tests/
├── tests_e2e/              # Visual E2E browser tests
│   └── tests/
├── graphql_client/         # GraphQL client and code generation
├── dataset/                # Test data seeding
├── .env                    # Environment variables (create this)
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

### Key Files
- `requirements.txt` - Python dependencies
- `.env` - Authentication tokens and secrets
- `conftest.py` - Shared fixtures and custom pytest options
- `graphql_client/python_graphql_codegen.py` - Generate GraphQL types

### Understanding Test Types
- **GraphQL tests** (`tests_graphql/`) - API functional testing
- **E2E tests** (`tests_e2e/`) - Full browser UI testing

---

## 4. Running Tests (25 minutes)

### GraphQL Functional Tests
```bash
# Run all GraphQL tests
pytest -v -s tests_graphql/tests/

# Run specific test
pytest tests_graphql/tests/test_graphql_add_variation_to_cart.py -k test_add_variation_to_cart

# Run with detailed output
pytest tests_graphql/tests/test_graphql_add_variation_to_cart.py::test_add_variation_to_cart -v -s
```

### E2E Visual Tests
```bash
# Run E2E tests (default: headless)
pytest tests_e2e/tests/ -v -s

# Run with visible browser
pytest tests_e2e/tests/ -v -s --show-browser
```

### Browser Selection
```bash
# Specify browser (chromium, firefox, webkit)
pytest --browser=chromium
pytest --browser=firefox
```

### 🎯 Custom Project Options

Our project has special custom options:

**1. Checkout Mode** (single-page or multi-step)
```bash
pytest tests_e2e/tests/ --checkout-mode single-page  # default
pytest tests_e2e/tests/ --checkout-mode multi-step
```

**2. Product Quantity Control** (stepper or button)
```bash
pytest tests_e2e/tests/ --product-quantity-control stepper  # default
pytest tests_e2e/tests/ --product-quantity-control button
```

**3. Show Browser** (headed mode)
```bash
pytest tests_e2e/tests/ --show-browser
```

### Combining Options
```bash
# Test with multi-step checkout, button controls, and visible browser
pytest tests_e2e/tests/ --checkout-mode multi-step --product-quantity-control button --show-browser
```

### Debugging Options
```bash
# Slow motion (500ms delay between steps)
pytest --headed --slowmo=500

# Debug mode
pytest --headed --debug
```

**Demo:** Run tests with different configurations (10 min)

---

## 5. Using Custom Options in Tests (10 minutes)

### Accessing Configuration in Your Tests

```python
def test_example(pytestconfig):
    # Get custom options
    checkout_mode = pytestconfig.getoption("--checkout-mode")
    product_quantity_control = pytestconfig.getoption("--product-quantity-control")
    show_browser = pytestconfig.getoption("--show-browser")
    
    print(f"Checkout mode: {checkout_mode}")
    print(f"Product quantity control: {product_quantity_control}")
    print(f"Show browser: {show_browser}")
    
    # Use these values to adapt test behavior
    if checkout_mode == "multi-step":
        # Test multi-step flow
        pass
```

### Using Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

def test_with_auth():
    # Use TOKEN for authentication
    pass
```

---

## 6. Writing Your First Test (20 minutes)

### Example: GraphQL Test Structure
```python
def test_add_product_to_cart(graphql_client):
    # Arrange - Prepare test data
    product_id = "test-product-123"
    
    # Act - Execute GraphQL mutation
    response = graphql_client.add_to_cart(product_id, quantity=1)
    
    # Assert - Verify results
    assert response.success is True
    assert len(response.cart.items) > 0
```

### Example: E2E Test Structure
```python
def test_checkout_flow(page, pytestconfig):
    checkout_mode = pytestconfig.getoption("--checkout-mode")
    
    # Navigate to product
    page.goto("https://example.com/product")
    
    # Add to cart
    page.click("#add-to-cart")
    
    # Go to checkout
    page.click("#checkout-button")
    
    # Adapt based on checkout mode
    if checkout_mode == "single-page":
        # Fill all fields on one page
        page.fill("#email", "test@example.com")
        page.fill("#address", "123 Main St")
    else:
        # Multi-step flow
        page.fill("#email", "test@example.com")
        page.click("#next-step")
        page.fill("#address", "123 Main St")
    
    # Complete order
    page.click("#place-order")
    
    # Assert
    assert page.locator(".order-confirmation").is_visible()
```

### Locator Best Practices
- Use data-test-id attributes when available
- Prefer role-based selectors: `page.get_by_role("button", name="Submit")`
- Avoid brittle selectors that break with CSS changes

**Hands-on:** Write a simple test together (10 min)

---

## 7. Advanced Features (15 minutes)

### Generating GraphQL Types
```bash
# Regenerate GraphQL types from schema
python graphql_client/python_graphql_codegen.py -s -v
```

### Test Data Management
```bash
# Seed test data
python -m dataset.dataset_seeder
```

### Playwright Code Generator
```bash
# Record actions and generate test code
playwright codegen example.com
```
*Demo this tool - it's incredibly useful!*

### Pre-commit Hooks
- Automatically formats code with Black
- Runs linting checks
- Ensures code quality before commits

---

## 8. Best Practices & Guidelines (10 minutes)

### Code Quality
- Pre-commit hooks enforce formatting (Black)
- Follow existing test patterns
- Keep tests independent
- Use meaningful test names

### When to Use Which Test Suite
- **GraphQL tests** - Fast API testing, business logic validation
- **E2E tests** - User journey testing, visual validation, integration flows

### Common Pitfalls
- Forgetting to activate virtual environment
- Not installing pre-commit hooks
- Hard-coding values instead of using custom options
- Missing `.env` file for authentication

### Testing Different Scenarios
- Always test with different `--checkout-mode` values
- Test with different `--product-quantity-control` values
- Use `--show-browser` when debugging

---

## 9. CI/CD Integration (5 minutes)
- How tests run in CI/CD pipeline
- Configuration for different environments
- Viewing test results
- When tests block deployments

---

## 10. Resources & Getting Help (5 minutes)

### Documentation
- Project README: https://github.com/VirtoCommerce/vc-testing-module
- Playwright Docs: https://playwright.dev/python/
- Pytest Docs: https://docs.pytest.org/

### Getting Help
- Team communication channels
- Code review process
- VirtoCommerce testing team

---

## 11. Q&A and Next Steps (10 minutes)
- Open floor for questions
- Assignment: Write your first test (GraphQL or E2E)
- Schedule follow-up session
- Feedback on onboarding process

---

## 📝 Action Items for Participants

- [ ] Complete environment setup (including pre-commit hooks!)
- [ ] Run GraphQL test suite successfully
- [ ] Run E2E tests with different custom options
- [ ] Create `.env` file with necessary tokens
- [ ] Write one test (GraphQL or E2E) for an assigned feature
- [ ] Test with both `--checkout-mode` options
- [ ] Submit first test for code review

---

## 🚀 Quick Reference Commands

```bash
# Setup (one-time)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pre-commit install
playwright install

# Run tests
pytest -v -s tests_graphql/tests/              # GraphQL tests
pytest tests_e2e/tests/ --show-browser         # E2E with browser visible
pytest tests_e2e/tests/ --checkout-mode multi-step --show-browser

# Utilities
python graphql_client/python_graphql_codegen.py -s -v  # Generate types
python -m dataset.dataset_seeder                       # Seed data
playwright codegen example.com                         # Record tests
```

Happy Testing! 🚀