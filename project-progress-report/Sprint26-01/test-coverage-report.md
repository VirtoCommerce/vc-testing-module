# Test Coverage Report

**Report Date:** January 22, 2026  
**Comparison Period:** December 23, 2025 → January 22, 2026  
**Sprint:** 26-01

---

## Executive Summary

This report provides test coverage statistics comparing the state of the test suite on December 23, 2025 with the current state on January 22, 2026.

**Key Achievements:**
- **+40 new tests** added (33% growth)
- **+5 new test files** created
- **3 major features** covered: Pickup Locations, Page Context, Ship To Search

---

## Charts & Visualizations

### Test Coverage Comparison (Dec 23, 2025 vs Jan 22, 2026)

![Test Coverage Comparison](./test-coverage-comparison-chart.png)

### Test Distribution by Feature Area

![Test Distribution](./test-distribution-pie-chart.png)

### Test Coverage Growth Trend

![Growth Trend](./test-growth-trend-chart.png)

---

## Detailed Statistics

### Current State (January 22, 2026)

#### tests_e2e (End-to-End Tests)

| Metric | Count |
|--------|-------|
| **Test Files** | 27 |
| **Total Test Functions** | 48 |
| **Active Tests** | 45 |
| **Ignored Tests** | 3 |

#### tests_graphql (GraphQL API Tests)

| Metric | Count |
|--------|-------|
| **Test Files** | 58 |
| **Total Test Functions** | 113 |
| **Active Tests** | 106 |
| **Ignored Tests** | 7 |

#### Grand Total

| Metric | Count |
|--------|-------|
| **Total Test Files** | 85 |
| **Total Test Functions** | 161 |
| **Active Tests** | 151 |
| **Ignored Tests** | 10 |

---

### Comparison: December 23, 2025 vs January 22, 2026

#### tests_e2e (End-to-End Tests)

| Metric | Dec 23, 2025 | Jan 22, 2026 | Change |
|--------|-------------|--------------|--------|
| **Test Files** | 26 | 27 | +1 |
| **Total Test Functions** | 43 | 48 | **+5** |
| **Ignored Tests** | 3 | 3 | 0 |
| **Active Tests** | 40 | 45 | **+5** |

#### tests_graphql (GraphQL API Tests)

| Metric | Dec 23, 2025 | Jan 22, 2026 | Change |
|--------|-------------|--------------|--------|
| **Test Files** | 54 | 58 | **+4** |
| **Total Test Functions** | 78 | 113 | **+35** |
| **Ignored Tests** | 0 | 7 | +7 |
| **Active Tests** | 78 | 106 | **+28** |

#### Grand Total

| Metric | Dec 23, 2025 | Jan 22, 2026 | Change |
|--------|-------------|--------------|--------|
| **Total Test Files** | 80 | 85 | **+5** |
| **Total Test Functions** | 121 | 161 | **+40** |
| **Active Tests** | 118 | 151 | **+33** |

---

## Newly Added Tests

### New E2E Test Files (+1)

| File | Tests Added |
|------|-------------|
| `test_e2e_ship_to_search_address.py` | 2 |

### New E2E Tests (+5)

| Test Name | File |
|-----------|------|
| `test_e2e_add_multiple_shipping_addresses` | test_e2e_ship_to_search_address.py |
| `test_e2e_search_shipping_address` | test_e2e_ship_to_search_address.py |
| `test_e2e_search_organization_with_special_chars` | test_e2e_multi_organizations.py |
| Enhanced tests | Various files |

### New GraphQL Test Files (+4)

| File | Tests Added |
|------|-------------|
| `test_graphql_pickup_locations.py` | 6 |
| `test_graphql_cart_pickup_locations.py` | 6 |
| `test_graphql_product_pickup_locations.py` | 9 |
| `test_graphql_page_context.py` | 8 |

### New GraphQL Tests by Feature (+35)

| Feature | Tests Added |
|---------|-------------|
| **Pickup Locations (Store)** | 6 |
| **Cart Pickup Locations** | 6 |
| **Product Pickup Locations** | 9 |
| **Page Context** | 8 |
| **Other Enhancements** | 6 |

---

## New Tests - Detailed List

