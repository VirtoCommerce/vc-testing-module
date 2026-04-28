---
name: review-pr
description: "Review a pull request — analyze diffs, commit quality, test coverage, pattern compliance across all changed files, and provide structured feedback"
argument-hint: "<pr-number-or-url>"
---

## Pull Request Review

When reviewing a PR, analyze the full scope of changes and provide structured, actionable feedback.

## Review Process

### Step 1: Gather PR Context

```bash
# Get PR details
gh pr view <number> --json title,body,baseRefName,headRefName,files,additions,deletions,commits

# Get changed files
gh pr diff <number>

# Get commit messages
gh pr view <number> --json commits --jq '.commits[].messageHeadline'

# Check CI status
gh pr checks <number>
```

### Step 2: Understand the Scope

- What is the PR trying to accomplish? (read title + description)
- How many files changed? What types? (tests, operations, pages, fixtures, config)
- Is this a new feature, bug fix, refactor, or infrastructure change?
- Which test types are affected? (GraphQL, E2E, REST API)

### Step 3: Review Each Changed File

For each file in the diff, apply the relevant checklist:

#### Test Files (`tests/**/*.py`)
Apply the full test code review checklist:
- Markers, Allure decorators, assertions, fixtures, cleanup
- Type-specific patterns (GraphQL/E2E/REST API)
- Code quality: type hints, no hardcoded values, proper imports

#### Operations Classes (`gql/operations/*.py`, `restapi/operations/*.py`)
- Follows `BaseOperations` / `RestBaseOperations` pattern
- Methods have proper return types (Pydantic models for GraphQL, dicts for REST)
- Auto-fragment injection via `_build_query()`
- Proper error handling

#### Page Objects and Components (`page_objects/**/*.py`)
- Extends correct base class (`MainLayout`, `Component`)
- Properties for locators, keyword arg constructors
- No test logic or assertions

#### Pydantic Types (`gql/types/*.py`)
- Inherits `GqlModel`
- Proper aliasing for inputs
- Exported in `__init__.py`

#### Fixture Files (`**/conftest.py`)
- Proper scoping (session vs. function)
- Factory fixtures have cleanup
- No side effects in session fixtures

#### Fragment Files (`gql/fragments/*.graphql`)
- Fragment name matches convention
- Spreads reference existing fragments
- Fields match the Pydantic type

### Step 4: Cross-File Analysis

- **Consistency:** Do all new test files follow the same patterns?
- **Completeness:** Are `__init__.py` exports updated?
- **Dependencies:** Do new operations reference types that exist? Do new tests import everything they need?
- **Coverage:** Does the PR add tests for the feature it introduces?
- **Cleanup:** Do new tests clean up after themselves?

### Step 5: Review Commit Quality

- **Commit messages:** Are they descriptive? Do they explain why, not just what?
- **Commit scope:** Is each commit focused on one change?
- **Commit order:** Do commits tell a logical story?

### Step 6: Check CI Status

- Are all checks passing?
- If checks are failing, is it related to the PR changes or a pre-existing issue?

## Output Format

```markdown
## PR Review: #<number> — <title>

### Summary
<2-3 sentence overview: what the PR does, overall quality assessment>

### Scope
- **Files changed:** <count>
- **Test types affected:** GraphQL / E2E / REST API
- **Categories:** <new tests | operations | pages | fixtures | infrastructure>

### Critical Issues
- **[file:line]** <issue> — **Fix:** <specific fix>

### Warnings
- **[file:line]** <issue> — **Suggestion:** <improvement>

### Suggestions
- <improvement idea>

### Coverage Assessment
- **New code tested:** Yes / No / Partially
- **Missing coverage:** <list of untested scenarios>

### Commit Quality
- <assessment of commit messages and scope>

### CI Status
- <passing / failing — details if failing>

### Verdict
**APPROVE** | **REQUEST_CHANGES** | **NEEDS_DISCUSSION**

<brief rationale for verdict>
```

## Common PR Patterns to Watch For

### New Feature PR
- Expect: new tests covering happy path + error cases
- Expect: new operations/types if new API surface
- Expect: new page objects if new UI pages
- Watch for: missing cleanup, incomplete coverage

### Bug Fix PR
- Expect: a test that reproduces the bug (would have failed before the fix)
- Watch for: test that only tests the fix, not the root cause

### Refactoring PR
- Expect: no behavior change — existing tests should still pass
- Expect: tests updated to match new patterns
- Watch for: removed tests without replacement

### Infrastructure PR
- Expect: fixture changes, conftest updates, base class changes
- Watch for: breaking changes to existing fixtures
- Watch for: missing updates to tests that use changed fixtures
