# Test Coverage Report - 2 Week Comparison

**Report Date:** March 6, 2026
**Comparison Periods:**
- **Previous Period:** February 9 - February 20, 2026 (2 weeks)
- **Current Period:** February 20 - March 6, 2026 (2 weeks)
**Sprint:** 26-04

---

## Executive Summary

This report compares test coverage between two consecutive 2-week periods, showing the evolution of the test suite.

**Key Achievements in Current Period (Feb 20 - Mar 6):**
- **+14 new test functions** added (7.7% growth)
- **+2 new test files** created
- **+14 active tests** enabled (+7.9% growth in active tests)
- **0 ignored tests change** (maintained at 5 ignored)
- **Major focus:** Pickup locations search, ship-to address rewrite, variations from list view, declarative test markers refactor, organization redesign fixes

---

## Test Coverage Comparison Charts

### Period Comparison Overview

```
Period 1: Feb 9-Feb 20, 2026  |  Period 2: Feb 20-Mar 6, 2026
-------------------------------+-------------------------------
                               |
Total Test Files:           90 |  94   (+4, +4.4%)
Total Test Functions:      183 |  197  (+14, +7.7%)
Active Tests:              178 |  192  (+14, +7.9%)
Ignored Tests:               5 |  5    (0, 0%)
                               |
```

### Test Functions Growth Trend

```
200 +                                                         *-- 197 (+14)
    |                                                    *----'
    |                                              * 183 |
180 +                                       *------'     |
    |                                * 178  |            |
160 +                         *------'      |            |
    |                   * 161 |             |            |
140 +                *--'     |             |            |
    |           *----'        |             |            |
120 +     *-----'             |             |            |
    | *---'                   |             |            |
100 +-'                       |             |            |
    +----+----------+---------+-------------+------------+--
     Dec 23      Jan 22     Feb 6        Feb 20       Mar 6
     2025        2026       2026         2026         2026
```

### Active vs Ignored Tests

```
Period 1 (Feb 9-Feb 20):    #################### 178 Active  | 5 Ignored
                            [97.3% active]

Period 2 (Feb 20-Mar 6):    ####################### 192 Active  | 5 Ignored
                            [97.5% active] +0.2%
```

---

## Detailed Statistics

### Current State (March 6, 2026)

#### tests_e2e (End-to-End Tests)

| Metric | Count |
|--------|-------|
| **Test Files** | 32 |
| **Total Test Functions** | 80 |
| **Active Tests** | 77 |
| **Ignored Tests** | 3 |
| **Active Rate** | 96.3% |

#### tests_graphql (GraphQL API Tests)

| Metric | Count |
|--------|-------|
| **Test Files** | 60 |
| **Total Test Functions** | 115 |
| **Active Tests** | 113 |
| **Ignored Tests** | 2 |
| **Active Rate** | 98.3% |

#### tests_webapi (Web API Tests)

| Metric | Count |
|--------|-------|
| **Test Files** | 2 |
| **Total Test Functions** | 2 |
| **Active Tests** | 2 |
| **Ignored Tests** | 0 |
| **Active Rate** | 100% |

#### Grand Total

| Metric | Count |
|--------|-------|
| **Total Test Files** | 94 |
| **Total Test Functions** | 197 |
| **Active Tests** | 192 |
| **Ignored Tests** | 5 |
| **Active Rate** | 97.5% |

---

### Two-Week Period Comparison

#### tests_e2e (End-to-End Tests)

| Metric | Period 1<br>(Feb 9-Feb 20) | Period 2<br>(Feb 20-Mar 6) | Change | % Change |
|--------|---------------------------|---------------------------|--------|----------|
| **Test Files** | 30 | 32 | **+2** | +6.7% |
| **Total Test Functions** | 68 | 80 | **+12** | +17.6% |
| **Active Tests** | 65 | 77 | **+12** | +18.5% |
| **Ignored Tests** | 3 | 3 | 0 | 0% |
| **Active Rate** | 95.6% | 96.3% | **+0.7%** | - |

#### tests_graphql (GraphQL API Tests)

