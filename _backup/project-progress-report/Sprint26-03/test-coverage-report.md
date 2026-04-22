# Test Coverage Report - 2 Week Comparison

**Report Date:** February 20, 2026
**Comparison Periods:**
- **Previous Period:** January 26 - February 6, 2026 (2 weeks)
- **Current Period:** February 9 - February 20, 2026 (2 weeks)
**Sprint:** 26-03

---

## Executive Summary

This report compares test coverage between two consecutive 2-week periods, showing the evolution of the test suite.

**Key Achievements in Current Period (Feb 9 - Feb 20):**
- **+5 new test functions** added (2.8% growth)
- **+3 new test files** created
- **+5 active tests** enabled (+2.9% growth in active tests)
- **0 ignored tests change** (maintained at 5 ignored)
- **Major focus:** B2C variant selection test rewrite, saved-for-later GraphQL coverage, test data consolidation, dependency security updates

---

## Test Coverage Comparison Charts

### Period Comparison Overview

```
Period 1: Jan 26-Feb 6, 2026  │  Period 2: Feb 9-Feb 20, 2026
────────────────────────────────┼────────────────────────────────
                                │
Total Test Files:           87  │  90   (+3, +3.4%)
Total Test Functions:      178  │  183  (+5, +2.8%)
Active Tests:              173  │  178  (+5, +2.9%)
Ignored Tests:               5  │  5    (0, 0%)
                                │
```

### Test Functions Growth Trend

```
200 ┤
    │                                                    ╭─● 183 (+5)
180 ┤                                         ╭──────────╯
    │                                  ● 178  │
160 ┤                           ╭──────╯      │
    │                     ● 161 │             │
140 ┤                  ╭──╯     │             │
    │             ╭────╯        │             │
120 ┤       ╭─────╯             │             │
    │  ╭────╯                   │             │
100 ┤──╯                        │             │
    └───┴────────────┴──────────┴─────────────┴──────────
     Dec 23       Jan 22      Feb 6        Feb 20
     2025         2026        2026         2026
```

### Active vs Ignored Tests

```
Period 1 (Jan 26-Feb 6):   ████████████████████ 173 Active  ▌ 5 Ignored
                           [97.2% active]

Period 2 (Feb 9-Feb 20):   █████████████████████ 178 Active  ▌ 5 Ignored
                           [97.3% active] ↑ +0.1%
```

---

## Detailed Statistics

### Current State (February 20, 2026)

#### tests_e2e (End-to-End Tests)

| Metric | Count |
|--------|-------|
| **Test Files** | 30 |
| **Total Test Functions** | 68 |
| **Active Tests** | 65 |
| **Ignored Tests** | 3 |
| **Active Rate** | 95.6% |

#### tests_graphql (GraphQL API Tests)

| Metric | Count |
|--------|-------|
| **Test Files** | 60 |
| **Total Test Functions** | 115 |
| **Active Tests** | 113 |
| **Ignored Tests** | 2 |
| **Active Rate** | 98.3% |

#### Grand Total

| Metric | Count |
|--------|-------|
| **Total Test Files** | 90 |
| **Total Test Functions** | 183 |
| **Active Tests** | 178 |
| **Ignored Tests** | 5 |
| **Active Rate** | 97.3% |

---

### Two-Week Period Comparison

#### tests_e2e (End-to-End Tests)

| Metric | Period 1<br>(Jan 26-Feb 6) | Period 2<br>(Feb 9-Feb 20) | Change | % Change |
|--------|---------------------------|---------------------------|--------|----------|
| **Test Files** | 29 | 30 | **+1** | +3.4% |
| **Total Test Functions** | 65 | 68 | **+3** | +4.6% |
| **Active Tests** | 62 | 65 | **+3** | +4.8% |
| **Ignored Tests** | 3 | 3 | 0 | 0% |
| **Active Rate** | 95.4% | 95.6% | **+0.2%** | - |

#### tests_graphql (GraphQL API Tests)

| Metric | Period 1<br>(Jan 26-Feb 6) | Period 2<br>(Feb 9-Feb 20) | Change | % Change |
|--------|---------------------------|---------------------------|--------|----------|
| **Test Files** | 58 | 60 | **+2** | +3.4% |
| **Total Test Functions** | 113 | 115 | **+2** | +1.8% |
| **Active Tests** | 111 | 113 | **+2** | +1.8% |
| **Ignored Tests** | 2 | 2 | 0 | 0% |
| **Active Rate** | 98.2% | 98.3% | **+0.1%** | - |

#### Grand Total