### GraphQL Pickup Locations Tests (6 tests)

1. `test_get_pickup_locations` - Get all pickup locations for store
2. `test_get_pickup_locations_with_pagination` - Get pickup locations with pagination
3. `test_search_pickup_locations_by_keyword` - Search pickup locations by keyword
4. `test_pickup_location_address_structure` - Verify pickup location address structure
5. `test_update_pickup_location` - Update pickup location via WebAPI and verify via GraphQL
6. `test_set_inactive_pickup_location` - Set inactive pickup location via WebAPI and verify via GraphQL

### GraphQL Cart Pickup Locations Tests (6 tests)

1. `test_get_cart_pickup_locations_transfer_required` - Cart pickup locations with transfer required
2. `test_get_cart_pickup_locations_multiple_products` - Cart pickup locations with multiple products
3. `test_cart_pickup_locations_today_availability` - Verify Today availability type
4. `test_cart_pickup_locations_transfer_availability` - Verify Transfer availability type
5. `test_cart_pickup_locations_all_availability_types` - Verify all availability types
6. `test_cart_pickup_locations_today_priority` - Today availability has higher priority

### GraphQL Product Pickup Locations Tests (9 tests)

1. `test_product_pickup_locations_main_ffc` - Product in main FFC (Illinois)
2. `test_product_pickup_locations_ohio_ffc` - Product in Ohio FFC
3. `test_product_pickup_locations_multi_ffc` - Product in multiple FFCs
4. `test_product_pickup_locations_track_inventory_false` - Product with track inventory false
5. `test_product_pickup_locations_european_berlin_billund` - European product Berlin+Billund
6. `test_product_pickup_locations_three_ffcs` - Product in 3 FFCs
7. `test_product_pickup_locations_pagination` - Pagination support
8. `test_product_pickup_locations_availability_types` - Verify availability types
9. `test_product_pickup_locations_address_structure` - Verify address structure

### GraphQL Page Context Tests (8 tests)

1. `test_get_page_context_store_info` - Page context with store info
2. `test_get_page_context_slug_info` - Page context with slug info
3. `test_get_page_context_category_slug_info` - Page context with category slug
4. `test_get_page_context_slug_info_authenticated_user` - Slug info for authenticated user
5. `test_get_page_context_anonymous_user` - Page context for anonymous user
6. `test_get_page_context_authenticated_user` - Page context for authenticated user
7. `test_get_page_context_white_labeling` - White labeling settings
8. `test_get_full_page_context` - Full page context

### E2E Ship To Search Address Tests (2 tests)

1. `test_e2e_add_multiple_shipping_addresses` - Add multiple shipping addresses
2. `test_e2e_search_shipping_address` - Search shipping address functionality

---

## Ignored Tests

### tests_e2e (3 ignored)

| File | Ignored Tests |
|------|---------------|
| `test_e2e_select_language_in_store.py` | 1 |
| `test_e2e_select_pickup_location.py` | 2 |

### tests_graphql (7 ignored)

| File | Ignored Tests |
|------|---------------|
| `test_graphql_cart_pickup_locations.py` | 6 |
| `test_graphql_page_context.py` | 1 |

---

## What's New in the Project

### 1. BOPIS (Buy Online, Pick Up In Store) Support
- Complete pickup locations API testing
- Store, cart, and product-level pickup availability
- Availability types: Today, Transfer, GlobalTransfer
- Multi-fulfillment center (FFC) support

### 2. Page Context GraphQL Operations
- Store context retrieval
- Slug resolution (products, categories)
- User context for anonymous and authenticated users
- White labeling settings support

### 3. Enhanced E2E Testing
- Ship To address search functionality
- Multi-organization management
- Organization sign-up with validation
- WebAPI integration in tests

### 4. Infrastructure Improvements
- Dataset manager refactoring
- WebAPI PATCH request support with JSON Patch media type
- Enhanced fixtures for config, auth, and webapi client

---

## Growth Summary

| Metric | Value |
|--------|-------|
| **Test Functions Growth** | +33% (121 → 161) |
| **Test Files Growth** | +6% (80 → 85) |
| **New Features Covered** | 3 major features |
| **Period** | ~1 month |

---

*Report generated automatically on January 22, 2026*
