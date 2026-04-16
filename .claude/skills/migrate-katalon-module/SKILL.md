---
name: migrate-katalon-module
description: "Migrate a Katalon REST API test module from vc-quality-gate-katalon into the refactored Pytest project — end-to-end flow from inventory to CI-verified PR"
argument-hint: "<KatalonModule> [jira-ticket]"
user-invocable: true
---

## Katalon → Pytest Migration Flow

Migrate one Katalon module (e.g., `ModuleCatalog`, `Contacts`, `ModulePricing`) from `VirtoCommerce/vc-quality-gate-katalon` into `_refactored/tests/restapi/<module>/`.

**CRITICAL LESSON:** Always read the Katalon Object Repository `.rs` files FIRST to get the real endpoint URLs and HTTP methods. Never guess endpoints from test names — they are often wrong (e.g., `/apiaccounts` vs `/users/apikeys`, POST vs PUT for role creation).

---

## Step 1: INVENTORY — List all Katalon scripts

```bash
# List top-level folders in the module
gh api "repos/VirtoCommerce/vc-quality-gate-katalon/contents/Scripts/API%20Coverage/<KatalonModule>" --jq '.[].name' | sort

# For each folder that contains sub-scripts (not a single .groovy):
gh api "repos/VirtoCommerce/vc-quality-gate-katalon/contents/Scripts/API%20Coverage/<KatalonModule>/<Folder>" --jq '.[].name'
```

**Output:** Complete list of all scripts. Mark each as:
- `REAL` — actual test to migrate
- `DRAFT` — skip (folder name starts with DRAFT or contains draft)
- `DEPRECATED` — skip (folder name contains deprecated)
- `TEMPLATE` — skip (`_suiteTemplate`, `z_snippet_*`)
- `UTILITY` — skip (shared helper called by other tests, not standalone)

Count total REAL scripts. This is the target.

---

## Step 2: ENDPOINTS — Read Object Repository `.rs` files

**DO THIS BEFORE WRITING ANY CODE.**

```bash
# Find the Object Repository folder for this module
gh api "repos/VirtoCommerce/vc-quality-gate-katalon/contents/Object%20Repository/API/backWebServices" --jq '.[].name' | sort

# List all .rs files
gh api "repos/VirtoCommerce/vc-quality-gate-katalon/contents/Object%20Repository/API/backWebServices/<VirtoCommerce.Module>" --jq '.[].name' | sort

# For each .rs file, extract the real endpoint:
gh api "repos/VirtoCommerce/vc-quality-gate-katalon/contents/Object%20Repository/API/backWebServices/<VirtoCommerce.Module>/<Name>.rs" --jq '.content' | base64 -d | grep -E 'restRequestMethod|restUrl'
```

**Output:** Endpoint map — for every API action, the verified:
- HTTP method (GET/POST/PUT/DELETE)
- URL path (with parameter placeholders)
- Whether body is JSON or form-encoded

**Common gotchas found in previous migrations:**
- Roles CREATE uses PUT, not POST
- Password reset uses `{userName}` in path, not `{userId}`
- API key POST returns empty body (204) — need diff-before-after pattern
- Dynamic properties: objectType goes in body, not URL path
- Asset upload from URL: it's a GET with query params, not POST with JSON
- Asset delete: DELETE with `?urls=` query params, not POST to `/delete`
- OAuth: `/oauthapps`, not `/security/oauth/clients`
- Notifications: search is POST, not GET; `markAllAsRead` is camelCase
- Background jobs: `/jobs/1` (specific job), not `/jobs`
- Restart: `/modules/restart`, not `/restart`

---

## Step 3: OPERATIONS CLASS

Create `_refactored/restapi/operations/<module>_operations.py`:

```python
from typing import Any
from restapi.operations.base import RestBaseOperations

class <Entity>Operations(RestBaseOperations):
    PATH = "/api/..."  # FROM .rs FILE, NOT GUESSED

    def create(self, *, <required_fields>, **overrides: Any) -> dict:
        payload = {<template>, **overrides}
        return self._client.<method>(self._url(self.PATH), json=payload)
```

