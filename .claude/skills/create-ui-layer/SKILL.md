---
name: create-ui-layer
description: "Create Page Objects (MainLayout/CheckoutLayout subclasses) and UI Components (Component subclasses) with Playwright locators and data-test-id conventions"
argument-hint: "<page-or-component>"
---

## UI Layer Scaffolding

When creating Page Objects or UI Components, follow these patterns exactly.

## File Locations

- Layouts: `page_objects/layouts/<layout>.py`
- Pages: `page_objects/pages/<page>.py`
- Components: `page_objects/components/<component>.py`
- Exports: `page_objects/pages/__init__.py`, `page_objects/components/__init__.py`

## Layout Base Class

Layouts provide shared UI sections (header, footer). Pages extend layouts.

```python
from playwright.sync_api import Locator, Page
from core.global_settings import GlobalSettings
from page_objects.components.top_header import TopHeader

class MainLayout:
    def __init__(self, page: Page, global_settings: GlobalSettings) -> None:
        self._global_settings = global_settings
        self._page = page

    @property
    def root(self) -> Locator:
        return self._page.locator(".main-layout")

    @property
    def top_header(self) -> TopHeader:
        return TopHeader(root=self._page.locator("[data-test-id='top-header']"))

    @property
    def cart_quantity_label(self) -> Locator:
        return self._page.locator(
            "[data-test-id='desktop-main-menu-cart-link'] .vc-badge__content"
        )

    def click_outside(self) -> None:
        self._page.locator("body").click()
```

## Page Object Pattern

Pages extend a layout and add page-specific elements and actions.

```python
from playwright.sync_api import Locator
from page_objects.components.line_item import LineItem
from page_objects.components.shipping_details_section import ShippingDetailsSection
from page_objects.layouts.main import MainLayout

class CartPage(MainLayout):
    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/cart"

    @property
    def shipping_details_section(self) -> ShippingDetailsSection:
        return ShippingDetailsSection(
            root=self._page.locator("[data-test-id='shipping-details-section']")
        )

    @property
    def line_items(self) -> Locator:
        return self._page.locator("[data-product-sku]")

    @property
    def clear_cart_button(self) -> Locator:
        return self._page.locator("[data-test-id='clear-cart-button']")

    @property
    def checkout_button(self) -> Locator:
        return self._page.locator("[data-test-id='checkout-button']")

    def find_line_item(self, sku: str) -> LineItem:
        return LineItem(root=self._page.locator(f"[data-product-sku='{sku}']"))

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")
```

**Key patterns:**
- Extend `MainLayout` (or `CheckoutLayout` for checkout pages)
- `url` property from `self._global_settings.frontend_base_url`
- `navigate()` uses `wait_until="load"` (not `networkidle`)
- Element properties return `Locator` or child `Component`
- `find_*` methods return components for dynamic elements
- No assertions in page objects — only element access and actions

## Component Base Class

```python
from playwright.sync_api import Locator

class Component:
    def __init__(self, root: Locator) -> None:
        self._root = root

    @property
    def root(self) -> Locator:
        return self._root
```

Do not add a `wait_for_results()` (or any `wait_for_load_state("networkidle")`) helper. `networkidle` is discouraged by Playwright and hangs on apps with WebSocket/polling traffic. Tests should wait via explicit `expect(locator).to_be_visible()` / `to_have_count(N)` assertions on the specific element they care about — Playwright's auto-wait covers the legitimate cases.

## Concrete Component Pattern

```python
from playwright.sync_api import Locator
from page_objects.components.component import Component
from page_objects.components.add_to_cart_button import AddToCartButton
from page_objects.components.quantity_stepper import QuantityStepper
from page_objects.components.line_item import LineItem

class ProductCard(Component):
    @property
    def sku(self) -> str | None:
        return self._root.get_attribute("data-product-sku")

    @property
    def quantity_stepper(self) -> QuantityStepper:
        return QuantityStepper(
            root=self._root.locator("[data-test-id='quantity-stepper']")
        )

    @property
    def add_to_cart_button(self) -> AddToCartButton:
        return AddToCartButton(
            root=self._root.locator("[data-test-id='add-to-cart-button']")
        )

    @property
    def variations_button(self) -> Locator:
        return self._root.locator(
            f"[data-test-id='variations-{self.sku}-button']"
        ).first

    def find_variation_item(self, sku: str) -> LineItem:
        return LineItem(root=self._root.locator(f"[data-item-sku='{sku}']"))
```

## Simple Component (Modal Example)

```python
from playwright.sync_api import Locator
from page_objects.components.component import Component

class ClearCartModal(Component):
    @property
    def yes_button(self) -> Locator:
        return self._root.locator("[data-test-id='yes-button']")

    @property
    def no_button(self) -> Locator:
        return self._root.locator("[data-test-id='no-button']")
```

## BrowserStorage Helper

```python
from page_objects.browser_storage import BrowserStorage

storage = BrowserStorage(page)
storage.set_user_id(user_id)                # Anonymous cart association
storage.set_auth(provider.token_info)       # Inject auth token
user_id = storage.get_user_id()             # Read from localStorage
```

## Locator Conventions

```python
# Primary: data-test-id attributes
self._page.locator("[data-test-id='clear-cart-button']")

# Data attributes for element state
self._root.get_attribute("data-product-sku")

# Dynamic locators with interpolation
self._page.locator(f"[data-product-sku='{sku}']")

# Scoped to component root
self._root.locator("[data-test-id='quantity-stepper']")

# First match for non-unique elements
self._root.locator(f"[data-test-id='variations-{self.sku}-button']").first

# CSS class fallback (only when data-test-id unavailable)
self._page.locator(".main-layout")
```

## __init__.py Exports

```python
# page_objects/pages/__init__.py
from page_objects.pages.cart import CartPage
from page_objects.pages.home import HomePage
from page_objects.pages.sign_in import SignInPage

# page_objects/components/__init__.py
from page_objects.components.clear_cart_modal import ClearCartModal
from page_objects.components.line_item import LineItem
from page_objects.components.product_card import ProductCard
```

## Rules

1. Pages extend a layout (`MainLayout` or `CheckoutLayout`) — never standalone
2. Components extend `Component` base class — constructor: `__init__(self, root: Locator)`
3. Instantiate with keyword args: `CartPage(global_settings=global_settings, page=page)`
4. Components instantiated with: `LineItem(root=locator)`
5. Use `@property` for all element locators and child components
6. All locators relative to `self._root` in components, `self._page` in pages
7. Use `data-test-id` attributes — prefer over CSS selectors or XPath
8. `navigate()` uses `wait_until="load"` (not `networkidle`)
9. No assertions or test logic in page objects/components
10. No `time.sleep()` and no `networkidle` waits — wait via explicit `expect()` assertions on specific locators
11. Add new pages/components to `__init__.py` exports
12. Type annotations on all properties: `-> Locator`, `-> str | None`, `-> ChildComponent`
