# Project Improvement Plan

A step-by-step plan to address findings from [CODE_REVIEW.md](CODE_REVIEW.md). Each phase builds on the previous one — completing in order maximises return on each step. Issue identifiers (C1, S11, M29, N1, etc.) reference [CODE_REVIEW.md](CODE_REVIEW.md).

**Refreshed 2026-04-30** to reflect the work landed in PRs #151 (visibility sweep), #152 (`networkidle` removal) and #153 (first batch of REST Pydantic models).

## Guiding principles

1. **Visibility before fixes.** Don't fix bugs you can't measure. Stop hiding flakes/types/cleanup failures first; then fix what surfaces.
2. **Type safety as a force multiplier.** A typed REST surface (C3) makes every subsequent fix safer.
3. **Small reviewable PRs.** Each step is sized to be a single PR, ~½–3 days of focused work.
4. **Validation per step.** Every step has a concrete "done" check — typically a CI signal, a passing run, or a measurable count.
5. **Dataset module is reference quality.** It was refactored on 2026-04-28 — use it as the bar for "what good looks like."

## Effort scale

- **S** = small, ½–1 day
- **M** = medium, 1–3 days
- **L** = large, 3–7 days
- **XL** = ≥ 1 sprint

## Status legend

- ✅ **DONE** — landed in main branch (PR linked where known).
- ◐ **IN PROGRESS** — partially landed; remaining scope listed.
- ☐ **TODO** — not started.

---

## Phase 1 — Visibility (open the books)

**Goal:** See the real state of the project. After this phase, broken things actually show as broken.

### Step 1.1 — Remove `--retries=1` (S, addresses C1) ✅ DONE

Landed in PR #151 (commit `c67a66c`). `addopts` no longer carries `--retries=1`.

**Follow-up:** No known-flaky tests have been tagged with `@pytest.mark.flaky` yet. If flakes resurface in CI, tag them per-test (via `pytest-rerunfailures`) with a comment linking the ticket — don't add the global retry back.

### Step 1.2 — Enable pyright on `restapi/` (S, addresses C2) ✅ DONE

Landed in PR #151. [pyproject.toml:44](pyproject.toml#L44) now includes `restapi`.

**Follow-up:** Confirm a `pyright` invocation runs in CI on every PR. (If not, see Step 4.4.)

### Step 1.3 — Stop swallowing teardown errors (S, addresses C6) ✅ DONE

Landed in PR #151. All `make_*` factories in `tests/restapi/*/conftest.py` now log via `logger.warning(...)`. Verified across `platform`, `catalog`, `contacts`, `marketing`, `orders`.

**Follow-up:** Two test-body `except Exception: pass` patterns surfaced in this review (N5, N6). Roll them up under Step 3.7 (new) below.

### Step 1.4 — Surface HAR recorder errors (S, addresses M37) ☐ TODO