**Rules:**
- PATH constant must match the `.rs` file exactly
- HTTP method must match `restRequestMethod` from `.rs` file
- If POST/PUT returns empty body, do a follow-up GET to return the created object
- Add to `restapi/operations/__init__.py`

---

## Step 4: FIXTURES

Create `_refactored/tests/restapi/<module>/conftest.py`:

```python
@pytest.fixture
def <entity>_ops(rest_client: RestClient, backend_base_url: str) -> <Entity>Operations:
    return <Entity>Operations(rest_client, backend_base_url)

@pytest.fixture
def make_<entity>(<entity>_ops) -> Generator[Callable[..., dict], None, None]:
    created_ids: list[str] = []
    def _make(**overrides) -> dict:
        name = overrides.pop("name", f"QA<Entity>_{uuid.uuid4().hex[:8]}")
        entity = <entity>_ops.create(name=name, **overrides)
        created_ids.append(entity["id"])
        return entity
    yield _make
    for eid in reversed(created_ids):
        try:
            <entity>_ops.delete(eid)
        except Exception:
            pass
```

**Rules:**
- Factory fixtures are function-scoped (default)
- Always yield + cleanup
- If POST returns empty body, use diff-before-after pattern:
  ```python
  before_ids = {e["id"] for e in ops.get_all() or []}
  ops.create(...)
  after = ops.get_all() or []
  new = [e for e in after if e["id"] not in before_ids]
  ```

---

## Step 5: TESTS

Create `_refactored/tests/restapi/<module>/test_<feature>.py`:

**Every test MUST have:**
- `@pytest.mark.restapi`
- `@allure.feature("<Module> / <Feature> (REST API)")`
- `@allure.title("<What this test does>")`
- `with allure.step("<HTTP method> <endpoint>"):` for each HTTP call
- `with allure.step("Verify ..."):` for assertions

**Serial tests:** Add `@pytest.mark.serial` for tests that mutate global state (settings, dynamic properties, module reload, restart).

**Parametrize:** When Katalon has N scripts that repeat the same pattern with different parameters (e.g., DynamicProperties across 16 object types), use `@pytest.mark.parametrize` instead of N separate functions.

**Constants:** If the module needs payload templates, add to `_refactored/restapi/constants.py`.

---

## Step 6: LOCAL VERIFICATION

```bash
cd _refactored
ADMIN_PASSWORD=<password> .venv/Scripts/pytest.exe tests/restapi/<module>/ -v -m "restapi" --tb=short
```

**Common failures and fixes:**
- `404 Not Found` → wrong endpoint path, re-check `.rs` file
- `405 Method Not Allowed` → wrong HTTP method, re-check `.rs` file
- `TypeError: NoneType is not a mapping` → endpoint returns empty body, use diff pattern
- `401 Unauthorized` → multipart upload needs explicit Authorization header (not Content-Type from admin_auth.headers)
- `succeeded: false` → check if endpoint uses userName vs userId in path

---

## Step 7: 1-TO-1 MAPPING CHECK

Build a complete mapping table:

```
Katalon script → Pytest test function → Status
```

Print it out. Verify:
- Every REAL Katalon script maps to exactly one test function or parametrize case
- 0 MISSING entries
- SKIP count matches DRAFT + DEPRECATED + TEMPLATE + UTILITY

---

## Step 8: CI + PR

1. Commit all files
2. Push branch
3. Create PR with mapping table in description
4. Dispatch `refactored-tests.yml` on the branch
5. Verify REST API steps pass (parallel-safe + serial + restart)
6. Merge

**CI test split:**
- Parallel-safe: `-m "restapi and not ignore and not serial"`
- Serial: `-m "restapi and serial and not ignore" --deselect test_restart_platform`
- Restart (last): `test_misc.py::test_restart_platform`

---

## Checklist

- [ ] All Katalon scripts inventoried
- [ ] All endpoints verified from `.rs` files (NOT guessed)
- [ ] Operations class created with correct paths + methods
- [ ] Factory fixtures with cleanup
- [ ] All tests have restapi marker + Allure decorators + allure.step
- [ ] Serial marker on global-state-mutating tests
- [ ] Parametrize used where Katalon repeats same pattern
- [ ] Local run: all passing
- [ ] 1-to-1 mapping: 0 missing
- [ ] CI dispatch: green
