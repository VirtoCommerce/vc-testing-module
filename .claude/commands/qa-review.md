# QA Review

**Stage 3 of 3** in the QA workflow: Plan → Implement → Review

You are orchestrating the review stage. Spawn the `qa-reviewer` agent to review the code produced in the previous `/qa-implement` stage, or review any specified files/PR.

## Input

One of:
- No arguments — review files changed in the current branch (from `/qa-implement`)
- A file path or glob pattern — review specific files
- A PR number — review a pull request

`$ARGUMENTS` specifies the target. If empty, auto-detect from git status.

## Steps

### 1. Determine Review Scope

If `$ARGUMENTS` is a PR number or URL:
- Spawn the `qa-reviewer` agent with the `/review-pr` skill

If `$ARGUMENTS` is a file path or pattern:
- Spawn the `qa-reviewer` agent with the `/review-test-code` skill

If no arguments:
- Run `git diff --name-only HEAD~1` (or detect uncommitted changes) to find changed files
- Filter for test-related files (`tests/`, `gql/`, `page_objects/`, `restapi/`)
- Spawn the `qa-reviewer` agent with `/review-test-code` on each changed file

### 2. Review

The agent performs a systematic review using its checklists:
- Pattern compliance (markers, Allure, fixtures, assertions)
- Code quality (type hints, no hardcoded values, cleanup)
- Coverage gaps (missing scenarios)
- Cross-file consistency

### 3. Output

Present the review results:
- Per-file review with Critical / Warning / Suggestion items
- Overall verdict: APPROVE / REQUEST_CHANGES / NEEDS_DISCUSSION
- Coverage gap summary

If issues are found, end with:
```
Review complete. Fix the issues above, then run /qa-review again.
```

If approved, end with:
```
Review complete. Code looks good — ready to commit.
```
