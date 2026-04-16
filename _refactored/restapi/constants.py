"""Read-only test-data templates for REST API tests.

Rules:
- Treat every value as read-only — always spread/copy:
      payload = {**ORGANIZATION_TEMPLATE, "name": ...}
- No environment values (URLs, credentials).
- No test-created state (IDs, entity names produced during a run).
"""

MEMBER_TYPES = ["Contact", "Organization", "Employee", "Vendor"]

ADDRESS_TEMPLATE = {
    "addressType": "BillingAndShipping",
    "countryCode": "USA",
    "countryName": "United States",
    "city": "New York",
    "line1": "123 Main St",
    "postalCode": "10001",
    "regionId": "NY",
}

ORGANIZATION_TEMPLATE = {
    "memberType": "Organization",
    "groups": ["Customers"],
    "addresses": [ADDRESS_TEMPLATE],
}

CONTACT_TEMPLATE = {
    "memberType": "Contact",
    "firstName": "FirstName",
    "lastName": "LastName",
    "addresses": [ADDRESS_TEMPLATE],
}

DEFAULT_LANGUAGE = {"isDefault": True, "languageCode": "en-US"}

CATALOG_TEMPLATE = {
    "isVirtual": False,
    "defaultLanguage": DEFAULT_LANGUAGE,
    "languages": [DEFAULT_LANGUAGE],
    "createdDate": "0001-01-01T00:00:00Z",
}

CATEGORY_TEMPLATE = {
    "isVirtual": False,
    "level": 0,
    "priority": 0,
    "isActive": True,
    "seoObjectType": "Category",
    "seoInfos": [],
    "isInherited": False,
    "createdDate": "0001-01-01T00:00:00Z",
}

PRODUCT_TEMPLATE = {
    "productType": "Physical",
    "weightUnit": "kg",
    "weight": "1.0",
    "height": "10",
    "width": "10",
    "length": "10",
    "images": [],
    "reviews": [
        {
            "languageCode": "en-US",
            "reviewType": "QuickReview",
            "content": "Automated test product",
        }
    ],
}
