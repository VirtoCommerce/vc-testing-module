# Test Coverage Report - 2 Week Comparison

**Report Date:** February 6, 2026
**Comparison Periods:**
- **Previous Period:** January 12-25, 2026 (2 weeks)
- **Current Period:** January 26 - February 6, 2026 (2 weeks)
**Sprint:** 26-02

---

## Executive Summary

This report compares test coverage between two consecutive 2-week periods, showing the evolution of the test suite.

**Key Achievements in Current Period (Jan 26 - Feb 6):**
- **+17 new test functions** added (11% growth)
- **+2 new test files** created
- **+22 active tests** enabled (+15% growth in active tests)
- **-5 ignored tests** (improved test reliability)
- **Major focus:** Search history feature, test stabilization, CI/CD automation

---

## 📊 Test Coverage Comparison Charts

### Period Comparison Overview

```
Period 1: Jan 12-25, 2026  │  Period 2: Jan 26-Feb 6, 2026
────────────────────────────┼────────────────────────────────
                            │
Total Test Files:        85 │  87  (+2, +2.4%)
Total Test Functions:   161 │  178 (+17, +10.6%)
Active Tests:           151 │  173 (+22, +14.6%)
Ignored Tests:           10 │  5   (-5, -50%)
                            │
```

### Test Functions Growth Trend

```
200 ┤
    │                                         ╭─● 178 (+17)
180 ┤                                      ╭──╯
    │                                   ╭──╯
160 ┤                            ╭──────╯
    │                      ● 161 │
140 ┤                   ╭──╯     │
    │              ╭────╯        │
120 ┤        ╭─────╯             │
    │   ╭────╯                   │
100 ┤───╯                        │
    └────┴────────────┴──────────┴──────────
      Dec 23       Jan 22      Feb 6
      2025         2026        2026
```

### Active vs Ignored Tests

```
Period 1 (Jan 12-25):  ████████████████ 151 Active  █ 10 Ignored
                       [93.8% active]

Period 2 (Jan 26-Feb 6): ████████████████████ 173 Active  ▌ 5 Ignored
                         [97.2% active] ↑ +3.4%
```

---

## 📈 Detailed Statistics

### Current State (February 6, 2026)

#### tests_e2e (End-to-End Tests)

| Metric | Count |
|--------|-------|
| **Test Files** | 29 |
| **Total Test Functions** | 65 |
| **Active Tests** | 62 |
| **Ignored Tests** | 3 |
| **Active Rate** | 95.4% |

#### tests_graphql (GraphQL API Tests)

| Metric | Count |
|--------|-------|
| **Test Files** | 58 |
| **Total Test Functions** | 113 |
| **Active Tests** | 111 |
| **Ignored Tests** | 2 |
| **Active Rate** | 98.2% |

#### Grand Total

| Metric | Count |
|--------|-------|
| **Total Test Files** | 87 |
| **Total Test Functions** | 178 |
| **Active Tests** | 173 |
| **Ignored Tests** | 5 |
| **Active Rate** | 97.2% |

---

### Two-Week Period Comparison

#### tests_e2e (End-to-End Tests)

| Metric | Period 1<br>(Jan 12-25) | Period 2<br>(Jan 26-Feb 6) | Change | % Change |
|--------|-------------------------|----------------------------|--------|----------|
| **Test Files** | 27 | 29 | **+2** | +7.4% |
| **Total Test Functions** | 48 | 65 | **+17** | +35.4% |
| **Active Tests** | 45 | 62 | **+17** | +37.8% |
| **Ignored Tests** | 3 | 3 | 0 | 0% |
| **Active Rate** | 93.8% | 95.4% | **+1.6%** | - |

#### tests_graphql (GraphQL API Tests)