| Metric | Period 1<br>(Jan 26-Feb 6) | Period 2<br>(Feb 9-Feb 20) | Change | % Change |
|--------|---------------------------|---------------------------|--------|----------|
| **Total Test Files** | 87 | 90 | **+3** | +3.4% |
| **Total Test Functions** | 178 | 183 | **+5** | +2.8% |
| **Active Tests** | 173 | 178 | **+5** | +2.9% |
| **Ignored Tests** | 5 | 5 | 0 | 0% |
| **Active Rate** | 97.2% | 97.3% | **+0.1%** | - |

---

## Test Coverage Distribution

### By Test Type (Current State)

```
E2E Tests:      ███████████████████ 68 tests (37.2%)
GraphQL Tests:  ██████████████████████████████████ 115 tests (62.8%)
```

### Growth by Test Type

```
E2E Tests:      +3 tests (+4.6%)  ██████████
GraphQL Tests:  +2 tests (+1.8%)  ██████
```

---

## What Changed in Period 2 (Feb 9 - Feb 20)

### New Test Files

| File | Tests | Status |
|------|-------|--------|
| **test_e2e_select_variant_option.py** | 3 tests | New (replaces 3 old variant files) |
| **test_graphql_get_saved_for_later.py** | 1 test | New feature coverage |
| **test_graphql_move_from_saved_for_later.py** | 1 test | New feature coverage |

### Removed Test Files (Consolidated)

| File | Status |
|------|--------|
| **test_e2e_variation_add_to_cart.py** | Consolidated into test_e2e_select_variant_option.py |
| **test_e2e_variation_option_selection.py** | Consolidated into test_e2e_select_variant_option.py |
| **test_e2e_variation_selector.py** | Consolidated into test_e2e_select_variant_option.py |

### New Components/Pages Created

No new component or page files were created this period. Existing components were refactored:
1. `variation_option_component.py` - Simplified, removed unused properties
2. `variation_selector_component.py` - Simplified, removed unused properties

### Tests Re-enabled or Newly Ignored

No changes to ignored test markers this period. Ignored test count remains at 5.

---

## Major Changes & Improvements

### 1. B2C Variant Selection Test Rewrite (3 tests)
**Commits:** a0f342c (Feb 16), f1c9989 (Feb 16)
- Complete rewrite of B2C variant selection E2E tests for Sport Band product
- Consolidated 3 old test files (831 lines) into 1 focused test file (348 lines)
- Covers: variant picker selection, title/price updates, add-to-cart with cart badge verification
- Added proper cart cleanup with try/finally patterns
- Enhanced test steps with Allure annotations
- **Net reduction of 490 lines** of test code through better design

### 2. Saved-for-Later GraphQL Feature Coverage (2 tests)
- New `test_graphql_get_saved_for_later.py` - Get saved-for-later items
- New `test_graphql_move_from_saved_for_later.py` - Move items from saved-for-later to cart
- Extends cart management test coverage

### 3. B2C Test Data Consolidation
**Commits:** 65a1a19 (Feb 11), c8163d8 (Feb 11)
- Merged 4 separate `b2c_test_*.json` files into main dataset files
- Added explicit ID fields to all product variations for reliable seeding
- Fixed Color/Size property ID mismatches for frontend rendering
- Added 2 B2B Color variations (Red, Blue) for product-b2c-test-simple
- Differentiated Sport Band variation prices by size and color

### 4. Multi-Organizations Test Fix
**Commit:** 243faaa (Feb 18)
- Fixed test_e2e_multi_organizations.py test stability
- Removed unnecessary test assertions (10 lines)

### 5. Platform & Dependency Updates
**Commit:** a42ddf3 (Feb 16)
- Updated platform version and module configurations in backend-packages.json
- Security dependency bumps: aiohttp 3.13.0 → 3.13.3, urllib3 2.2.3 → 2.6.3, pillow 11.3.0 → 12.1.1

### 6. Project Documentation
**Commit:** a36d911 (Feb 11)
- Added CLAUDE.md project guidance file for AI-assisted development

---

## Test Files Modified

### E2E Tests Modified (5 files)

1. `test_e2e_select_variant_option.py` - **NEW** B2C variant selection (replaces 3 files)
2. `test_e2e_multi_organizations.py` - Test stability fix
3. `variation_option_component.py` - Simplified component
4. `variation_selector_component.py` - Simplified component
5. `product_page.py` - Updated for new variant tests

### GraphQL Tests Modified (2 files)

1. `test_graphql_get_saved_for_later.py` - **NEW** Saved-for-later get test
2. `test_graphql_move_from_saved_for_later.py` - **NEW** Move from saved-for-later test

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

