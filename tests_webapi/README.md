# tests_webapi — REST API test suite

Pytest tests for the VirtoCommerce backend admin REST API. Migrated from the legacy
Katalon `Test Cases/API Coverage/` suite (569 original tests across 17 modules).

## Layout

```
tests_webapi/
├── constants.py              # read-only test-data templates (see "Shared data")
├── platform/                 # ModulePlatform — users, settings, api keys, etc.
├── contacts/                 # Members, organizations, employees, vendors
├── catalog/                  # Catalogs, categories, products, channels, tags
├── pricing/                  # Prices, pricelists, assignments
├── marketing/                # DynamicContent, promotions
├── assets/                   # Asset upload / management
├── content/                  # Content pages, folders
├── store/                    # Store configuration
├── search/                   # Search APIs
├── catalog_publishing/       # Publishing workflows
├── catalog_personalisation/  # Personalization rules
├── core/, health_check/, orders/, backend/, frontend/, utility/
```

Each `<module>/` holds `test_<module>_<feature>.py` files plus an optional
`conftest.py` for per-module factory fixtures.

Reusable request builders live in [webapi_operations/](../webapi_operations/),
mirroring [graphql_operations/](../graphql_operations/). One sub-package per module.

## Writing a new test

Standard template:

```python
# tests_webapi/<module>/test_<module>_<feature>.py
import uuid

import allure
import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.webapi_client import WebAPISession
from webapi_operations.<module>.<thing>_operations import ThingOperations


@pytest.mark.webapi
@allure.feature("<Module> / <Thing> (WebAPI)")
@allure.title("<What this verifies>")
def test_<operation>(
    webapi_client: WebAPISession, auth: Auth, config: Config
):
    auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])
    things = ThingOperations(webapi_client)

    with allure.step("Create"):
        created = things.create(name=f"Thing_{uuid.uuid4().hex[:8]}")

    with allure.step("Verify"):
        assert created["id"]

    with allure.step("Cleanup"):
        things.delete(created["id"])
```

Every test MUST:
- carry `@pytest.mark.webapi`
- call `auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])` when
  the endpoint requires auth