| Metric | Period 1<br>(Jan 12-25) | Period 2<br>(Jan 26-Feb 6) | Change | % Change |
|--------|-------------------------|----------------------------|--------|----------|
| **Test Files** | 58 | 58 | 0 | 0% |
| **Total Test Functions** | 113 | 113 | 0 | 0% |
| **Active Tests** | 106 | 111 | **+5** | +4.7% |
| **Ignored Tests** | 7 | 2 | **-5** | -71.4% |
| **Active Rate** | 93.8% | 98.2% | **+4.4%** | - |

#### Grand Total

| Metric | Period 1<br>(Jan 12-25) | Period 2<br>(Jan 26-Feb 6) | Change | % Change |
|--------|-------------------------|----------------------------|--------|----------|
| **Total Test Files** | 85 | 87 | **+2** | +2.4% |
| **Total Test Functions** | 161 | 178 | **+17** | +10.6% |
| **Active Tests** | 151 | 173 | **+22** | +14.6% |
| **Ignored Tests** | 10 | 5 | **-5** | -50% |
| **Active Rate** | 93.8% | 97.2% | **+3.4%** | - |

---

## 🎯 Test Coverage Distribution

### By Test Type (Current State)

```
E2E Tests:      ████████████████ 65 tests (36.5%)
GraphQL Tests:  ██████████████████████████████████ 113 tests (63.5%)
```

### Growth by Test Type

```
E2E Tests:      +17 tests (+35.4%) ████████████████████
GraphQL Tests:  +0 tests (0%)
Ignored Reduced: -5 tests (-50%)   ████████████
```

---

## 🆕 What Changed in Period 2 (Jan 26 - Feb 6)

### New E2E Test File (+1)

| File | Tests | Status |
|------|-------|--------|
| **test_e2e_search_bar.py** | 10+ tests | ✅ New feature coverage |

### New E2E Components Created (+8)

1. `search_bar_component.py` - Search bar interactions
2. `search_history_section_component.py` - Search history display
3. `search_history_section_item_component.py` - Individual history items
4. `search_products_section_component.py` - Product search results
5. `search_products_section_item_component.py` - Individual product results
6. `search_suggestions_dropdown_component.py` - Search suggestions
7. `pickup_location_list_item_component.py` - Pickup location items
8. `select_bopis_map_modal_component.py` - BOPIS map modal

### GraphQL Tests Re-enabled (-5 ignored)

**Pickup Location Tests Stabilized:**
- ✅ Re-enabled 5 cart pickup location tests
- ✅ Enhanced with proper wait states
- ✅ Improved assertions and reliability

---

## 📝 Major Changes & Improvements

### 1. Customer Search History Feature (10+ tests)
**Commit:** 17362c8 (Jan 28)
- Complete E2E coverage for search functionality
- Search history tracking and display
- Product search suggestions
- 513 lines of new test code

### 2. Test Reliability Improvements
**Enhanced Tests:**
- Pickup location filtering tests improved
- Multi-organization tests refactored
- Authentication flow streamlined
- Network idle states added for stability

### 3. Infrastructure & CI/CD
**DevOps Improvements:**
- Docker-based test execution configured
- GitHub Actions workflows for GraphQL tests
- SendGrid integration for email testing
- Backend package tracking added

### 4. Authentication Enhancement
**Auth System Updates:**
- UI-based login implementation
- JWT token handling improved
- User ID extraction from tokens
- Token expiration management

---

## 🔍 Test Files Modified (14 files)

### E2E Tests Modified (8 files)
1. `test_e2e_search_bar.py` - **NEW** Search history feature
2. `test_e2e_merge_carts.py` - Auth flow improvements
3. `test_e2e_multi_organizations.py` - Refactored auth
4. `test_e2e_filter_pickup_locations.py` - Enhanced reliability
5. `test_e2e_ship_to_search_address.py` - Auth improvements
6. `test_e2e_category_page_add_product_to_cart.py` - Improved assertions
7. `test_e2e_create_order.py` - Enhanced flow
8. `test_e2e_clear_cart.py` - Cleanup improvements

