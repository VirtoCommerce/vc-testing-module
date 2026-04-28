---
name: review-test-code
description: "Review test files for pattern compliance, code quality, correctness, coverage gaps, and best practices — produces actionable feedback"
argument-hint: "<file-path-or-pattern>"
---

## Test Code Review

When reviewing test code, systematically check every item below and report only actual issues found.

## Review Process

### Step 1: Read the File(s)

Read the target test file(s) completely. Also read related files:
- The conftest.py that provides fixtures for this test
- The operations class(es) used by the test
- The page objects/components used by the test (for E2E)

### Step 2: Check Structure (all test types)

For every test function, verify:

- [ ] **Type marker present:** `@pytest.mark.graphql` / `@pytest.mark.e2e` / `@pytest.mark.restapi`
- [ ] **Allure feature:** `@allure.feature("<Domain> (<TestType>)")` with correct naming
- [ ] **Allure title:** `@allure.title("<Action description>")` — descriptive, not generic
- [ ] **Return annotation:** `-> None` on test function
- [ ] **Constants at module level:** `_PRODUCT_ID = "..."` (not inline strings)
- [ ] **Single responsibility:** each test verifies one behavior
- [ ] **Test name is descriptive:** `test_<feature>_<action>` pattern

### Step 3: Check Type-Specific Patterns

#### For GraphQL Tests

- [ ] Uses `graphql_client` fixture (not manual `GraphQLClient()`)
- [ ] Uses `ctx` fixture for store/user/currency/culture (not hardcoded)
- [ ] Marker-driven setup preferred: `@pytest.mark.with_cart`, `@pytest.mark.with_user`
- [ ] Manual setup has try-finally cleanup
- [ ] Asserts on Pydantic model attributes: `cart.id`, `cart.is_anonymous` (not `cart["id"]`)
- [ ] Operations created as: `CartOperations(client=graphql_client)` (keyword arg)
- [ ] Cleanup variable initialized before try: `cart: Cart | None = None`

#### For E2E Tests

- [ ] Page objects use keyword args: `CartPage(global_settings=global_settings, page=page)`
- [ ] Navigation via `page_object.navigate()` (not `page.goto()`)
- [ ] All UI assertions use `expect()` (not bare `assert`)
- [ ] Locators use `data-test-id` (not CSS class or XPath)
- [ ] No `time.sleep()` anywhere
- [ ] Components created with `root=` keyword: `Component(root=locator)`
- [ ] Auth via `@pytest.mark.with_user` (not manual BrowserStorage)

#### For REST API Tests

- [ ] Uses factory fixtures: `make_product`, `make_catalog` (not manual create/delete)
- [ ] Test body uses `with allure.step()` blocks
- [ ] `@allure.feature("<Module> / <Entity> (REST API)")` naming
- [ ] Assertions on raw dicts (not Pydantic models)
- [ ] Error handling: `except HTTPError as e:` with status code check
- [ ] `@pytest.mark.serial` for tests that mutate global state

### Step 4: Check Code Quality

- [ ] **Type hints** on all function parameters and return values
- [ ] **No hardcoded credentials** — uses `global_settings` or `ctx`
- [ ] **No hardcoded URLs** — uses `global_settings.frontend_base_url` etc.
- [ ] **Cleanup before assertions** — resources cleaned up in `finally`, not after `assert`
- [ ] **No mutable global state** — no module-level variables modified by tests
- [ ] **Import order** — stdlib, third-party, local (standard Python convention)
- [ ] **`SecretStr` access** — uses `.get_secret_value()` for passwords

### Step 5: Check Coverage

- [ ] **Happy path covered** — the primary success scenario
- [ ] **Error scenarios** — invalid input, unauthorized access, not found
- [ ] **Edge cases** — empty collections, boundary values, special characters
- [ ] **User roles** — anonymous vs. registered vs. admin (where applicable)
- [ ] **Cleanup verified** — test doesn't leak resources on failure

## Severity Levels

### Critical (must fix before merge)
- Missing cleanup / resource leak
- Hardcoded credentials or secrets
- Missing required marker
- Dict access on Pydantic model in GraphQL test
- Bare `assert` for UI state in E2E test
- `time.sleep()` in any code

### Warning (should fix)
- Missing Allure decorators
- Raw `page.goto()` instead of `navigate()`
- CSS/XPath selectors instead of `data-test-id`
- Missing type hints
- Assertions after cleanup (should be before, cleanup in finally)
- Manual setup when markers would work

### Suggestion (nice to have)
- Test could be split (does too many things)
- Missing `allure.step()` for logical grouping
- Duplicate setup across tests (extract to fixture)
- Missing edge case coverage

## Output Format

```markdown
## Review: <file_path>

### Summary
<1-2 sentence assessment: what's good, what needs work>

### Critical Issues
- **[line N]** <issue description> — **Fix:** <specific fix>

### Warnings
- **[line N]** <issue description> — **Suggestion:** <specific improvement>

### Suggestions
- <improvement idea with rationale>

### Coverage Gaps
- <missing test scenario that should exist>

### Verdict
APPROVE | REQUEST_CHANGES | NEEDS_DISCUSSION
```

When reviewing multiple files, produce one section per file, then a final overall summary.