| Metric | Period 1<br>(Feb 9-Feb 20) | Period 2<br>(Feb 20-Mar 6) | Change | % Change |
|--------|---------------------------|---------------------------|--------|----------|
| **Test Files** | 60 | 60 | 0 | 0% |
| **Total Test Functions** | 115 | 115 | 0 | 0% |
| **Active Tests** | 113 | 113 | 0 | 0% |
| **Ignored Tests** | 2 | 2 | 0 | 0% |
| **Active Rate** | 98.3% | 98.3% | 0% | - |

#### tests_webapi (Web API Tests)

| Metric | Period 1<br>(Feb 9-Feb 20) | Period 2<br>(Feb 20-Mar 6) | Change | % Change |
|--------|---------------------------|---------------------------|--------|----------|
| **Test Files** | 0 | 2 | **+2** | New |
| **Total Test Functions** | 0 | 2 | **+2** | New |
| **Active Tests** | 0 | 2 | **+2** | New |
| **Ignored Tests** | 0 | 0 | 0 | - |
| **Active Rate** | - | 100% | - | - |

#### Grand Total

| Metric | Period 1<br>(Feb 9-Feb 20) | Period 2<br>(Feb 20-Mar 6) | Change | % Change |
|--------|---------------------------|---------------------------|--------|----------|
| **Total Test Files** | 90 | 94 | **+4** | +4.4% |
| **Total Test Functions** | 183 | 197 | **+14** | +7.7% |
| **Active Tests** | 178 | 192 | **+14** | +7.9% |
| **Ignored Tests** | 5 | 5 | 0 | 0% |
| **Active Rate** | 97.3% | 97.5% | **+0.2%** | - |

---

## Test Coverage Distribution

### By Test Type (Current State)

```
E2E Tests:      #################### 80 tests (40.6%)
GraphQL Tests:  ############################### 115 tests (58.4%)
WebAPI Tests:   # 2 tests (1.0%)
```

### Growth by Test Type

```
E2E Tests:      +12 tests (+17.6%)  ####################
GraphQL Tests:  +0 tests (0%)
WebAPI Tests:   +2 tests (New)      ####
```

---

## What Changed in Period 2 (Feb 20 - Mar 6)

### New Test Files

| File | Tests | Status |
|------|-------|--------|
| **test_e2e_add_variations_to_cart_from_list_view.py** | 2 tests | New - Variation cart operations from category list view |
| **test_e2e_product_pickup_locations.py** | 6 tests | New - Pickup locations modal search and selection |

### New Components Created

| Component | Purpose |
|-----------|---------|
| **variation_line_item_component.py** | Variation line items in cart from list view |

### Tests Re-enabled or Newly Ignored

No changes to ignored test markers this period. Ignored test count remains at 5.

### Modified Test Files (16 files)

#### E2E Tests Modified

1. `test_e2e_filter_pickup_locations.py` - Updated after frontend bug fixes
2. `test_e2e_ship_to_search_address.py` - Rewritten with anonymous, authenticated, and search scenarios
3. `test_e2e_multi_organizations.py` - Simplified special chars org search; updated for redesigned org selector
4. `test_e2e_search_bar.py` - Fixed flaky test with networkidle wait
5. `test_e2e_select_variant_option.py` - Pre-test cart cleanup added
6. `test_e2e_category_add_to_cart_viewport.py` - Declarative markers refactor
7. `test_e2e_category_page_add_product_to_cart.py` - Declarative markers refactor
8. `test_e2e_category_price_range_filter.py` - Declarative markers refactor
9. `test_e2e_change_cart_item.py` - Declarative markers refactor
10. `test_e2e_checkout_add_shipping_address.py` - Declarative markers refactor
11. `test_e2e_checkout_select_shipping_address.py` - Declarative markers refactor
12. `test_e2e_checkout_switch_shipping_option.py` - Declarative markers refactor
13. `test_e2e_create_order.py` - Declarative markers refactor
14. `test_e2e_proceed_to_checkout.py` - Declarative markers refactor
15. `test_e2e_select_pickup_location.py` - Declarative markers refactor
16. `test_e2e_shipping_cost.py` - Declarative markers refactor

#### GraphQL Tests Modified (1 file)

1. `test_graphql_reset_password.py` - Minor update

#### Infrastructure Modified

1. `conftest.py` - Added FEATURE_MARKERS hook for declarative test skipping
2. `pytest.ini` - Registered new markers (checkout_mode, quantity_control, range_filter)
3. `CLAUDE.md` - Comprehensive architecture documentation update