- Edit [utils/har_recorder.py:60-64](utils/har_recorder.py#L60) — replace `except Exception: pass` with `logger.exception(...)`.
- **Done when:** HAR recorder failures are logged.

**Phase 1 outcome (current):** ¾ done. Once 1.4 lands, the visibility cluster is closed.

---

## Phase 2 — Foundation (typed REST surface)

**Goal:** Eliminate the type-safety asymmetry between GraphQL and REST. This is the highest-leverage architectural change in the project.

### Step 2.1 — Pick a REST typing strategy (S, addresses C3) ✅ DONE

PR #153 picked **Option B (hand-written Pydantic models, conservative coverage)**. `restapi/types/` houses 14 hand-written models with `RestModel` as the base. Codegen from OpenAPI is parked as a future direction.

### Step 2.2 — First batch of typed responses (M, addresses C3) ✅ DONE

PR #153 typed the top responses: `Catalog`, `Category`, `Product`, `Member`/`Contact`/`Organization`/`Employee`/`Vendor`, `Role`, `Store`, `User` (read paths), `Promotion`, `Pricelist` + assignment, `CustomerOrder`. Operation methods updated to return the typed models.

### Step 2.3 — Migrate remaining REST operations (M, addresses C3, N1) ◐ IN PROGRESS

~70 method signatures still return `dict`, concentrated in:
- `dynamic_content_operations.py` (18 dict returns)
- `order_operations.py` write/search/recalculate paths (9)
- `user_operations.py` write paths (7)
- `cms_content_operations.py` (4), `promotion_operations.py` (4), `price_operations.py` (3), `category_operations.py` (3)
- 1–2 each: `oauth`, `settings`, `notifications`, `api_key`, `pricelist_assignment`, `member`, `employee`, `vendor`, `contact`, `pricelist`, `product`, `organization`, `role`, `store`, `catalog`, `promotion`

**Suggested order (one PR per module):**
1. `order_operations.py` — finishes the order surface that PR #153 started.
2. `dynamic_content_operations.py` — largest single module of `dict` returns.
3. `user_operations.py` — write paths return a `{succeeded, errors}` shape; consider a `UserOperationResult` TypedDict or model.
4. `promotion_operations.py` + `price_operations.py` + `pricelist_assignment_operations.py`.
5. `oauth`, `settings`, `notifications`, `api_key`, `cms_content` — clean-up batch.
6. Pure read endpoints across all modules: `search()`, list endpoints — typed list-result envelope (`ListResponse[T]`).

**Done when:** every method in `restapi/operations/` returns a typed model (or a documented TypedDict for status-style payloads).

### Step 2.4 — Strict `RestModel` (S, addresses N2, S21) ☐ TODO — gate behind 2.3

- Once 2.3 finishes, change [restapi/types/base.py](restapi/types/base.py) to `extra="forbid"`.
- For update flows that need round-tripping unknown fields, replace `extra="allow"` reliance with an explicit `unknown_fields: dict[str, Any] = Field(default_factory=dict)` capture field plus a `model_dump(...)` extension that re-emits them.
- Apply same to [gql/types/base.py](gql/types/base.py) (`GqlModel`).
- **Done when:** both base models are strict; the suite is green; any failures from the flip are tracked back to real schema drift.

**Phase 2 outcome:** REST + GraphQL parity in type safety. Schema-drift bugs surface at compile/validation time.

---

## Phase 3 — Correctness (close the silent-failure holes)

**Goal:** Fix the remaining places where bugs hide.

### Step 3.1 — Fix `AuthProvider` race condition (S, addresses C5) ☐ TODO

- Edit [core/auth/provider.py:42-68](core/auth/provider.py#L42) so the lock is held through the HTTP refresh.
- Optional: switch `RLock` → `Lock` (M34) if reentrance isn't required.
- **Done when:** refresh is single-flight; concurrent test workers can't double-refresh.

**Why now:** This is invisible today (single-threaded) but becomes a real bug the moment Step 3.5 / `pytest-xdist` lands. Fix it before adding parallelism.

### Step 3.2 — Replace `Component.wait_for_results` (M, addresses C8) ✅ DONE

Landed in PR #152. `Component` is now a thin locator wrapper; no `networkidle` anywhere in `page_objects/`.

**Follow-up:** M41 — `Component` is now so thin it barely justifies existing. Decide in Step 5.3a (new) whether to delete it or give it real shared behaviour.

### Step 3.3 — Replace `time.sleep` polling with `poll_until` (S, addresses C7, N6) ☐ TODO

- Replace loops in [tests/restapi/search/test_search.py:108-115](tests/restapi/search/test_search.py#L108) and [tests/restapi/platform/test_misc.py:37](tests/restapi/platform/test_misc.py#L37) with calls to [utils/polling_utils.py](utils/polling_utils.py) `poll_until`.
- The search-loop also contains a bare `except Exception: pass` (N6) — encode the tolerated failure modes in `predicate=` instead.
- **Done when:** no `time.sleep(...)` outside `polling_utils.py`; no bare `except: pass` in test bodies.

### Step 3.4 — Fix `Context.from_dataset` dead branch (S, addresses C4) ☐ TODO

- Edit [tests/context.py:34-36](tests/context.py#L34) — use `next((... for ...), None)`.
- **Done when:** unknown user produces friendly `ValueError`, not `StopIteration`.

### Step 3.5 — Investigate `serial` marker (S, addresses C10) ☐ TODO

- Decide whether parallel test execution is in use (or planned).
- If no: remove the `serial` marker definition from [pyproject.toml:26](pyproject.toml#L26).
- If yes: add `pytest-xdist`, document `xdist_group("serial")` usage, update CI workflows. **Sequence after 3.1** so the auth race is fixed first.
- **Done when:** `serial` marker is either removed or actually enforced.

### Step 3.6 — Public hook API on clients (S, addresses C9) ☐ TODO

- Add `add_response_hook` / `remove_response_hook` to [core/clients/rest.py](core/clients/rest.py) and [core/clients/graphql.py](core/clients/graphql.py).
- Update [tests/conftest.py:109](tests/conftest.py#L109) `har_recorder` fixture to use the public API.
- **Done when:** No `client._session` access from outside the class.

### Step 3.7 — Fix test-body silent failures (S, addresses N5) ☐ TODO

- Edit [tests/restapi/store/test_store.py:46-47](tests/restapi/store/test_store.py#L46) — replace `try/except Exception: pass` with `pytest.raises(requests.HTTPError)` and assert on the status code (the comment says "Expected: validation error or 400" — make that explicit).
- Sweep `tests/` for any other test-body `except: pass` that survived the C6 fix.
- **Done when:** no bare `except: pass` in test bodies under `tests/`.

### Step 3.8 — `OrderOperations.update` typed contract (S, addresses N4) ☐ TODO

- Decide between (a) keep `update(order: CustomerOrder)` typed-only and add a separate `update_raw(payload: dict)`, or (b) extend `CustomerOrder` with the mutators tests need.
- **Done when:** call sites are explicit about typed vs raw; pyright catches typo'd field names in the typed path.

**Phase 3 outcome:** No more silent failures. No more discouraged Playwright patterns. No more private member access.

---

## Phase 4 — Patterns and conventions

**Goal:** Eliminate duplication and enforce conventions automatically.

### Step 4.1 — Deduplicate `cart_operations.py` (M, addresses S11) ☐ TODO

- Add `_execute_command(operation_name, query, command)` helper to [gql/operations/base_operations.py](gql/operations/base_operations.py).
- Refactor each of the 12 cart mutations to use it.
- Optional: extract a `_build_cart_command` helper for the recurring `storeId/userId/currencyCode/cultureName/cartId` pattern.
- **Done when:** [gql/operations/cart_operations.py](gql/operations/cart_operations.py) shrinks by ~40–50%; tests still pass.

### Step 4.2 — Strict Pydantic models (S, addresses S21, N2) ☐ TODO — see Step 2.4

Folded into Phase 2.4. Apply `extra="forbid"` to both `GqlModel` and `RestModel` once REST coverage is complete.

### Step 4.3 — Make `restapi/constants.py` immutable (S, addresses S18, S19) ☐ TODO

- Convert lists → tuples, dicts → `MappingProxyType`.
- Move `ORDER_LINE_ITEM_TEMPLATE` into a fixture in `tests/restapi/orders/conftest.py` that reads the actual seeded product.
- **Done when:** `restapi/constants.py` only contains immutable, dataset-independent templates.

### Step 4.4 — Add ruff + extend pre-commit (M, addresses cross-cutting T3, T4) ☐ TODO

Current [.pre-commit-config.yaml](.pre-commit-config.yaml) only runs `black`. No `ruff`, no `pyright`.

- Add `ruff.toml` with rules: `E`, `W`, `F`, `I`, `UP`, `B`, `SIM`, `RUF`. Configure line-length to match existing style.
- Add custom rules where useful:
  - Ban `time.sleep` outside `utils/polling_utils.py`.
  - Ban `networkidle` string.
  - Ban `except Exception: pass` outside an explicit allowlist (none expected once Step 3.7 lands).
- Extend `.pre-commit-config.yaml` with `ruff`, `ruff-format`, `pyright` (mirror CI).
- Add a `lint` workflow (or fold into existing) that runs ruff + pyright on PRs.
- **Done when:** PRs blocked on lint failures; existing violations fixed or grandfathered.

### Step 4.5 — Naming consistency (S, addresses S12, M45) ☐ TODO

- Rename `restapi/operations/base.py` → `base_operations.py`.
- Rename `RestBaseOperations` → match the GraphQL naming. Recommended: rename both to `GraphQLOperations` (in `gql/`) and `RestOperations` (in `restapi/`) for symmetry.
- Update all imports.
- **Done when:** Naming convention is consistent across `gql/` and `restapi/`.

### Step 4.6 — Marker payloads to kwargs (S, addresses S17) ☐ TODO

- Migrate all marker call sites from `@pytest.mark.with_cart([...])` (positional) to `@pytest.mark.with_cart(items=[...])` (kwargs).
- Update fixtures in [tests/conftest.py](tests/conftest.py) (six positional `marker.args[0]` reads at lines 30, 32, 181, 206, 208, 270) to read `marker.kwargs["..."]`.
- Apply to `with_user`, `with_cart`, `quantity_control`, `range_filter_type`, `checkout_mode`.
- **Done when:** All marker payloads use kwargs.

**Phase 4 outcome:** Conventions are enforced automatically. Major duplication is gone. Models reject schema drift.

---

## Phase 5 — Architectural cleanup

**Goal:** Address structural issues that need careful coordination.

### Step 5.1 — Split conftest by suite (M, addresses S14, S15) ☐ TODO

- Create `tests/e2e/conftest.py` — move e2e-only fixtures and the e2e branches of shared fixtures (`with_user`'s `BrowserStorage` part, `with_cart`'s `set_user_id`, `screenshot_on_failure`).
- Create `tests/graphql/conftest.py` if any graphql-specific helpers emerge.
- Trim root [tests/conftest.py](tests/conftest.py) to only truly shared fixtures.
- **Done when:** No `if marker == "e2e"` branches in shared conftest; suite-specific fixtures live near their suites.

### Step 5.2 — Make `with_user` opt-in (M, addresses S13) ☐ TODO

- Rename `with_user` → `signed_in_user` (keeps semantic clarity).
- Remove the chain that pulls `with_user` through `with_cart` / `delete_cart_after` / `ctx`.
- Update all tests that need authentication to request the fixture explicitly.
- **Done when:** Test signature reveals what fixtures activate; no implicit chain.

### Step 5.3 — Cache page object children (S, addresses S16) ☐ TODO

- Edit [page_objects/components/top_header.py](page_objects/components/top_header.py) and similar files: assign children in `__init__` instead of recreating per-property.
- **Done when:** Pattern matches the convention documented in [.claude/skills/create-ui-layer/SKILL.md](.claude/skills/create-ui-layer/SKILL.md).

### Step 5.3a — Decide `Component` base class fate (S, addresses M41) ☐ TODO

After C8 fix, [page_objects/components/component.py](page_objects/components/component.py) is just `__init__(self, root)` + `root` property — barely a base class.

- **Option A:** Delete and have components hold a `Locator` directly.
- **Option B:** Give it real shared behaviour (`wait_visible()`, `data-test-id` lookups, common attribute accessors).
- **Done when:** decision applied across `page_objects/components/`.

### Step 5.4 — Standardise `__init__.py` placement in `tests/` (S, addresses S24) ☐ TODO

- Pick: **no `__init__.py` anywhere in `tests/`** (recommended).
- Delete existing `tests/restapi/__init__.py` and subpackage init files.
- Verify pytest still collects all tests.
- **Done when:** Consistent (probably empty) init policy across `tests/`.

### Step 5.5 — Improve `RestClient._parse_response` (S, addresses S27) ☐ TODO

- Edit [core/clients/rest.py:60-62](core/clients/rest.py#L60) — return text for non-JSON content types instead of raising `NotImplementedError`.
- Update return type to `_ResponseBody | str | None`.
- **Done when:** Tests against text-returning endpoints don't crash with `NotImplementedError`.

### Step 5.6 — Improve `GraphQLClient.execute` (S, addresses S26) ☐ TODO

- Edit [core/clients/graphql.py:36-38](core/clients/graphql.py#L36) — only raise when `data is None`; return body otherwise (let caller inspect `errors` field).
- Or: introduce a `GraphQLResponse(data, errors)` value object.
- Update tests that depend on the raise-on-error behaviour.
- **Done when:** Partial-result GraphQL responses are testable.

### Step 5.7 — Reorganise `restapi/operations/` into subpackages (M, addresses M44) ☐ TODO

- Group operation files by domain: `restapi/operations/catalog/`, `platform/`, `orders/`, etc.
- Update `restapi/operations/__init__.py` to re-export from new locations (preserves existing imports).
- **Done when:** Top-level operations namespace is split into thematic subpackages.

**Phase 5 outcome:** Architecture matches documented conventions; structural issues that have been compounding are resolved.

---

## Phase 6 — Polish

**Goal:** Cosmetic and ergonomic improvements. Low individual value, but they accumulate.

| Step | Issue | Effort | Action | Status |
|---|---|---|---|---|
| 6.1 | M29 | S | Add CI check that every product ID in `dataset/cheat_sheet.md` exists in `data/`, or remove the cheat sheet. | ☐ |
| 6.2 | M31 | S | Replace `os.path.join` with `Path` in [tests/conftest.py](tests/conftest.py). | ☐ |
| 6.3 | M32 | S | Move `_INVALID_FILENAME_CHARS` to `utils/safe_filename.py`. | ☐ |
| 6.4 | M33 | S | Use `json.dumps` for `BrowserStorage.set_user_id` to handle special characters. | ☐ |
| 6.5 | M35 | S | Validate `delete_cart`'s server response with `isinstance` check. | ☐ |
| 6.6 | M36 | S | `_collect_fragments` should raise on unknown fragment spreads. | ☐ |
| 6.7 | M38 | M | Route `AuthProvider` HTTP calls through a shared session for HAR observability. | ☐ |
| 6.8 | M39 | S | Decide on test-file constant style (`_PRODUCT_ID` vs `PRODUCT_ID`); apply uniformly. | ☐ |
| 6.9 | M40 | S | Remove `inflection` dep or keep with comment. | ☐ |
| 6.10 | M42 | S | Promote `MainLayout._page` access via property. | ☐ |
| 6.11 | M43 + N3 | M | Consolidate 7 GitHub workflows into reusable workflow + matrix. | ☐ |
| 6.12 | S20 | S | Decide: keep `gql()` no-op marker (with comment) or remove. | ☐ |
| 6.13 | S22 | S | Fix `# type: ignore[call-arg]` in [core/global_settings.py:45](core/global_settings.py#L45). | ☐ |
| 6.14 | S25 | S | Move `dataset_manager.log` out of the package directory. | ☐ |
| 6.15 | S28 | S | Stop mutating server response in `make_user`; return a typed credential bundle. | ☐ |
| 6.16 | S23 | M | Document Allure decorator policy in `CLAUDE.md` and add a hook to enforce. | ☐ |
| 6.17 | M30 | — | ✅ DONE — `dataset/_legacy/` removed. | ✅ |

---

## Suggested timeline (refreshed)

A rough sketch — adapt to team capacity. Sprint 1 work is now ✅ done.

| Sprint | Focus | Deliverables | Status |
|---|---|---|---|
| 1 | Phase 1 | Visibility steps 1.1–1.3 | ✅ Done (PR #151) |
| — | Phase 3.2 | `Component.wait_for_results` removed | ✅ Done (PR #152) |
| — | Phase 2.1–2.2 | First batch of typed REST responses | ✅ Done (PR #153) |
| 2 | Phase 1.4 + Phase 3 | M37 logging; C5 race; C7+N6 polling; C4 dead branch; C9 hooks; N5 test-body sweep | ☐ TODO |
| 3 | Phase 2.3 (part 1) | Type `order`, `dynamic_content`, `user` write paths | ☐ TODO |
| 4 | Phase 2.3 (part 2) + 2.4 | Finish typing remaining modules; flip `extra="forbid"` on both base models | ☐ TODO |
| 5 | Phase 4.1–4.3 | Cart operations dedup; immutable constants | ☐ TODO |
| 6 | Phase 4.4–4.6 | ruff + pre-commit live; naming + marker migration | ☐ TODO |
| 7–8 | Phase 5 | Conftest split; with_user opt-in; client improvements | ☐ TODO |
| 9+ | Phase 6 | Polish, opportunistically | ☐ TODO |

---

## Risks and dependencies

- **Phase 2.3 → 2.4.** Don't flip `extra="forbid"` until coverage is complete; otherwise tests fail for "the model is missing fields" reasons rather than schema drift.
- **Phase 3.5 (xdist) depends on Phase 3.1 (auth race).** The auth race is invisible today but becomes a real correctness bug under parallel runs.
- **Phase 4.4 (ruff) should land early in Phase 4** so subsequent phases benefit from automatic enforcement.
- **Phase 5.2 (`with_user` opt-in) is the riskiest single change.** Touches every test that uses `with_cart`/`ctx`. Recommend a feature branch with a long-running CI loop before merging.
- **Cart operations refactor (4.1) may temporarily reduce readability.** A helper-heavy refactor can feel terse — ensure the helper is well-documented.

---

## Success metrics

After completing **Phases 1–4**:

- pyright passes on the entire repo. ◐ (configured ✅; per-module clean still in flight)
- ruff/pre-commit blocks pattern violations on PRs. ☐
- Zero `except: pass` in factories. ✅
- Zero `except: pass` in test bodies. ☐ (regression in N5/N6 to fix)
- Zero `time.sleep` outside `utils/polling_utils.py`. ☐ (2 sites)
- Zero `networkidle` in `page_objects/`. ✅
- REST + GraphQL operations both return typed Pydantic models. ◐ (~50% REST done)
- `--retries=1` no longer hides flakes. ✅
- Every test factory logs cleanup failures. ✅
- Both base models use `extra="forbid"`. ☐

After completing **Phases 5–6**:

- Conftest hierarchy matches the documented suite-locality rule. ☐
- No private-attribute access from tests. ☐
- Every page-object child is cached in `__init__`. ☐
- All conventions from `.claude/skills/` are either enforced or removed from the docs. ☐

---

## Notes

- Issue identifiers reference [CODE_REVIEW.md](CODE_REVIEW.md). New identifiers (N1–N7) were introduced in the 2026-04-30 review pass.
- The dataset module (refactored 2026-04-28) is not part of this plan — it's already at the target quality level.
- `_BACKUP/` should be deleted at some point in Phase 6, but is currently in active use as a source of test material per project owner direction.
- Three PRs since the previous review (#151, #152, #153) have closed C1, C2, C6, C8 outright and made meaningful progress on C3.