### GraphQL Tests Modified (6 files)
1. `test_graphql_cart_pickup_locations.py` - Tests re-enabled (-6 ignored → -5 ignored)
2. `test_graphql_pickup_locations.py` - Enhanced reliability
3. `test_graphql_invite_user.py` - Fixed and marked as ignored
4. `test_graphql_filter_orders.py` - Improved assertions
5. `test_graphql_search_order.py` - Enhanced tests
6. `test_graphql_register_contact.py` - Teardown improvements

---

## 📉 Ignored Tests Analysis

### Current Ignored Tests (5 total)

#### tests_e2e (3 ignored)
| File | Test | Reason |
|------|------|--------|
| `test_e2e_select_language_in_store.py` | Language selection | Under investigation |
| `test_e2e_select_pickup_location.py` | Pickup location (2 tests) | Stability issues |

#### tests_graphql (2 ignored)
| File | Test | Reason |
|------|------|--------|
| `test_graphql_page_context.py` | 1 test | Flaky behavior |
| `test_graphql_invite_user.py` | User invitation | Indexing timing issues |

### Improvement: -5 Ignored Tests 🎉
- **Previous Period:** 10 ignored tests (6.2% of total)
- **Current Period:** 5 ignored tests (2.8% of total)
- **Improvement:** 50% reduction in ignored tests

---

## 📊 Period-over-Period Growth Analysis

### Historical Trend (3 Data Points)

| Date | Total Tests | Active Tests | Growth Rate |
|------|-------------|--------------|-------------|
| **Dec 23, 2025** | 121 | 118 | - |
| **Jan 22, 2026** | 161 | 151 | +33.1% |
| **Feb 6, 2026** | 178 | 173 | +14.6% |

### Growth Velocity

```
Dec 23 → Jan 22 (30 days):  +40 tests (+33%)  █████████████████
Jan 22 → Feb 6 (15 days):   +17 tests (+11%)  ████████

Daily Average:
  Period 1: 1.33 tests/day
  Period 2: 1.13 tests/day
```

---

## 🎯 Quality Metrics

### Test Reliability (Active Test Rate)

```
Previous Period:  93.8% ████████████████
Current Period:   97.2% ████████████████████  (+3.4%)

Target:          95.0% ████████████████
Status:          ✅ EXCEEDING TARGET
```

### Code Coverage Impact

- **+513 lines** of new test code (search feature)
- **+837 net lines** in codebase (including implementation)
- **Test-to-code ratio maintained** at healthy levels

### Test Distribution Balance

```
E2E Tests:      36.5%  ████████████
GraphQL Tests:  63.5%  ████████████████████

Balance Status: ✅ Well-balanced (target: 30-40% E2E)
```

---

## 🚀 Key Achievements Summary

| Achievement | Impact |
|-------------|--------|
| **New Feature Coverage** | Customer search history fully tested |
| **Test Stabilization** | 50% reduction in ignored tests |
| **E2E Growth** | 35% increase in E2E test functions |
| **Active Test Rate** | Improved from 93.8% to 97.2% |
| **Infrastructure** | CI/CD automation with Docker |
| **Code Quality** | Enhanced auth system and refactoring |
| **Component Library** | 8 new reusable UI components |

---

## 📅 Sprint Comparison Summary

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

### Combined Impact (Dec 23 → Feb 6)
- Total Duration: ~45 days
- Total New Tests: +57 (+47%)
- Total New Files: +7
- Active Test Rate: 97.5% → 97.2%

---

## 🎯 Recommendations for Next Period

1. **Continue Test Stabilization**
   - Address remaining 5 ignored tests
   - Target: <2% ignored test rate

2. **Maintain Growth Momentum**
   - Continue 1+ test per day average
   - Focus on critical user journeys

3. **Infrastructure Enhancement**
   - Expand CI/CD coverage
   - Add automated coverage reporting

4. **Component Library Expansion**
   - Reuse new search components
   - Document component patterns

---

*Report generated on February 6, 2026*
*Data sources: Git history analysis, test file counting, pytest marker analysis*
