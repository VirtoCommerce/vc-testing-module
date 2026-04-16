---
name: plan-implementation
description: "Plan file-by-file implementation for test automation tasks — which files to create/modify, in what order, which patterns and existing code to reuse"
argument-hint: "<task-description>"
---

## Implementation Planning

Given a task or test strategy, produce a step-by-step implementation plan with exact file paths, patterns to follow, and dependencies.

## Process

### Step 1: Identify All Artifacts Needed

For each test case in the strategy, determine what needs to exist:

| Artifact | Location | Pattern |
|----------|----------|---------|
| GraphQL fragment | `gql/fragments/<entity>.graphql` | Fragment definition |
| Pydantic type | `gql/types/<entity>.py` | `GqlModel` subclass |
| Pydantic input | `gql/types/<entity>_input.py` | `GqlModel` with `serialization_alias` |
| GraphQL operations | `gql/operations/<entity>_operations.py` | `BaseOperations` subclass |
| REST operations | `restapi/operations/<entity>_operations.py` | `RestBaseOperations` subclass |
| REST template | `restapi/constants.py` | Immutable dict constant |
| Page object | `page_objects/pages/<page>.py` | `MainLayout` subclass |
| Component | `page_objects/components/<component>.py` | `Component` subclass |
| Factory fixture | `tests/restapi/<module>/conftest.py` | Generator yielding callable |
| Test file | `tests/<type>/test_<feature>.py` | Markers + Allure + assertions |
| Shared constants | `tests/constants.py` | Pydantic model instances |

### Step 2: Check What Already Exists

Before adding new files, search the codebase:
- Existing operations classes that already have the methods you need
- Existing Pydantic types that cover the response shape
- Existing page objects and components
- Existing factory fixtures in conftest files
- Existing fragment files

### Step 3: Determine Implementation Order

Dependencies flow downward — implement in this order:

```
1. gql/fragments/*.graphql          (fragments first — operations depend on them)
2. gql/types/*.py                   (types next — operations return them)
3. gql/types/__init__.py            (export new types)
4. gql/operations/*_operations.py   (operations use fragments + types)
5. gql/operations/__init__.py       (export new operations)
6. restapi/constants.py             (templates — if REST API tests needed)
7. restapi/operations/*.py          (REST operations — if needed)
8. page_objects/components/*.py     (components — if E2E tests needed)
9. page_objects/components/__init__.py
10. page_objects/pages/*.py          (pages use components)
11. page_objects/pages/__init__.py
12. tests/constants.py               (shared test constants — if needed)
13. tests/restapi/<module>/conftest.py (factory fixtures — if REST tests)
14. tests/graphql/test_*.py          (GraphQL tests)
15. tests/e2e/test_*.py              (E2E tests)
16. tests/restapi/<module>/test_*.py (REST API tests)
```

### Step 4: Reference Existing Patterns

For each file, specify which existing file to use as a pattern reference:

| New File | Pattern Reference |
|----------|-------------------|
| GraphQL operations | `gql/operations/cart_operations.py` |
| Pydantic types | `gql/types/cart.py` |
| Pydantic inputs | `gql/types/cart_item_input.py` |
| Page object | `page_objects/pages/cart.py` |
| Component | `page_objects/components/product_card.py` |
| REST operations | `restapi/operations/product_operations.py` |
| Factory fixture | `tests/restapi/catalog/conftest.py` |
| GraphQL test (simple) | `tests/graphql/test_cart.py` |
| GraphQL test (manual) | `tests/graphql/test_cart_add_bulk_items.py` |
| E2E test | `tests/e2e/test_cart_clear.py` |
| REST API test | `tests/restapi/catalog/test_product.py` |

## Output Format

```markdown
# Implementation Plan: <Task Name>

## Summary
<1-2 sentences: what will be built and why>

## Prerequisites
- [ ] <anything that must exist or be verified before starting>

## Files to Create/Modify

### Phase 1: Infrastructure (types, operations, pages)

#### 1. `<file_path>` (CREATE/MODIFY)
- **Pattern reference:** `<existing_file_to_follow>`
- **What:** <brief description>
- **Details:**
  - <specific class/method/field to add>
  - <specific import to add>
- **Skill to use:** `/create-graphql-layer` | `/create-ui-layer` | none

#### 2. `<file_path>` (CREATE/MODIFY)
...

### Phase 2: Test Files

#### N. `<file_path>` (CREATE)
- **Pattern reference:** `<existing_test_to_follow>`
- **Test functions:**
  - `test_<name>` — <what it verifies>
  - `test_<name>` — <what it verifies>
- **Markers:** `@pytest.mark.<type>`, `@pytest.mark.with_user(...)`, etc.
- **Fixtures:** `graphql_client`, `ctx`, `make_product`, etc.
- **Allure:** `@allure.feature("...")`, `@allure.title("...")`
- **Skill to use:** `/write-graphql-test` | `/write-e2e-test` | `/write-rest-api-test`

### Phase 3: Exports and Registration

#### M. `<__init__.py path>` (MODIFY)
- **What:** Add exports for new classes

## Verification Steps
1. <how to run the tests>
2. <what to check in the output>
3. <any manual verification needed>

## Risks and Notes
- <potential issues, edge cases, or things to watch out for>
```

## Planning Rules

1. **Never propose a new file when an existing one can be extended** — check first
2. **Always specify the pattern reference file** — the implementer should have a concrete example to follow
3. **Always specify which skill to invoke** for each file creation step
4. **Include `__init__.py` exports** — they're easy to forget
5. **Plan verification** — how will we know the implementation is correct?
6. **Order matters** — dependencies must be built before dependents
7. **One test file per feature area** — don't scatter related tests across files
8. **Include cleanup** — every test that creates data must have a cleanup strategy in the plan
