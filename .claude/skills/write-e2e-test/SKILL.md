---
name: write-e2e-test
description: "Scaffold E2E UI test files following project patterns — Playwright assertions, Page Objects, Components, markers, fixtures, Allure decorators, BrowserStorage"
argument-hint: "<domain> <test-scenario>"
---

## E2E Test Scaffolding

When writing an E2E test, follow these patterns exactly.

## Required Imports

```python
import allure
import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings
from page_objects.pages import CartPage, HomePage, SignInPage  # domain-specific pages
from page_objects.components import ClearCartModal, LineItem    # domain-specific components
from tests.context import Context
```

## Allure Conventions

```python
@allure.feature("<Domain> (E2E)")   # e.g., "Cart (E2E)", "Authentication (E2E)"
@allure.title("<Action description>")  # e.g., "Clear cart", "Sign in with valid credentials"
```

## Pattern 1: Cart Fixture-Driven Test

Use when the `with_cart` marker handles cart setup and teardown automatically.

```python
_PRODUCT_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"
_QUANTITY = 3

@pytest.mark.e2e
@allure.feature("Cart (E2E)")
@allure.title("Clear cart")
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
def test_cart_clear(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    expect(cart_page.line_items).to_be_visible()
    expect(cart_page.line_items).to_have_count(1)
    expect(cart_page.clear_cart_button).to_be_visible()
    expect(cart_page.clear_cart_button).to_be_enabled()

    cart_page.clear_cart_button.click()
    clear_cart_modal = ClearCartModal(
        root=page.locator("[data-test-id='clear-cart-modal']")
    )
    expect(clear_cart_modal.root).to_be_visible()
    expect(clear_cart_modal.yes_button).to_be_visible()

    clear_cart_modal.yes_button.click()
    expect(clear_cart_modal.root).not_to_be_visible()
    expect(cart_page.line_items).not_to_be_visible()
```

## Pattern 2: User Authentication with Form Interaction

Use when testing login flows or pages that require manual form filling.

```python
_USERNAME = "acme_store_employee_1@acme.com"

@pytest.mark.e2e
@allure.feature("Authentication (E2E)")
@allure.title("Sign in with valid credentials")
def test_sign_in_success(global_settings: GlobalSettings, page: Page, ctx: Context) -> None:
    sign_in_page = SignInPage(global_settings=global_settings, page=page)
    sign_in_page.navigate()

    expect(sign_in_page.email_input).to_be_visible()
    expect(sign_in_page.password_input).to_be_visible()
    expect(sign_in_page.sign_in_button).to_be_visible()

    sign_in_page.email_input.fill(_USERNAME)
    sign_in_page.password_input.fill(global_settings.users_password.get_secret_value())
    sign_in_page.sign_in_button.click()

    home_page = HomePage(global_settings=global_settings, page=page)
    expect(page).to_have_url(home_page.url)
    expect(home_page.top_header.account_button.root).to_be_visible()
```

## Pattern 3: Authenticated User with Cart (marker-driven)

Use when a test needs both a signed-in user and a pre-seeded cart.

```python
_USERNAME = "acme_store_maintainer_1@acme.com"
_PRODUCT_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"

@pytest.mark.e2e
@allure.feature("Cart (E2E)")
@allure.title("Update cart item quantity")
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
def test_cart_item_update(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    # ... test actions with authenticated user's cart
```

## Page Object Instantiation

Always pass keyword arguments:

```python
cart_page = CartPage(global_settings=global_settings, page=page)
cart_page.navigate()

# Components instantiated inline from locators
clear_cart_modal = ClearCartModal(root=page.locator("[data-test-id='clear-cart-modal']"))

# Find child components via page methods
line_item = cart_page.find_line_item(sku="product-sku")
```

## BrowserStorage (auth injection)

The `with_user` fixture auto-injects auth to localStorage for E2E tests. For manual auth:

```python
from page_objects.browser_storage import BrowserStorage

storage = BrowserStorage(page)
storage.set_user_id(user_id)                # Anonymous cart association
storage.set_auth(provider.token_info)       # Full auth token injection
```

## Available Fixtures

| Fixture | Scope | Description |
|---------|-------|-------------|
| `page: Page` | function | Playwright page (from pytest-playwright) |
| `global_settings: GlobalSettings` | session | Environment configuration |
| `ctx: Context` | function | Test context from dataset + markers |
| `with_cart: Cart \| None` | function (autouse) | Seeded from `@pytest.mark.with_cart` |
| `with_user: AuthProvider` | function | Auth + auto localStorage for E2E |
| `dataset: dict` | session | Raw test data from JSON files |

## Assertion Patterns

```python
from playwright.sync_api import expect

# URL assertions
expect(page).to_have_url(expected_url)

# Visibility
expect(element).to_be_visible()
expect(element).not_to_be_visible()
expect(element).to_be_enabled()

# Content
expect(element).to_have_text("Expected text")
expect(element).to_have_value(str(quantity))
expect(locator).to_have_count(3)
```

## Locator Conventions

```python
# Primary: data-test-id attributes
page.locator("[data-test-id='clear-cart-button']")

# Data attributes for element state
element.get_attribute("data-product-sku")

# Dynamic locators with interpolation
page.locator(f"[data-product-sku='{sku}']")

# Component root locators
self._root.locator("[data-test-id='quantity-stepper']")
```

## Rules

1. Every test function MUST have `@pytest.mark.e2e`
2. Every test function MUST have `@allure.feature()` and `@allure.title()`
3. Module-level constants for product IDs, usernames: `_PRODUCT_ID = "..."`
4. Return type annotation: `def test_...(fixtures) -> None:`
5. Use `expect()` for all UI assertions — not bare `assert`
6. Use `data-test-id` attributes for locators — prefer over CSS/XPath
7. Navigate via `page_object.navigate()` — not raw `page.goto()`
8. Prefer marker-driven setup (`with_cart`, `with_user`) over manual BrowserStorage
9. Use `allure.step()` for logical groupings when tests have multiple phases
10. No `time.sleep()` — Playwright auto-waits; use `expect()` or `wait_for_selector()`
