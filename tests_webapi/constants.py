"""Read-only test-data templates for WebAPI tests.

These replace Katalon `GlobalVariable` entries that held stock test payloads
(addresses, names, member-type lists, default language blocks, etc.).

Rules:
- Treat every value as read-only. Never mutate in place — always spread/copy:
      payload = {**ORGANIZATION_TEMPLATE, "name": ...}
- No environment values (URLs, credentials) belong here — those go through `Config`.
- No test-created state belongs here (IDs returned from the backend, entity names
  produced during a run) — those stay in the test function or a factory fixture.
- Templates are only for modules that need them. Small modules (HealthCheck,
  Utility) can skip entries entirely.
"""

# ---------- Member / Contact / Organization ----------

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

# ---------- Catalog ----------

DEFAULT_LANGUAGE = {"isDefault": True, "languageCode": "en-US"}

CATALOG_TEMPLATE = {
    "isVirtual": False,
    "defaultLanguage": DEFAULT_LANGUAGE,
    "languages": [DEFAULT_LANGUAGE],
    "createdDate": "0001-01-01T00:00:00Z",
}
