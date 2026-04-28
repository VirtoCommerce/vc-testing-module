# Generate Test Coverage Report

You are generating a test coverage report for the VirtoCommerce testing module. Follow these steps precisely.

## Step 1: Determine Sprint ID and Dates

Ask the user for the following information:
- **Sprint ID** (e.g., `26-03`) - used for the report folder and header
- **Current period start date** (e.g., `February 7, 2026`)
- **Current period end date** (e.g., `February 20, 2026`) - this is also the report date
- **Previous period start date** (e.g., `January 26, 2026`)
- **Previous period end date** (e.g., `February 6, 2026`)

## Step 2: Collect Current Test Metrics

Scan the codebase to collect accurate current metrics:

### 2a. Count Test Files
- Count all `test_*.py` files in `tests_e2e/tests/` (E2E test files)
- Count all `test_*.py` files in `tests_graphql/tests/` (GraphQL test files)

### 2b. Count Test Functions
For each test file, count all functions starting with `test_` (these are pytest test functions). Do this for both `tests_e2e/tests/` and `tests_graphql/tests/`.

### 2c. Count Ignored Tests
Search for `@pytest.mark.ignore` markers across all test files. Count how many test functions are marked as ignored in each directory (`tests_e2e` and `tests_graphql`). Active tests = Total test functions - Ignored tests.

### 2d. Identify Ignored Test Details
For each ignored test, record:
- File name
- Test function name
- Reason if available (from comments near the marker)

## Step 3: Collect Previous Period Metrics

Read the most recent existing report from `project-progress-report/` directory to get the previous period's metrics. The previous report's "Current State" section contains the baseline numbers for comparison.

## Step 4: Analyze Git History for Changes

Use `git log` to find commits in the current period date range. Identify:
- New test files added
- Modified test files
- New test functions added
- Tests re-enabled or newly ignored
- New components or page objects created
- Key feature areas covered

## Step 5: Calculate Derived Metrics

Calculate:
- **Change** (absolute): Current - Previous for each metric
- **% Change**: ((Current - Previous) / Previous) * 100
- **Active Rate**: (Active Tests / Total Test Functions) * 100
- **Growth velocity**: Tests per day = New tests / Days in period
- **Test distribution**: E2E % and GraphQL % of total

## Step 6: Read Historical Data

From existing reports, compile historical trend data (at least 3 data points) for the growth trend section:
- Date, Total Tests, Active Tests, Growth Rate

## Step 7: Generate the Report

Create the report file at: `project-progress-report/Sprint{SPRINT_ID}/test-coverage-report.md`

Use this exact structure and format (matching the established report template):