- clean up any entities it creates (via operations-class `.delete(...)` or a
  factory fixture's yield-cleanup)
- use `allure.feature` + `allure.title` + `allure.step` for Allure reporting
- follow the parallel-safety rules below

## Parallel execution (pytest-xdist)

Tests are written to run in parallel via `pytest-xdist`. Each xdist worker is a
separate Python process with its own `Auth`, `WebAPISession`, and in-memory
dataset — no shared state inside Python. The backend is shared, so all tests
must follow these rules or they will flake under load.

### Four hard rules

1. **Every created entity name must be unique.** Use
   `f"<prefix>_{uuid.uuid4().hex[:8]}"` for catalog names, usernames, emails,
   etc. Never reuse fixed names from Katalon profiles (`"QWEcatalog"`,
   `"UserQAK"`, etc.).
2. **Never mutate `dataset[...][index]` entities.** The seeded dataset is
   read-only shared reference data. If a test needs to update or delete
   something, it must *create* that entity itself first, then act on it.
3. **Tests that mutate global platform state must be marked
   `@pytest.mark.serial`.** This includes Settings* (`SettingsUpdateBlacklist`,
   `SettingsUpdateBoolean`), ModulesManagement, RestartPlatform, DynamicProperties
   at the global scope, feature-flag toggles, anything that restarts services,
   anything that rewrites a singleton config resource. When in doubt, mark it
   serial.
4. **Tests must be order-independent.** `allure.step` ordering inside one test
   is fine (one worker). Cross-test ordering is not.

### Commands

```bash
# All webapi tests, serial (local dev default)
pytest -m "webapi and not ignore" tests_webapi/ -v

# Parallel-safe tests, parallel (CI pattern)
pytest -m "webapi and not ignore and not serial" -n auto --dist loadfile tests_webapi/

# Serial-only tests (global state mutators)
pytest -m "webapi and serial and not ignore" tests_webapi/

# Per-module
pytest tests_webapi/platform/ -v

# Single file / single test
pytest tests_webapi/catalog/test_catalog_catalogs.py::test_catalog_create -v
```

`--dist loadfile` distributes at file granularity so tests in one file run on the
same worker — good default when a file's tests share a setup pattern or may touch
a common entity.

## Shared test data

Katalon `GlobalVariable` entries map to three Pytest-native replacements:

| Katalon global | Category | Pytest replacement |
|---|---|---|
| `urlBack`, `api_key`, `userName`, `storeId` | Environment config | `.env` → `Config` fixture |
| `contactName`, `organizationZip`, `memberType[]`, address fields | Read-only templates | `tests_webapi/constants.py` |
| `catalogId`, `productId`, `memberId[]` (produced by one test, read by another) | Test-to-test leakage | **Banned.** Use a factory fixture and clean up. |

### Read-only templates (`constants.py`)

Stable payload shells. Spread them; override only the identifying field:

```python
from tests_webapi.constants import ORGANIZATION_TEMPLATE

payload = {**ORGANIZATION_TEMPLATE, "name": f"OrgQA_{uuid.uuid4().hex[:8]}"}
```

Rules:
- Everything is read-only — no `.append()`, no in-place mutation of nested dicts.
- No environment values here (URLs, credentials).
- No test state here (server-assigned IDs, created-entity names).

### Factory fixtures (`<module>/conftest.py`)

When a test needs an entity and needs it cleaned up, a factory fixture beats
open-coding create/delete in every test:

```python
# tests_webapi/<module>/conftest.py
import uuid
import pytest
from tests_webapi.constants import ORGANIZATION_TEMPLATE


@pytest.fixture
def make_organization(webapi_client, auth, config):
    """Create a fresh organization, return it, clean up after the test."""
    created_ids: list[str] = []

    def _make(**overrides) -> dict:
        auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])
        payload = {
            **ORGANIZATION_TEMPLATE,
            "name": f"OrgQA_{uuid.uuid4().hex[:8]}",
            **overrides,
        }
        org = webapi_client.post("/api/members", data=payload)
        created_ids.append(org["id"])
        return org

    yield _make

    for oid in created_ids:
        try:
            webapi_client.delete(f"/api/members/{oid}")
        except Exception:
            pass  # cleanup must not fail the test
```

Rules:
- **Function-scoped by default.** Session-scoped factories leak shared state.
- **Always yield + cleanup.** Don't rely on a later DELETE test running — something
  may fail before it.
- **Accept `**overrides`.** Edge-case tests override one key, not the whole payload.
- **Return the backend response**, not the request payload — tests need the
  server-assigned `id`.
- **One factory per entity type per module.** If two modules need the same entity,
  promote the factory to `tests_webapi/conftest.py`.

## HAR capture on failure

Every test in `tests_webapi/` gets an autouse fixture (`har_recorder` in
[tests_webapi/conftest.py](conftest.py)) that records every HTTP
request/response made through `webapi_client` during the test. On failure, the
capture is serialized to a HAR 1.2 file and attached to the Allure report.

What you get:

- One `.har` attachment named `<test_name>.har` per failed test. Green tests
  produce no HAR attachment.
- Every request/response captured — including factory-fixture setup
  (`make_catalog` POST) and teardown (`catalog_operations.delete` DELETE).
- Method, URL, status, timings, request body, response body, all headers.
- `Authorization`, `Cookie`, `Set-Cookie`, `api_key`, `x-api-key` values are
  replaced with `***REDACTED***` before serialization — safe to attach to bug
  reports.

Open the HAR in Chrome DevTools (right-click the Network tab → "Import HAR
file..."), Charles, Fiddler, Paw, or any HAR viewer for a full request/response
timeline.

If you need to disable HAR for a specific test (e.g., a large response body
would bloat the report), override the fixture per-test:

```python
@pytest.fixture
def har_recorder():
    """Local override — no-op HAR recording for this test."""
    from fixtures.har_recorder import HARRecorder
    yield HARRecorder()
```

## Banned pattern: GlobalVariable-style state

Do **not** create session-scoped fixtures that return a created entity for the
whole run, and do **not** stash IDs in module-level or `pytest` session objects
for other tests to read. That was the Katalon pattern (`GlobalVariable.catalogId`
populated in `catalogCreate`, read by `catalogUpdate`) — it forces a test order,
breaks parallelism, and hides dependencies. Each test creates what it needs.
