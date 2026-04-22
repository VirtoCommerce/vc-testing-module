---
name: write-graphql-test
description: "Scaffold GraphQL API test files following project patterns — markers, fixtures, Allure decorators, Pydantic assertions, try-finally cleanup"
argument-hint: "<domain> <test-scenario>"
---

## GraphQL Test Scaffolding

When writing a GraphQL test, follow these patterns exactly.

## Required Imports

```python
import allure
import pytest

from core.clients import GraphQLClient
from gql.operations import CartOperations  # or domain-specific operations
from gql.types import Cart, CartItemInput   # or domain-specific types
from tests.context import Context
from utils.line_item_utils import has_line_item  # cart-specific helper
```

## Allure Conventions

```python
@allure.feature("<Domain> (GraphQL)")   # e.g., "Cart (GraphQL)", "Order (GraphQL)"
@allure.title("<Action description>")   # e.g., "Add bulk items to cart"
```

## Pattern 1: Simple Marker-Driven Test

Use when the `with_cart` / `with_user` fixtures handle setup and teardown automatically.

```python
_REGISTERED_USER = "acme_store_maintainer_1@acme.com"
_PRODUCT_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"

@pytest.mark.graphql
@allure.feature("Cart (GraphQL)")
@allure.title("Anonymous cart creation")
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
def test_cart_anonymous(with_cart: Cart) -> None:
    assert with_cart is not None
    assert with_cart.is_anonymous is True

@pytest.mark.graphql
@allure.feature("Cart (GraphQL)")
@allure.title("Registered user cart creation")
@pytest.mark.with_user(_REGISTERED_USER)
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
def test_cart_registered_user(with_cart: Cart) -> None:
    assert with_cart is not None
    assert with_cart.is_anonymous is False
```

**When to use:** Test only needs a pre-seeded cart and/or authenticated user. No custom setup logic.

## Pattern 2: Manual Operations with Try-Finally Cleanup

Use when you need custom setup, multiple operations, or assertions between operations.

```python
_PRODUCT_1_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"
_PRODUCT_2_ID = "product-acme-laptop-asus-vivobook-16-x1607qa"
_QUANTITY_1 = 3
_QUANTITY_2 = 4

@pytest.mark.graphql
@allure.feature("Cart (GraphQL)")
@allure.title("Add bulk items to cart")
def test_cart_add_bulk_items(graphql_client: GraphQLClient, ctx: Context) -> None:
    cart_ops = CartOperations(client=graphql_client)
    cart: Cart | None = None

    try:
        cart = cart_ops.add_items_to_cart(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            items=[
                CartItemInput(product_id=_PRODUCT_1_ID, quantity=_QUANTITY_1),
                CartItemInput(product_id=_PRODUCT_2_ID, quantity=_QUANTITY_2),
            ],
        )

        assert has_line_item(cart.items, product_id=_PRODUCT_1_ID, quantity=_QUANTITY_1)
        assert has_line_item(cart.items, product_id=_PRODUCT_2_ID, quantity=_QUANTITY_2)
    finally:
        if cart is not None:
            cart_ops.delete_cart(cart_id=cart.id, user_id=ctx.user_id)
```

**When to use:** Custom multi-step operations, assertions on intermediate state, or resources that need manual cleanup.

## Available Fixtures

| Fixture | Scope | Description |
|---------|-------|-------------|
| `graphql_client: GraphQLClient` | function | Auto-closed via context manager |
| `ctx: Context` | function | `store_id`, `user_id`, `currency_code`, `culture_name`, etc. |
| `with_cart: Cart \| None` | function (autouse) | Seeded from `@pytest.mark.with_cart([(...)])` |
| `with_user: AuthProvider` | function | Authenticated from `@pytest.mark.with_user("email")` |
| `dataset: dict` | session | Raw test data from JSON files |
| `global_settings: GlobalSettings` | session | Environment configuration |

## Assertion Patterns

```python
# Pydantic model attribute access (typed)
assert cart.id is not None
assert cart.is_anonymous is True
assert cart.items_quantity == 1
assert cart.total.amount > 0

# Line item helper
from utils.line_item_utils import has_line_item
assert has_line_item(cart.items, product_id=_PRODUCT_ID, quantity=3)

# Error testing
from requests.exceptions import HTTPError
with pytest.raises(ValueError, match="GraphQL errors"):
    cart_ops.get_cart(...)
```

## Rules

1. Every test function MUST have `@pytest.mark.graphql`
2. Every test function MUST have `@allure.feature()` and `@allure.title()`
3. Module-level constants for product IDs, usernames: `_PRODUCT_ID = "..."`
4. Return type annotation: `def test_...(fixtures) -> None:`
5. Use `ctx` fixture for store/user/currency/culture — don't hardcode
6. Prefer marker-driven setup (`with_cart`, `with_user`) over manual setup
7. Always clean up created resources in `finally` blocks when using manual setup
8. Use `allure.step()` for logical groupings when tests have multiple phases
