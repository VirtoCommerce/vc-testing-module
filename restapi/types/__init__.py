"""Pydantic models for REST API responses.

Hand-written, conservative — only fields the test suite touches are typed.
`extra="ignore"` drops unknown fields silently so server additions don't break.
A future direction is to generate these from the platform's OpenAPI schema; for
now hand-written keeps the models small and the layering simple.
"""

from restapi.types.base import RestModel
from restapi.types.catalog import Catalog, CatalogLanguage
from restapi.types.category import Category
from restapi.types.order import CustomerOrder, OrderLineItem
from restapi.types.product import Product
from restapi.types.role import Role
from restapi.types.user import User

__all__ = [
    "Catalog",
    "CatalogLanguage",
    "Category",
    "CustomerOrder",
    "OrderLineItem",
    "Product",
    "RestModel",
    "Role",
    "User",
]
