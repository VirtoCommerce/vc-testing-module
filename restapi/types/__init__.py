"""Pydantic models for REST API responses.

Hand-written, conservative — only fields the test suite touches are typed.
`extra="allow"` (in `RestModel`) keeps unknown server fields round-tripping
through `model_dump()`, so update flows that re-send the response don't
silently drop them.

Future direction: codegen from the platform's OpenAPI schema.
"""

from restapi.types.base import RestModel
from restapi.types.catalog import Catalog, CatalogLanguage
from restapi.types.category import Category
from restapi.types.contact import Contact
from restapi.types.employee import Employee
from restapi.types.member import Member
from restapi.types.order import CustomerOrder, OrderLineItem
from restapi.types.organization import Organization
from restapi.types.pricelist import Pricelist, PricelistAssignment
from restapi.types.product import Product
from restapi.types.promotion import Promotion
from restapi.types.role import Role
from restapi.types.store import Store
from restapi.types.user import User
from restapi.types.vendor import Vendor

__all__ = [
    "Catalog",
    "CatalogLanguage",
    "Category",
    "Contact",
    "CustomerOrder",
    "Employee",
    "Member",
    "OrderLineItem",
    "Organization",
    "Pricelist",
    "PricelistAssignment",
    "Product",
    "Promotion",
    "RestModel",
    "Role",
    "Store",
    "User",
    "Vendor",
]
