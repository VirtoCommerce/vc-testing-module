# Migrate Katalon Module

Migrate Katalon REST API test module `$ARGUMENTS` from `VirtoCommerce/vc-quality-gate-katalon` into `_refactored/tests/restapi/`.

Arguments format: `<KatalonModule> [jira-ticket]`
Example: `/migrate-katalon-module Contacts VCST-4941`

## CRITICAL RULE

**ALWAYS read Katalon Object Repository `.rs` files FIRST to get real endpoint URLs and HTTP methods. NEVER guess endpoints from test names.**

## Execute these steps sequentially

### Step 1: BRANCH
If jira-ticket provided: `git checkout dev && git pull && git checkout -b <jira-ticket>-restapi-<module>-module`

### Step 2: INVENTORY
List ALL Katalon scripts in the module:
```bash
gh api "repos/VirtoCommerce/vc-quality-gate-katalon/contents/Scripts/API%20Coverage/<KatalonModule>" --jq '.[].name'
```
For each folder, list sub-scripts. Classify: REAL / DRAFT / DEPRECATED / TEMPLATE / UTILITY. Count REAL scripts.

### Step 3: ENDPOINTS (from Object Repository)
Read EVERY `.rs` file before writing code:
```bash
gh api "repos/VirtoCommerce/vc-quality-gate-katalon/contents/Object%20Repository/API/backWebServices/<VirtoCommerce.Module>/<Name>.rs" --jq '.content' | base64 -d | grep -E 'restRequestMethod|restUrl'
```
Build endpoint map: `Name | HTTP Method | URL Path`

### Step 4: OPERATIONS CLASS
Create `_refactored/restapi/operations/<module>_operations.py` using VERIFIED endpoints from Step 3. Add to `__init__.py`.

### Step 5: FIXTURES
Create `_refactored/tests/restapi/<module>/conftest.py` with operations fixtures + factory fixtures with auto-cleanup.

### Step 6: TESTS
Create test files with: `@pytest.mark.restapi` + `@allure.feature` + `@allure.title` + `allure.step`. Use `@pytest.mark.serial` for global state mutators. Use `@pytest.mark.parametrize` where Katalon repeats same pattern.

### Step 7: LOCAL VERIFY
```bash
cd _refactored && ADMIN_PASSWORD=<pwd> .venv/Scripts/pytest.exe tests/restapi/<module>/ -v -m "restapi" --tb=short
```
Fix all failures.

### Step 8: ENDPOINT VERIFICATION
Programmatically cross-reference ALL our operations endpoints against Katalon `.rs` files. Normalize `${var}` and `{var}` to `{x}`, strip query params. Match by (method, normalized_path). **Result must be 0 MISSING.**

### Step 9: 1-TO-1 MAPPING
Print table: every REAL Katalon script → our test function. **0 MISSING required.**

### Step 10: COMMIT + PUSH
```bash
git add _refactored/ && git commit && git push -u origin <branch>
```

### Step 11: PR
```bash
gh pr create --title "feat: <JIRA> — REST API <Module> migration (N test cases)" --base dev
```

### Step 12: CI DISPATCH
```bash
gh workflow run refactored-tests.yml --ref <branch> -f frontendZipUrl="https://vc3prerelease.blob.core.windows.net/packages/vc-theme-b2b-vue-2.45.0-pr-2234-e507-e5076378.zip"
```
Wait for green. Fix if needed.

### Step 13: MERGE
```bash
gh pr merge <PR> --squash
```