---

## Major Changes & Improvements

### 1. Declarative Feature Markers Refactor (12+ files)
**PR:** #120 (VCST-4676) | **Commits:** d095196, bf62b22 (Feb 24)
- Replaced imperative `if config["CHECKOUT_MODE"] == ...` branching with `@pytest.mark.checkout_mode("single-page")` declarative markers
- Added `FEATURE_MARKERS` mapping in conftest.py for auto-skipping
- Refactored 12+ E2E test files to use new marker pattern
- Registered `checkout_mode`, `quantity_control`, and `range_filter` markers in pytest.ini
- Reduces code duplication and improves test readability

### 2. Pickup Locations Search Tests (6 tests)
**PRs:** #117, #118 (VCST-4649), #122 (VCST-4650) | **Commits:** c074835 (Feb 20), 9a13fd7 (Feb 23), 3032a0c (Feb 26)
- New E2E tests for product pickup locations modal
- Search by full name, partial name, and out-of-stock product scenarios
- Stabilized with proper wait states and assertions
- Updated after frontend bug fixes

### 3. Variations from List View (2 tests)
**PR:** #119 (VCST-4672) | **Commits:** 9029f38, 0cb3bfa (Feb 24)
- New E2E test for adding variations to cart from category list view
- New E2E test for updating variation quantity from list view
- New `variation_line_item_component.py` component
- Enhanced `product_card_component.py` and `category_page.py`

### 4. Ship-to Address Test Rewrite (3+ scenarios)
**Commit:** 596729a (Feb 26)
- Complete rewrite of ship-to address tests
- Now covers anonymous, authenticated, and search scenarios
- Improved test structure and reliability

### 5. Organization Redesign Fix
**PR:** #121 (VCST-4685) | **Commits:** 5cb175f, d389f0f (Feb 25-26)
- Updated `AccountMenuComponent` for redesigned organization selector
- Simplified special chars organization search test
- Fixed organization switching after UI redesign

### 6. Test Stability Improvements
**Commits:** c8c9fbf, b80d311 (Feb 25)
- Fixed flaky search history test by waiting for networkidle after navigation
- Added pre-test cart cleanup to prevent stale state failures

---

## Ignored Tests Analysis

### Current Ignored Tests (5 total)

#### tests_e2e (3 ignored)

| File | Test | Reason |
|------|------|--------|
| `test_e2e_select_language_in_store.py` | `test_e2e_select_language_in_store` | Under investigation |
| `test_e2e_select_pickup_location.py` | `test_e2e_select_pickup_location_single_page_checkout` | Stability issues |
| `test_e2e_select_pickup_location.py` | `test_e2e_select_pickup_location_multi_step_checkout` | Stability issues |

#### tests_graphql (2 ignored)

| File | Test | Reason |
|------|------|--------|
| `test_graphql_page_context.py` | `test_get_page_context_white_labeling` | Flaky behavior |
| `test_graphql_invite_user.py` | `test_invite_user` | Indexing timing issues |

### Improvement/Change Summary

- **Previous Period:** 5 ignored tests (2.7% of total)
- **Current Period:** 5 ignored tests (2.5% of total)
- **Status:** Stable - percentage decreased due to total test growth

---

## Period-over-Period Growth Analysis

### Historical Trend

| Date | Total Tests | Active Tests | Growth Rate |
|------|-------------|--------------|-------------|
| **Dec 23, 2025** | 121 | 118 | - |
| **Jan 22, 2026** | 161 | 151 | +33.1% |
| **Feb 6, 2026** | 178 | 173 | +10.6% |
| **Feb 20, 2026** | 183 | 178 | +2.8% |
| **Mar 6, 2026** | 197 | 192 | +7.7% |

### Growth Velocity

```
Dec 23 -> Jan 22 (30 days):  +40 tests (+33%)    #########################
Jan 22 -> Feb 6 (15 days):   +17 tests (+11%)    ##############
Feb 6 -> Feb 20 (14 days):   +5 tests (+2.8%)    ####
Feb 20 -> Mar 6 (14 days):   +14 tests (+7.7%)   ###########

Daily Average:
  Sprint 26-01: 1.33 tests/day
  Sprint 26-02: 1.13 tests/day
  Sprint 26-03: 0.36 tests/day (consolidation-focused sprint)
  Sprint 26-04: 1.00 tests/day (growth resumed)
```

