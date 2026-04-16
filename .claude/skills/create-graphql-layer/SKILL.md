---
name: create-graphql-layer
description: "Create GraphQL Operations classes (BaseOperations subclass with auto-fragment injection) and Pydantic GqlModel types for response/input types"
argument-hint: "<entity>"
---

## GraphQL Layer Scaffolding

When creating GraphQL Operations classes or Pydantic types, follow these patterns exactly.

## File Locations

- Operations: `gql/operations/<entity>_operations.py`
- Response types: `gql/types/<entity>.py`
- Input types: `gql/types/<entity>_input.py`
- Fragments: `gql/fragments/<entity>.graphql`
- Exports: `gql/operations/__init__.py`, `gql/types/__init__.py`

## GqlModel Base Class

All GraphQL types MUST inherit from `GqlModel`:

```python
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class GqlModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,      # snake_case -> camelCase
        populate_by_name=True,         # Accept both forms
    )
```

## Response Type Pattern

```python
from gql.types.base import GqlModel
from gql.types.money import Money
from gql.types.line_item import LineItem

class Cart(GqlModel):
    id: str
    store_id: str                       # Alias: storeId
    is_anonymous: bool                  # Alias: isAnonymous
    has_physical_products: bool
    customer_id: str
    total: Money
    sub_total: Money
    items_count: int
    items_quantity: int
    items: list[LineItem]
    payments: list[Payment] = []        # Optional lists default to []
    shipments: list[Shipment] = []
    coupons: list[Coupon] = []
```

**Key patterns:**
- Inherit from `GqlModel` — never `BaseModel` directly
- Use snake_case field names — `to_camel` auto-aliases to camelCase
- Optional/nullable fields: `field: str | None = None`
- Optional lists: `field: list[Type] = []`
- Nested models compose naturally

## Input Type Pattern

```python
from pydantic import ConfigDict, Field
from gql.types.base import GqlModel

class CartItemInput(GqlModel):
    model_config = ConfigDict(alias_generator=None, populate_by_name=True)

    product_id: str = Field(serialization_alias="productId")
    quantity: int = 1
```

**Key patterns:**
- Input types override `alias_generator=None` to prevent auto-aliasing on deserialization
- Use `Field(serialization_alias="productId")` for explicit output aliasing
- Serialize with `model_dump(by_alias=True)` — produces `{"productId": "...", "quantity": 1}`

## Operations Class Pattern

```python
from gql.operations.base_operations import BaseOperations, gql
from gql.types.cart import Cart
from gql.types.cart_item_input import CartItemInput

class CartOperations(BaseOperations):
    def get_cart(
        self,
        store_id: str,
        user_id: str,
        currency_code: str,
        culture_name: str,
        cart_id: str | None = None,
    ) -> Cart | None:
        # fmt: off
        query = gql("""
            query GetCart($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $cartId: String) {
              cart(storeId: $storeId, userId: $userId, currencyCode: $currencyCode, cultureName: $cultureName, cartId: $cartId) {
                ...CartFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={
                "storeId": store_id,
                "userId": user_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
                "cartId": cart_id,
            },
        )
        data = result["data"]["cart"]
        return Cart.model_validate(data) if data else None

    def add_items_to_cart(
        self,
        store_id: str,
        user_id: str,
        items: list[CartItemInput],
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart:
        # fmt: off
        mutation = gql("""
            mutation AddItemsCart($command: InputAddItemsType!) {
              addItemsCart(command: $command) {
                ...CartFragment
              }
            }
        """)
        # fmt: on
        command = {
            "storeId": store_id,
            "userId": user_id,
            "cartItems": [i.model_dump(by_alias=True) for i in items],
            **({"currencyCode": currency_code} if currency_code else {}),
            **({"cultureName": culture_name} if culture_name else {}),
        }
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": command},
        )
        return Cart.model_validate(result["data"]["addItemsCart"])

    def delete_cart(self, cart_id: str, user_id: str) -> bool:
        # fmt: off
        mutation = gql("""
            mutation RemoveCart($command: InputRemoveCartType!) {
              removeCart(command: $command)
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"cartId": cart_id, "userId": user_id}},
        )
        return result["data"]["removeCart"]
```

## Auto-Fragment Injection

`BaseOperations._build_query(operation)` automatically:
1. Scans `gql/fragments/*.graphql` for fragment definitions
2. Finds all `...FragmentName` spreads in the operation
3. Recursively collects transitive fragment dependencies
4. Concatenates fragment definitions + operation into a single query string

**Fragment file example** (`gql/fragments/cart.graphql`):
```graphql
fragment CartFragment on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  total { ...MoneyFragment }
  subTotal { ...MoneyFragment }
  itemsCount
  itemsQuantity
  items { ...LineItemFragment }
  payments { ...PaymentFragment }
  shipments { ...ShipmentFragment }
  coupons { ...CouponFragment }
}
```

**You only write `...CartFragment` in operations — `_build_query()` handles the rest.**

## __init__.py Exports

```python
# gql/operations/__init__.py
from gql.operations.cart_operations import CartOperations
from gql.operations.order_operations import OrderOperations

# gql/types/__init__.py
from gql.types.cart import Cart
from gql.types.cart_item_input import CartItemInput
from gql.types.order import Order
```

## Rules

1. Operations classes extend `BaseOperations` — constructor: `__init__(self, client: GraphQLClient)`
2. All query/mutation strings wrapped in `gql("""...""")`
3. Use `# fmt: off / # fmt: on` around multi-line GraphQL strings
4. `self._build_query(query)` for auto-fragment injection — ALWAYS use this
5. Return Pydantic models (not dicts): `Cart.model_validate(data)`
6. Return `None` for nullable queries: `return Cart.model_validate(data) if data else None`
7. Input lists use `model_dump(by_alias=True)`: `[i.model_dump(by_alias=True) for i in items]`
8. Conditional optional params: `**({"key": val} if val else {})`
9. All types inherit from `GqlModel` — never `BaseModel`
10. Add new types to `__init__.py` exports
11. Create fragment `.graphql` file for any new entity type
