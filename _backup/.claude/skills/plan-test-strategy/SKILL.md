---
name: plan-test-strategy
description: "Analyze a Jira ticket, feature requirement, or bug report and produce a structured test coverage strategy — what to test, which test types, priority, test data needs"
argument-hint: "<ticket-or-requirement>"
---

## Test Strategy Planning

When given a requirement, feature description, or Jira ticket, produce a structured test strategy.

## Process

### Step 1: Understand the Requirement

- Read the ticket/requirement carefully
- Identify the feature area (cart, checkout, catalog, contacts, orders, quotes, etc.)
- Identify the user roles involved (anonymous, registered, admin, organization member)
- Identify the API surface (GraphQL mutations/queries, REST endpoints, UI pages)

### Step 2: Explore Existing Coverage

Before planning new tests, search for what already exists:

```
# Find existing tests for this domain
tests/graphql/test_<domain>*.py
tests/e2e/test_<domain>*.py
tests/restapi/<module>/test_<domain>*.py
```

Check existing operations classes and page objects that can be reused:
```
gql/operations/<domain>_operations.py
restapi/operations/<domain>_operations.py
page_objects/pages/<domain>.py
page_objects/components/<domain>*.py
```

### Step 3: Design Test Cases

For each behavior, decide:

1. **What to assert** — the specific expected outcome
2. **Test type** — GraphQL (API logic), E2E (UI flow), REST API (admin CRUD)
3. **Setup needed** — markers (`with_user`, `with_cart`), factory fixtures, manual setup
4. **Cleanup needed** — auto (marker), factory fixture, or manual try-finally
5. **Priority** — P0 (critical path), P1 (important), P2 (edge case)

### Step 4: Identify Test Data Needs

- Which dataset entries are required (users, products, categories)?
- Do new dataset entries need to be seeded?
- Are there shared constants to define (addresses, product IDs)?

## Output Format

Produce the strategy in this structure:

```markdown
# Test Strategy: <Feature Name>

## Requirement Summary
<1-3 sentences describing what the feature does>

## Existing Coverage
- **Existing tests:** <list of related test files already in the codebase>
- **Existing operations:** <list of operations classes that can be reused>
- **Existing page objects:** <list of pages/components that can be reused>
- **Gaps:** <what's missing>

## Test Cases

### P0 — Critical Path
| # | Test Name | Type | Description | Setup | Markers |
|---|-----------|------|-------------|-------|---------|
| 1 | test_<name> | GraphQL/E2E/REST | <what it verifies> | <fixtures needed> | <markers> |

### P1 — Important
| # | Test Name | Type | Description | Setup | Markers |
|---|-----------|------|-------------|-------|---------|

### P2 — Edge Cases
| # | Test Name | Type | Description | Setup | Markers |
|---|-----------|------|-------------|-------|---------|

## Test Data Requirements
- **Existing dataset entries needed:** <list>
- **New dataset entries needed:** <list, or "None">
- **Shared constants to define:** <product IDs, usernames, etc.>

## New Infrastructure Needed
- **New operations class:** <Yes/No — which domain>
- **New Pydantic types:** <Yes/No — which types>
- **New page objects:** <Yes/No — which pages>
- **New components:** <Yes/No — which components>
- **New factory fixtures:** <Yes/No — which entities>
- **New fragments:** <Yes/No — which .graphql files>

## Allure Organization
- **Feature labels:** <list of @allure.feature values to use>
- **Example titles:** <sample @allure.title values>

## Notes
<any caveats, dependencies, or risks>
```

## Test Type Decision Guide

| Signal | Recommended Type |
|--------|-----------------|
| Tests a GraphQL mutation/query response | **GraphQL** |
| Tests business logic (cart totals, order creation, user registration) | **GraphQL** |
| Tests UI rendering, navigation, visual state | **E2E** |
| Tests form submission, modal interaction, page transitions | **E2E** |
| Tests admin REST API CRUD operations | **REST API** |
| Tests platform settings, user management, role assignment | **REST API** |
| Tests error handling on an API | **GraphQL** or **REST API** (not E2E) |
| Tests the same logic for anonymous vs. registered user | **GraphQL** (two tests with different markers) |

## Coverage Patterns by Feature Area

### Cart Feature
- Anonymous cart CRUD (GraphQL)
- Registered user cart CRUD (GraphQL + `with_user`)
- Cart merge (GraphQL)
- Cart UI interactions: add, remove, update quantity, clear (E2E + `with_cart`)
- Cart checkout flow (E2E + `with_user` + `with_cart`)

### Catalog Feature
- Product search and filtering (GraphQL)
- Category SEO resolution (GraphQL)
- Product CRUD (REST API + factory fixtures)
- Category CRUD (REST API + factory fixtures)
- Catalog CRUD (REST API + factory fixtures)
- Category page UI: filters, sorting, view switcher (E2E)

### User/Contact Feature
- Registration (GraphQL)
- Sign in/sign out (E2E)
- Contact address management (GraphQL + `with_user`)
- Organization management (REST API)
- Role assignment (REST API + GraphQL)

### Order/Quote Feature
- Order creation from cart (GraphQL + `with_user` + `with_cart`)
- Order listing, filtering, sorting (GraphQL + `with_user`)
- Quote creation and update (GraphQL + `with_user`)
- Checkout E2E flow (E2E + `with_user` + `with_cart`)