```markdown
# Test Coverage Report - 2 Week Comparison

**Report Date:** {REPORT_DATE}
**Comparison Periods:**
- **Previous Period:** {PREV_START} - {PREV_END} (2 weeks)
- **Current Period:** {CURR_START} - {CURR_END} (2 weeks)
**Sprint:** {SPRINT_ID}

---

## Executive Summary

This report compares test coverage between two consecutive 2-week periods, showing the evolution of the test suite.

**Key Achievements in Current Period ({CURR_START} - {CURR_END}):**
- **+{NEW_FUNCTIONS} new test functions** added ({GROWTH}% growth)
- **+{NEW_FILES} new test files** created
- **+{NEW_ACTIVE} active tests** enabled ({ACTIVE_GROWTH}% growth in active tests)
- **{IGNORED_CHANGE} ignored tests** ({IGNORED_DESCRIPTION})
- **Major focus:** {FOCUS_AREAS}

---

## Test Coverage Comparison Charts

### Period Comparison Overview

{ASCII chart comparing Period 1 vs Period 2 metrics}

### Test Functions Growth Trend

{ASCII line chart showing growth over 3+ data points}

### Active vs Ignored Tests

{ASCII bar chart showing active vs ignored per period}

---

## Detailed Statistics

### Current State ({REPORT_DATE})

#### tests_e2e (End-to-End Tests)

| Metric | Count |
|--------|-------|
| **Test Files** | {E2E_FILES} |
| **Total Test Functions** | {E2E_FUNCTIONS} |
| **Active Tests** | {E2E_ACTIVE} |
| **Ignored Tests** | {E2E_IGNORED} |
| **Active Rate** | {E2E_ACTIVE_RATE}% |

#### tests_graphql (GraphQL API Tests)

| Metric | Count |
|--------|-------|
| **Test Files** | {GQL_FILES} |
| **Total Test Functions** | {GQL_FUNCTIONS} |
| **Active Tests** | {GQL_ACTIVE} |
| **Ignored Tests** | {GQL_IGNORED} |
| **Active Rate** | {GQL_ACTIVE_RATE}% |

#### Grand Total

| Metric | Count |
|--------|-------|
| **Total Test Files** | {TOTAL_FILES} |
| **Total Test Functions** | {TOTAL_FUNCTIONS} |
| **Active Tests** | {TOTAL_ACTIVE} |
| **Ignored Tests** | {TOTAL_IGNORED} |
| **Active Rate** | {TOTAL_ACTIVE_RATE}% |

---

### Two-Week Period Comparison

{Comparison tables for E2E, GraphQL, and Grand Total with columns:
Metric | Period 1 | Period 2 | Change | % Change}

---

## Test Coverage Distribution

### By Test Type (Current State)

{ASCII bar chart showing E2E vs GraphQL distribution}

### Growth by Test Type

{ASCII bars showing growth per type}

---

## What Changed in Period 2

### New Test Files
{Table of new test files with test counts and status}

### New Components/Pages Created
{List of new component or page object files if any}

### Tests Re-enabled or Newly Ignored
{Details of marker changes}

---

## Major Changes & Improvements

{Numbered sections for key changes, referencing git commits where possible:
1. Feature name (N tests) - with commit hash and description
2. Reliability improvements
3. Infrastructure changes
4. Other notable changes}

---

## Test Files Modified

### E2E Tests Modified
{Numbered list of modified E2E test files with description}

### GraphQL Tests Modified
{Numbered list of modified GraphQL test files with description}

---

## Ignored Tests Analysis

### Current Ignored Tests ({TOTAL_IGNORED} total)

#### tests_e2e ({E2E_IGNORED} ignored)
| File | Test | Reason |
|------|------|--------|
{rows}

#### tests_graphql ({GQL_IGNORED} ignored)
| File | Test | Reason |
|------|------|--------|
{rows}

### Improvement/Change Summary
{Comparison of ignored test counts between periods}

---

## Period-over-Period Growth Analysis

### Historical Trend

| Date | Total Tests | Active Tests | Growth Rate |
|------|-------------|--------------|-------------|
{historical data rows - at least 3 data points}

### Growth Velocity

{ASCII chart showing tests/day per period}

---

## Quality Metrics

### Test Reliability (Active Test Rate)

{ASCII progress bars comparing previous vs current active rate against 95% target}

### Code Coverage Impact

{Lines of code statistics from git}

### Test Distribution Balance

{ASCII bars showing E2E vs GraphQL % with balance assessment}

---

## Key Achievements Summary

| Achievement | Impact |
|-------------|--------|
{key achievement rows}

---

## Sprint Comparison Summary

{Comparison of current sprint vs previous sprint(s)}

### Combined Impact
{Cumulative statistics from earliest tracked period to now}

---

## Recommendations for Next Period

{4 numbered recommendations based on the data:
1. Test stabilization recommendations
2. Growth recommendations
3. Infrastructure recommendations
4. Other improvement areas}

---

*Report generated on {REPORT_DATE}*
*Data sources: Git history analysis, test file counting, pytest marker analysis*
```

## Step 8: Generate HTML Presentation

Create an interactive HTML presentation at: `project-progress-report/Sprint{SPRINT_ID}/test-coverage-presentation.html`

Use Chart.js (via CDN: https://cdn.jsdelivr.net/npm/chart.js@4.4.7) to create an interactive slide-based presentation with:
- Dark theme with modern styling
- Slide navigation (Previous/Next buttons + keyboard arrows)
- Multiple chart types: bar, line, doughnut, horizontal bar
- Card-based layouts for summaries
- All the same data from the markdown report visualized

Include these slides:
1. **Title Slide** - Sprint ID, dates, key headline metric
2. **Executive Summary** - 4-6 metric cards with icons
3. **Test Growth Trend** - Line chart with historical data
4. **Period Comparison** - Grouped bar chart
5. **Active vs Ignored** - Stacked bar chart
6. **Test Distribution** - Doughnut chart (E2E vs GraphQL)
7. **E2E Detailed** - Bar chart for E2E metrics comparison
8. **GraphQL Detailed** - Bar chart for GraphQL metrics comparison
9. **What Changed** - Card layout with key changes
10. **Key Achievements** - Card layout with metrics
11. **Quality Metrics** - Progress bars and gauges
12. **Recommendations** - Styled list

## Step 9: Generate Chart Script

Create a Python script at: `project-progress-report/Sprint{SPRINT_ID}/generate_charts.py`

This script uses matplotlib to generate PNG chart images saved to `project-progress-report/Sprint{SPRINT_ID}/charts/`:
1. `1_test_growth_trend.png` - Line chart
2. `2_period_comparison_overview.png` - Horizontal bar chart
3. `3_active_vs_ignored.png` - Stacked bar chart
4. `4_test_distribution_donut.png` - Donut chart
5. `5_e2e_tests_comparison.png` - Grouped bar chart
6. `6_graphql_tests_comparison.png` - Grouped bar chart
7. `7_key_achievements.png` - Card-based summary

Use a professional color scheme, 180 DPI, clear labels and annotations.

## Step 10: Summary

After generating all files, provide a summary to the user:
- Report location and file paths
- Key metrics highlights (total tests, growth, active rate)
- Any notable findings or concerns
- Reminder to run `python generate_charts.py` from the sprint folder to generate PNG charts