- **Previous Period:** 5 ignored tests (2.8% of total)
- **Current Period:** 5 ignored tests (2.7% of total)
- **Status:** Stable - no new tests ignored, no tests re-enabled

---

## Period-over-Period Growth Analysis

### Historical Trend

| Date | Total Tests | Active Tests | Growth Rate |
|------|-------------|--------------|-------------|
| **Dec 23, 2025** | 121 | 118 | - |
| **Jan 22, 2026** | 161 | 151 | +33.1% |
| **Feb 6, 2026** | 178 | 173 | +10.6% |
| **Feb 20, 2026** | 183 | 178 | +2.8% |

### Growth Velocity

```
Dec 23 → Jan 22 (30 days):  +40 tests (+33%)   █████████████████████████
Jan 22 → Feb 6 (15 days):   +17 tests (+11%)   ██████████████
Feb 6 → Feb 20 (14 days):   +5 tests (+2.8%)   ████

Daily Average:
  Sprint 26-01: 1.33 tests/day
  Sprint 26-02: 1.13 tests/day
  Sprint 26-03: 0.36 tests/day (consolidation-focused sprint)
```

---

## Quality Metrics

### Test Reliability (Active Test Rate)

```
Previous Period:  97.2% █████████████████████████████████████████████████
Current Period:   97.3% █████████████████████████████████████████████████  (+0.1%)

Target:          95.0% █████████████████████████████████████████████████
Status:          EXCEEDING TARGET
```

### Code Coverage Impact

- **+3,734 lines** added across all files
- **-3,840 lines** removed (consolidation)
- **Net: -106 lines** (focused on code quality over quantity)
- **Test code: -490 net lines** (831 lines consolidated into 348 lines)
- Strong emphasis on code maintainability and reducing technical debt

### Test Distribution Balance

```
E2E Tests:      37.2%  █████████████
GraphQL Tests:  62.8%  █████████████████████

Balance Status: Well-balanced (target: 30-40% E2E)
```

---

## Key Achievements Summary

| Achievement | Impact |
|-------------|--------|
| **Variant Test Consolidation** | 3 files → 1 file, -490 lines of test code |
| **Saved-for-Later Coverage** | New GraphQL feature fully tested (2 tests) |
| **Test Data Consolidation** | 4 separate data files merged into main dataset |
| **Active Test Rate** | Maintained at 97.3% (above 95% target) |
| **Security Updates** | 3 dependencies bumped (aiohttp, urllib3, pillow) |
| **Platform Update** | Backend packages updated to latest versions |
| **Code Quality** | Allure annotations added, cleanup patterns improved |

---

## Sprint Comparison Summary

### Sprint 26-01 (Dec 23 → Jan 22)
- Duration: ~30 days
- New Tests: +40 (+33%)
- New Files: +5
- Focus: Pickup locations, page context, ship-to-search

### Sprint 26-02 (Jan 26 → Feb 6)
- Duration: 12 days
- New Tests: +17 (+11%)
- New Files: +2
- Focus: Search history, test reliability, CI/CD

### Sprint 26-03 (Feb 9 → Feb 20)
- Duration: 12 days
- New Tests: +5 (+2.8%)
- New Files: +3 (net, after consolidation)
- Focus: Variant test rewrite, saved-for-later, data consolidation

### Combined Impact (Dec 23 → Feb 20)
- Total Duration: ~59 days
- Total New Tests: +62 (+51.2%)
- Total New Files: +10
- Active Test Rate: 97.5% → 97.3% (stable)
- Test Suite Growth: 121 → 183 tests

---

## Recommendations for Next Period

1. **Address Remaining Ignored Tests**
   - Investigate `test_e2e_select_pickup_location` stability issues (2 tests)
   - Review `test_e2e_select_language_in_store` for re-enablement
   - Target: Reduce to 3 or fewer ignored tests (<2% rate)

2. **Resume Test Growth Momentum**
   - Sprint 26-03 focused on consolidation; next sprint should balance new coverage
   - Prioritize untested critical user journeys (e.g., order management, returns)
   - Target: Return to 0.5+ tests/day growth rate

3. **Expand Saved-for-Later Coverage**
   - Build on new GraphQL saved-for-later tests
   - Add E2E tests for saved-for-later UI interactions
   - Cover edge cases (empty list, maximum items, cross-session persistence)

4. **Continue Test Data Quality Improvements**
   - Validate consolidated dataset completeness
   - Add data integrity checks for variation properties
   - Consider automated data validation in CI pipeline

---

*Report generated on February 20, 2026*
*Data sources: Git history analysis, test file counting, pytest marker analysis*