---

## Quality Metrics

### Test Reliability (Active Test Rate)

```
Previous Period:  97.3% #################################################
Current Period:   97.5% ################################################# (+0.2%)

Target:          95.0% #################################################
Status:          EXCEEDING TARGET
```

### Code Coverage Impact

- **+1,596 lines** added across all files
- **-1,271 lines** removed (refactoring and simplification)
- **Net: +325 lines** (balanced growth with quality improvements)
- 30 files changed across the codebase
- Strong emphasis on architectural improvements (declarative markers)

### Test Distribution Balance

```
E2E Tests:      40.6%  #################
GraphQL Tests:  58.4%  #########################
WebAPI Tests:   1.0%   #

Balance Status: Well-balanced (target: 30-40% E2E, slightly above due to E2E growth)
```

---

## Key Achievements Summary

| Achievement | Impact |
|-------------|--------|
| **Declarative Markers Refactor** | 12+ files refactored, cleaner test architecture |
| **Pickup Locations Coverage** | 6 new E2E tests for pickup modal search |
| **Variations from List View** | 2 new E2E tests + new component |
| **Ship-to Address Rewrite** | Complete test rewrite with 3 scenarios |
| **Organization Redesign Support** | Tests updated for new UI |
| **Test Stability** | Flaky test fixes, cart cleanup patterns |
| **Active Test Rate** | Improved to 97.5% (above 95% target) |
| **Growth Resumed** | 1.00 tests/day (up from 0.36 in Sprint 26-03) |

---

## Sprint Comparison Summary

### Sprint 26-02 (Jan 26 -> Feb 6)
- Duration: 12 days
- New Tests: +17 (+11%)
- New Files: +2
- Focus: Search history, test reliability, CI/CD

### Sprint 26-03 (Feb 9 -> Feb 20)
- Duration: 12 days
- New Tests: +5 (+2.8%)
- New Files: +3 (net, after consolidation)
- Focus: Variant test rewrite, saved-for-later, data consolidation

### Sprint 26-04 (Feb 20 -> Mar 6)
- Duration: 14 days
- New Tests: +14 (+7.7%)
- New Files: +4
- Focus: Pickup locations, variations from list view, declarative markers, org redesign

### Combined Impact (Dec 23 -> Mar 6)
- Total Duration: ~73 days
- Total New Tests: +76 (+62.8%)
- Total New Files: +14
- Active Test Rate: 97.5% -> 97.5% (stable, exceeding target)
- Test Suite Growth: 121 -> 197 tests

---

## VCST Tickets Covered

| Ticket | Description | PRs |
|--------|-------------|-----|
| **VCST-4649** | Product page pickup locations list, search, select on map | #117, #118 |
| **VCST-4650** | Update pickup locations search tests | #122 |
| **VCST-4672** | Add variations to cart from list view | #119 |
| **VCST-4676** | Refactor: replace imperative config branching with declarative markers | #120 |
| **VCST-4685** | Fix switch between organizations after redesign | #121 |

---

## Recommendations for Next Period

1. **Address Remaining Ignored Tests**
   - Investigate `test_e2e_select_pickup_location` stability issues (2 tests)
   - Review `test_e2e_select_language_in_store` for re-enablement
   - Target: Reduce to 3 or fewer ignored tests (<2% rate)

2. **Expand WebAPI Test Coverage**
   - New test layer introduced with 2 tests; expand to cover key platform endpoints
   - Target: 5+ WebAPI tests by next sprint

3. **Maintain Growth Momentum**
   - Sprint 26-04 recovered to 1.00 tests/day; sustain this rate
   - Prioritize untested critical user journeys (order management, returns, wishlist)

4. **Leverage Declarative Markers Pattern**
   - Apply declarative markers to any remaining tests with config branching
   - Consider extending FEATURE_MARKERS for new config dimensions

5. **Continue Component Library Growth**
   - 37 reusable components now available
   - Document component catalog for team reference

---

*Report generated on March 6, 2026*
*Data sources: Git history analysis, test file counting, pytest marker analysis*
