# Refinements

Review of the whole repository (core, api, dataset, fixtures, pages, all test projects, tooling, docs), done on 2026-09-30 on branch `vcst-6033`. Each item names where the problem is, what to do, and how to know it is done.

## Change log

| Date | Change |
|---|---|
| 2026-09-30 | Initial review. |
| 2026-09-30 | GitHub workflow `.github/workflows/auto-tests.yml` added (manual run through the reusable `VirtoCommerce/.github` Playwright workflow). R8.2 done; R0.3, R8.4, R8.7, R8.8 partly covered; new items R8.17–R8.22 from the workflow review. |
| 2026-09-30 | `backend-packages.json` restored from `dev` (R8.17 done). README: new "Continuous integration" section (inputs, what the shared workflow does, secrets, keeping `backend-packages.json` current), CI artifact instructions under Reports, `backend-packages.json` and `.github/workflows/` in Prerequisites and Project structure. |
| 2026-09-30 | Format: section tables replaced by one heading per item with emoji status (⬜ to do, ✅ done, ❌ won't do) and labelled description lines; content unchanged. |
| 2026-09-30 | `backend-packages.json` bumped to edge versions (platform 3.1074.0, 27 modules); README explains how to keep it on edge. |

## How to use this file

- Every item is a heading `<status> <ID> · <priority> · <title>` followed by **Where**, **Problem**, **What to do** and, where useful, **Done when**.
- Status:
  - ⬜ to do
  - ✅ done: swap the emoji when the item is merged and add a **Done in:** line with the commit or PR.
  - ❌ won't do: add a **Reason:** line.
- After changing a status, update the counts in [Progress](#progress).
- Priority: **P1** fix first (wrong results, data leaks, broken setups), **P2** reliability and maintainability, **P3** polish and consistency.
- Items marked **decision** need a choice before work starts; they are collected in [Section 0](#0-decisions-needed).
- Line numbers are from the review date; search by symbol name if they have moved.

## Progress

**Total: ✅ 2 of 110 done.**

- ⬜ [0. Decisions needed](#0-decisions-needed): 0 of 6
- ⬜ [1. Correctness](#1-correctness): 0 of 10
- ⬜ [2. Isolation and cleanup](#2-isolation-and-cleanup): 0 of 12
- ⬜ [3. Test quality](#3-test-quality): 0 of 14
- ⬜ [4. Page objects and e2e](#4-page-objects-and-e2e): 0 of 14
- ⬜ [5. API clients](#5-api-clients): 0 of 12
- ⬜ [6. Dataset and fixtures](#6-dataset-and-fixtures): 0 of 13
- ⬜ [7. GraphQL documents](#7-graphql-documents): 0 of 7
- ⬜ [8. Configuration, tooling, CI, docs](#8-configuration-tooling-ci-docs): 2 of 22 (R8.2, R8.17)

## Suggested order of work

1. **Section 0 decisions**, so nothing is blocked later.
2. **All P1 items** (sections 1 and 2): they make runs trustworthy and stop leaking data.
3. **CI pipeline (R8.1–R8.3)**, so every later refactoring is checked automatically.
4. **Shared helpers first, then their callers:** R5.1–R5.3 (response helpers) before R5.4+; R6.9 (seeded constants) before the duplicate-removal items in sections 3 and 4.
5. The remaining P2, then P3, section by section.

---

## 0. Decisions needed

### ⬜ R0.1 · Sign-in retry: backoff or shared token

- **Decision:** Sign-in retry for the concurrent same-user `/connect/token` 500
- **Options:** a) longer exponential backoff with jitter (6 attempts, up to ~11 s); b) sign in once per run and share the token between workers
- **Notes:** Bug report: [BUG-concurrent-token-sign-in-500.md](BUG-concurrent-token-sign-in-500.md). Current: 3 attempts ~0.2–0.6 s (`api/auth/token-auth-client.ts:68-73`).

### ⬜ R0.2 · HTTP logging redaction is expected but missing

- **Decision:** HTTP logging safety features that are expected but **not in the code**: secret redaction, `Secret` env values, `onExchange` listener, redacted network-error call logs
- **Options:** a) implement them; b) confirm they were dropped
- **Notes:** Earlier design notes describe them as agreed; `api/http/http-client.ts` calls `context.fetch` directly and nothing redacts `Authorization` headers or passwords.

### ⬜ R0.3 · Scope of the CI pipeline

- **Decision:** Scope of the CI pipeline
- **Options:** quality job on every PR; e2e/API job manual + nightly; destructive tests opt-in
- **Notes:** **Partly decided:** manual test runs exist (`auto-tests.yml`, suite choice + `--grep`). Still open: PR quality job (R8.1), nightly schedule (R8.20), destructive runs (R8.3), database matrix (R8.19).

### ⬜ R0.4 · Where platform-wide settings tests run

- **Decision:** Where platform-wide settings tests run
- **Options:** a) one serial project (`workers: 1`) for everything that changes global settings; b) keep them in their files but make restore undo only the test's own change
- **Notes:** See R2.1.

### ⬜ R0.5 · Tracker keys for known product issues

- **Decision:** Tracking of known product issues
- **Options:** Every `test.fail(true, …)` and the `test.fixme` gets a tracker key in its reason
- **Notes:** 6 `test.fail` (page builder toasts, duplicate permalink, verbatim permalinks, store without name) and 1 `fixme` (theme zip).

### ⬜ R0.6 · Retries on CI

- **Decision:** Retries on CI
- **Options:** `retries: 1` on CI only, or none
- **Notes:** Retries hide flakiness; they also stop a single slow-environment timeout from failing a nightly run.

---

## 1. Correctness

Things that make results wrong or setups fail.

### ⬜ R1.1 · P1 · Unset `GOOGLE_MAPS_API_KEY` breaks the dataset

- **Where:** `core/env.ts:32`, `dataset/data/stores/acme_electronics.json:81`, `core/interpolate.ts:16`
- **Problem:** `GOOGLE_MAPS_API_KEY` is declared optional, but the store data interpolates it and interpolation throws when it is missing, so an unset key breaks **every** test that loads the dataset.
- **What to do:** Either make it required (`string().min(1)`), or support an empty default in interpolation; align README and `.env.example`.
- **Done when:** Unset key: either a clear start-up error or tests run.

### ⬜ R1.2 · P1 · Seeder ignores `succeeded:false`

- **Where:** `dataset/seeder.ts:76`
- **Problem:** Seeding only checks the HTTP status. User creation answers `200 {succeeded:false}` (existing user, rejected password), so users are "seeded" without error and a changed `USERS_PASSWORD` is never applied.
- **What to do:** Check `succeeded` for security endpoints (manifest flag or dedicated user upsert: find → create / reset password).
- **Done when:** Re-seed with a new password actually changes it; a rejected password fails the seed.

### ⬜ R1.3 · P1 · Cart-validation checks pass vacuously

- **Where:** `tests/graphql/cart/cart-validation.spec.ts:232-260`
- **Problem:** `readCartValidation` returns `undefined` errors when the cart is missing, and `expectNoQuantityError(undefined)` passes: five "no error" tests can pass vacuously.
- **What to do:** `requireFields` on the returned cart before reading errors.
- **Done when:** The tests fail when the cart is null.

### ⬜ R1.4 · P1 · Empty entity sends `PUT []`

- **Where:** `dataset/seeder.ts:40-46`, `dataset/seed-requests.ts:13`
- **Problem:** An entity with no items still sends a request; for array payloads that is `PUT []`, which can wipe e.g. store aggregation properties.
- **What to do:** `continue` after the "no items" warning.
- **Done when:** Empty entity folder sends nothing.

### ⬜ R1.5 · P2 · `"(anonymous)"` sent as the operation name

- **Where:** `api/graphql/graphql-client.ts:49`
- **Problem:** For an unnamed document the placeholder `"(anonymous)"` is sent as `operationName`, which the server rejects. (All current documents are named.)
- **What to do:** Send `operationName` only when found; keep the placeholder for messages.
- **Done when:** Unnamed document executes.

### ⬜ R1.6 · P2 · GraphQL client parses the body before checking the status

- **Where:** `api/graphql/graphql-client.ts:54-59`
- **Problem:** The body is parsed before the status is checked, so a 502 HTML page or empty 401 fails with "not valid JSON" instead of the HTTP error.
- **What to do:** Check `!response.ok` first, parse leniently.
- **Done when:** 502 shows the status error.

### ⬜ R1.7 · P2 · Organization orders read without a sort

- **Where:** `tests/graphql/orders/orders.spec.ts:51-53`
- **Problem:** `orders[0]` is called "newest organization order" but the query has no sort.
- **What to do:** Pass `sort: "createdDate:desc"`.
- **Done when:** Deterministic order.

### ⬜ R1.8 · P2 · "Cancel an indexation" passes whether cancel works or not

- **Where:** `tests/restapi/search/indexes.spec.ts:59-73`
- **Problem:** "cancel an indexation" asserts `completed === true`; a one-document indexation finishes on its own, so the test passes whether cancel works or not.
- **What to do:** Cancel a long job and assert an aborted/cancelled state, or drop the test.
- **Done when:** Test fails if cancel is a no-op.

### ⬜ R1.9 · P2 · `typeof` tautology in orders

- **Where:** `tests/restapi/orders/orders.spec.ts:101-103`
- **Problem:** Tautology: `typeof enabled === "boolean"`.
- **What to do:** Compare with the known configuration, or remove.
- **Done when:** Assertion can fail.

### ⬜ R1.10 · P2 · `getStockQuantity` fails for zero-stock records

- **Where:** `dataset/stock.ts:12-27`
- **Problem:** `getStockQuantity` throws "missing" for a center that has an inventory record with 0 stock, because zero-stock records are filtered out first.
- **What to do:** Look up the raw record; return 0 or throw "not stocked".
- **Done when:** Zero-stock center gives 0 or a clear error.

---

## 2. Isolation and cleanup

Data leaks and interference between parallel tests.

### ⬜ R2.1 · P1 · REST files race on global settings

- **Where:** `tests/restapi/platform/settings.spec.ts:65-91`, `content/validation.spec.ts:79-91`, `content/files.spec.ts:90-97`, `catalog-personalization/tags.spec.ts:40-53,205-213`, `catalog/products.spec.ts:159-182`, `search/indexes.spec.ts`, `platform/system.spec.ts:62-73`
- **Problem:** Several files change the same global platform settings (file-extension blacklist, indexing jobs, member groups, tag inheritance, editorial review types) and restore a snapshot; files run in parallel, so restores overwrite each other. `files.spec` relies on the blacklist without arranging it. `mode: "default"` in three files does not help (the race is between files).
- **What to do:** Per decision R0.4. Also: `files.spec` arranges its own blacklist entry; remove the three `test.describe.configure({ mode: "default" })`.
- **Done when:** Global-settings tests cannot overlap; `files.spec` passes alone.

### ⬜ R2.2 · P1 · UI-only cart tests leak the default cart

- **Where:** `tests/e2e/frontend/catalog/category.spec.ts:118-206`, `catalog/product-configuration.spec.ts:23-153`, `wishlists/wishlist-items.spec.ts:122`, `cart/cart-merge.spec.ts:51-79`; `fixtures/shopper.fixture.ts:32`
- **Problem:** Tests that add to the cart only through the UI do not request `shopper`, so the default cart is never removed.
- **What to do:** Register default-cart removal inside `storageState` when `app === "frontend"` (it already knows the credentials / anonymous id), so every frontend test cleans up without asking. Do **not** make `storageState` depend on `frontendContext` (breaks the backend project, where `user` is the platform admin).
- **Done when:** No carts left for test users after a frontend run.

### ⬜ R2.3 · P1 · Cart save-for-later uses a seeded user

- **Where:** `tests/graphql/cart/cart-save-for-later.spec.ts:20-56`
- **Problem:** Uses the seeded `acme_store_maintainer_1`; the saved-for-later list is one per user and the cleanup deletes the whole list; exact `toEqual` breaks if anything else saved items.
- **What to do:** Use `customerAccount`, as the second describe in the file does.
- **Done when:** No seeded user's list is modified.

### ⬜ R2.4 · P1 · Checkout order cleanup registered late

- **Where:** `tests/e2e/frontend/checkout/checkout-order.spec.ts:45-54`
- **Problem:** Order cleanup is registered only after the assertion and only if a number was found: a timeout leaks the order.
- **What to do:** Capture the order from the create-order GraphQL response (or register cleanup by order number before asserting), `requireFields` instead of `if`.
- **Done when:** Failed run leaves no order.

### ⬜ R2.5 · P2 · `Promise.all` creates leak one entity on failure

- **Where:** `contacts/contacts.spec.ts:98-132`, `contacts/employees.spec.ts:56-77`, `contacts/members.spec.ts:75-146`, `contacts/organizations.spec.ts:58-166`, `marketing/dynamic-content.spec.ts:123-126`
- **Problem:** `Promise.all` creates two entities and registers cleanup only after both succeed; if one fails, the other leaks.
- **What to do:** Register cleanup by draft id first (builders set ids), then create.
- **Done when:** Pattern gone from REST specs.

### ⬜ R2.6 · P2 · Coupon cleanup registered late

- **Where:** `tests/restapi/marketing/promotions.spec.ts:110-170`
- **Problem:** Coupon cleanup registered after assertions / inside an `assert:` step.
- **What to do:** Register by code before `saveCoupons` (find-then-delete).
- **Done when:** —

### ⬜ R2.7 · P2 · `arrangeApiKey` and `arrangePage` register cleanup late

- **Where:** `dataset/arrange/security.ts:29-32`, `dataset/arrange/page-builder.ts:11-12`
- **Problem:** `arrangeApiKey` and `arrangePage` register cleanup after the create/validation, so a failing check leaks.
- **What to do:** Register first, find by key value / unique name inside the cleanup.
- **Done when:** —

### ⬜ R2.8 · P2 · `saveMemberAddress` registers no cleanup

- **Where:** `dataset/arrange/contact.ts:17-42`
- **Problem:** `saveMemberAddress(es)` registers no cleanup; with a seeded organization (option `customerAccountOrganizationId`) test addresses stay forever.
- **What to do:** Take `cleanupStack`, register removal, rename to `arrangeMemberAddress(es)`.
- **Done when:** —

### ⬜ R2.9 · P2 · Deleted users stay in the token cache

- **Where:** `dataset/arrange/customer-account.ts:62-69`, `fixtures/customer-account.fixture.ts:124`
- **Problem:** Fresh accounts stay in the worker token cache after the user is deleted; `signOutAll` later refreshes/revokes tokens of deleted users.
- **What to do:** Push `tokenManager.signOut(username, storeId)` to `cleanupStack` right after the user is created.
- **Done when:** Token cache holds no deleted users at worker end.

### ⬜ R2.10 · P2 · `addOrganizationMembership` has no find-or-create guard

- **Where:** `dataset/arrange/customer-account.ts:80-91`
- **Problem:** `addOrganizationMembership` has no find-or-create guard and no role, unlike `arrangeCustomerAccount`.
- **What to do:** Shared `ensureMembership(userId, organizationId, role)`.
- **Done when:** —

### ⬜ R2.11 · P2 · Notifications test runs on the shared admin

- **Where:** `tests/restapi/platform/notifications.spec.ts:28-36`
- **Problem:** "mark all as read" then expects `newCount === 0` for the shared admin while other files create notifications.
- **What to do:** Run as a fresh user.
- **Done when:** —

### ⬜ R2.12 · P3 · Local-storage uploads cannot be deleted

- **Where:** `tests/restapi/platform/assets.spec.ts:55-65`
- **Problem:** Local-storage upload leaves a file behind (the platform cannot delete local-storage uploads).
- **What to do:** Document as a known limitation in the test (unique name already), or skip on shared environments.
- **Done when:** Decision recorded.

---

## 3. Test quality

Weak assertions, duplicates, hard-coded data.

### ⬜ R3.1 · P1 · Tests without an assertion

- **Where:** `tests/restapi/catalog-publishing/channels.spec.ts:132-141`, `tests/restapi/platform/user-passwords.spec.ts:79-84`
- **Problem:** Tests without any assertion ("save evaluated product completeness", "send a verification email").
- **What to do:** Assert the stored result / returned status.

### ⬜ R3.2 · P2 · Weak REST assertions

- **Where:** REST: `channels.spec.ts:104-108,122-128`, `tags.spec.ts:32-37,189-191`, `orders.spec.ts:78-80,125-127`, `notifications.spec.ts:22-25`, `changelog.spec.ts:22-46`, `system.spec.ts:27-29,70-72`, `health.spec.ts:21`, `authorization.spec.ts:47`, `assignments.spec.ts:72`, `prices.spec.ts:156-157`, `indexes.spec.ts:38,55`, `organizations.spec.ts:152`
- **Problem:** Assertions that pass on empty or arbitrary data (`length > 0` on shared data, `expect.any(...)`, `Array.isArray`, `every` on possibly empty list, job started but not finished).
- **What to do:** Assert the specific arranged entity / exact value; wait for jobs to finish.

### ⬜ R3.3 · P2 · Weak GraphQL assertions

- **Where:** GraphQL: `product-variations.spec.ts:40-53`, `page-context.spec.ts:54-66`, `cart-validation.spec.ts:263-271`, `cart-promotions.spec.ts:44-66`, `current-addresses.spec.ts:106,126`, `contact-search.spec.ts:31,41`
- **Problem:** Same kind: comparisons that pass on empty results, an assertion helper that returns early without asserting, `>=` where exact counts are known.
- **What to do:** Assert non-empty, exact counts, specific gift/discount values.

### ⬜ R3.4 · P2 · Cart-lifecycle "get the cart" tests never query the cart

- **Where:** `tests/graphql/cart/cart-lifecycle.spec.ts:28-60`
- **Problem:** "get the cart of …" never calls the `cart` query.
- **What to do:** Arrange with `arrangeCart`, act with `GetCartDocument`.

### ⬜ R3.5 · P2 · Duplicate REST tests

- **Where:** REST duplicates: `catalog/assets.spec.ts` vs `platform/assets.spec.ts`; `organizations.spec.ts:112-159`; `members.spec.ts:17-59,175-188`; `stores.spec.ts:92-112`; `users.spec.ts:111-121` vs `authorization.spec.ts:20-31`; `pricelists.spec.ts:95-110` vs `prices.spec.ts:20-35,75-90`; `health.spec.ts:42-50` vs `indexes.spec.ts:21-29`
- **Problem:** Tests repeating each other.
- **What to do:** Keep one of each; remove combined "create, rename, delete" variants.

### ⬜ R3.6 · P2 · Duplicate GraphQL tests

- **Where:** GraphQL duplicates: `pickup-locations.spec.ts:276-305` (Berlin/Billund) vs `:221-250`; `page-context.spec.ts:68-92`
- **Problem:** Same.
- **What to do:** Merge or remove.

### ⬜ R3.7 · P2 · Tests depend on files hosted on GitHub

- **Where:** `tests/restapi/catalog/assets.spec.ts:9`, `platform/assets.spec.ts:9-10`
- **Problem:** Upload-from-URL tests download from `raw.githubusercontent.com/.../dev/`: network or rename breaks them.
- **What to do:** Upload a local fixture first, then upload-from-URL that asset.

### ⬜ R3.8 · P2 · Weak backend search and validation tests

- **Where:** e2e backend: `search-and-validation.spec.ts:131-135,161-166,95-100`
- **Problem:** Duplicate-permalink check spins through 15 reloads when correctly rejected; special-character assertions only run `if` the page exists (vacuous); required-fields case depends on the previous loop iteration.
- **What to do:** Assert explicitly on both outcomes; give both fields per case.

### ⬜ R3.9 · P2 · Seeded ids repeated across specs

- **Where:** Seeded ids repeated across specs: `laptop-acer-predator-helios-neo-16-ai` (7 REST + 3 GraphQL + 3 e2e files), `smartphone-apple-iphone-17-256gb-black` (12 GraphQL), `…-mist-blue`, `sodimm-crucial-ddr4-2400-8gb`, `smartphone-samsung-galaxy-a57-5g` (5 e2e), configurable memory option names, variation SKUs
- **Problem:** Hard-coded in many files.
- **What to do:** Use the shared seeded-data constants from R6.9.

### ⬜ R3.10 · P3 · Admin username repeated in every REST file

- **Where:** `USERNAME = "acme_store_administrator@acme.com"` + identical `test.use` in all 40 REST files; seeded usernames in GraphQL
- **Problem:** Repeated.
- **What to do:** Export seeded user constants (R6.9) and an `asStoreAdministrator` option or shared `test.use` value.

### ⬜ R3.11 · P3 · REST helpers that belong in `dataset/arrange`

- **Where:** REST local helpers: `arrangeRole` (roles.spec.ts:129-145), `arrangeOrder`/`orderWithLineItem` (orders.spec.ts:230-242), `createCategoryWithProduct`/`createProduct` (tags.spec.ts, products.spec.ts), settings save/restore (6 places), `newApiKey` (5 places), `/connect/token` form bodies
- **Problem:** Helpers duplicated in specs.
- **What to do:** Move to `dataset/arrange/*` / builders (`arrangeSettingValue`, `arrange/order.ts`, `arrangeRole`, `newApiKey`); export `TOKEN_PATH`.

### ⬜ R3.12 · P3 · GraphQL helpers that belong in `dataset/arrange`

- **Where:** GraphQL local helpers: product configuration fetch (3 files), `Configuration-${id}` SKU (2), pickup helpers duplicated between `cart-pickup-locations` and `pickup-locations` specs, `quoteFromCart`/`registerQuoteRemoval`, invite helper, "create list + add item", manual `new GraphqlClient(await tokenManager.authorize(...))`
- **Problem:** Duplicated.
- **What to do:** Move to `dataset/arrange` (`quote.ts`, `pickup-location.ts`, `catalog.ts`), reuse `signInGraphqlClient`.

### ⬜ R3.13 · P3 · `??` fallbacks hide missing data

- **Where:** `?? ""`, `?? []`, `?? 0`, `?? undefined`, `?.` hiding missing data in REST (settings, catalogs, changelog, orders, dynamic-content, promotions, assignments), GraphQL (cart-validation, pickup-locations, current-addresses, organizations-locked, contact-registration) and e2e (wishlist-items, wishlist-lists, checkout-pickup, shared-list) specs
- **Problem:** Violates the "no fallbacks" convention.
- **What to do:** `requireFields` / explicit assertions; see R6.1 for `null` support.

### ⬜ R3.14 · P3 · Test naming and step conventions

- **Where:** Test naming and steps: imperative vs statement titles (REST health, seo, changelog, assets, user-lock); `act:` steps that only call arrange helpers; actions/assertions outside steps (several e2e and GraphQL specs); combined "act and assert:" steps; `orders.spec.ts:217-220` hard-codes 65 instead of `MAX_ORDER_NUMBER_LENGTH + 1`
- **Problem:** Inconsistent.
- **What to do:** One title style (imperative); every action in an `arrange:`/`act:`/`assert:` step.

---

## 4. Page objects and e2e

### ⬜ R4.1 · P1 · Page-builder wait loops give up silently

- **Where:** `pages/backend/page-builder/page-builder-shell.ts:79-100`, `pages-list-blade.ts:82-87`
- **Problem:** `waitUntilListed`, `waitUntilCounterMatchesList`, `waitForRows` are manual `waitForTimeout` loops that **give up silently**; tests then fail later on a vague check. Callers wrap them in one-shot assertions (5 places).
- **What to do:** Replace with `expect.poll` / `toPass` that fail with a clear message; callers assert directly.

### ⬜ R4.2 · P2 · List-blade search can match an earlier response

- **Where:** `pages/backend/page-builder/pages-list-blade.ts:38-43`
- **Problem:** Search waits for any `page-builder-pages/search` response (can be a previous keyword) and casts the body with `?? 0`.
- **What to do:** Match the request's keyword; validate the body.

### ⬜ R4.3 · P2 · Blades picked by position; double navigation in `open()`

- **Where:** `pages/backend/page-builder/page-builder-shell.ts:45-46,57-65`
- **Problem:** List/details blades picked by position (`first()`/`last()`); `open()` navigates twice and waits for `networkidle`.
- **What to do:** Locate blades by title; navigate once and wait for the grid.

### ⬜ R4.4 · P2 · Date picker and configuration-expand waits

- **Where:** `pages/backend/shell/controls.ts:101-118`, `pages/frontend/components/product-configuration.ts:43-47`
- **Problem:** Date picker checks the new month before it renders and uses `.first()` over neighbour-month cells; closes by clicking a blade title. Configuration `expand()` does not wait for the expanded state.
- **What to do:** Wait for the month header change; exclude off-month cells; close with `Escape`; wait for `vc-widget--collapsed` to disappear.

### ⬜ R4.5 · P2 · `scrollToProduct` is an unbounded loop

- **Where:** `pages/frontend/pages/category-page.ts:31-50`
- **Problem:** `scrollToProduct` is an endless loop with `catch` as control flow and a string `evaluate`.
- **What to do:** Bounded loop or `expect.poll` over the loaded cards.

### ⬜ R4.6 · P2 · Substring text matching plus `.first()`

- **Where:** `pages/frontend/pages/account-pages.ts:28`, `components/wishlist.ts:51-52`, `select-address-modal.ts:20-22`, `address-filters.ts:36-38`, `product-configuration.ts:51,76`, `address-form.ts:47,52`
- **Problem:** Substring `hasText` + `.first()` (e.g. `card("list-x")` also matches `list-x-edited`); wishlist menu items page-wide `:visible`.
- **What to do:** Use `exactText`; scope menus to the opened card.

### ⬜ R4.7 · P2 · Page-wide `[data-product-sku]` locators

- **Where:** `[data-product-sku]` page-wide in `cart-page.ts`, `account-pages.ts`, `checkout-pages.ts`, `category-page.ts`; `lineItem(sku)` copy-pasted 3 times
- **Problem:** Unscoped and duplicated.
- **What to do:** Scope to each list container; one shared helper.

### ⬜ R4.8 · P2 · Duplicated e2e helpers

- **Where:** Duplicated e2e helpers: `signIn` + `waitForURL` (organizations-menu, cart-merge), ship-to-test-address (3 checkout specs), pick saved address (2), `addConfiguration` (2), `openDraft`/`openFrom` + "open then openPage" (4 files), `saveAndWaitForToast` (4 places), toolbar enabled/disabled checks (7 places)
- **Problem:** Duplicated in specs.
- **What to do:** `SignInPage.signIn(credentials)` that waits; checkout helpers in `checkout-support.ts`; `ProductPage.configure`; `PageBuilderShell.openPage(name, route)`, `PageDetailsBlade.save()`; `BladeToolbar` enabled/disabled locators.

### ⬜ R4.9 · P2 · `networkidle` waits

- **Where:** `tests/e2e/backend/page-builder/page-status.spec.ts:234`, `search-and-validation.spec.ts:128,154`
- **Problem:** `waitForLoadState("networkidle")` after publish/save.
- **What to do:** Wait for the response, toast or badge.

### ⬜ R4.10 · P2 · Add-to-cart variants do not wait for the mutation

- **Where:** `tests/e2e/frontend/catalog/category.spec.ts:150-151,205-206`
- **Problem:** Add-to-cart-button variants don't wait for the mutation (stepper variants do).
- **What to do:** `Promise.all([waitForResponse, click])`.

### ⬜ R4.11 · P3 · Mixed wait styles

- **Where:** `pages/backend/shell/controls.ts:3,34,58`, `pages/backend/shell/controls.ts:24,178-185`, `product-configuration.ts:39`
- **Problem:** Mixed wait styles (`expect` vs `waitFor`) in page objects; `getAttribute("class") ?? ""`; `AppMenu.counter` returns 0 for a missing badge (a broken badge "matches" an empty list).
- **What to do:** One wait style; class checks via locators; counter returns `undefined`/throws.

### ⬜ R4.12 · P3 · Page-object naming and style

- **Where:** Naming/style: `ProductPage.addToCartButton` is a `Locator` while elsewhere a component; `okButton` vs `confirmButton`; `dropdownButton` vs `toggle`; modal constructors take `Page` or a root; duplicated `navigate`/`clickOutside` in two layouts; `CartPage.shippingCostLabel` duplicates the layout's; `title='Add to cart'` selectors depend on UI language
- **Problem:** Inconsistent.
- **What to do:** Align names and constructor convention; common base layout; `data-test-id` for cart buttons (request from frontend if missing).

### ⬜ R4.13 · P3 · Unused page-object members

- **Where:** Unused page-object members (about 35), e.g. `BladeToolbar.itemIds`, `Blade.label`, `Card.title/body`, `ConfirmationPopup.cancel`, `ListToolbar.refresh`, `Chip.textLabel/closeButton`, `TopHeader.signInLink/signUpLink`, `AccountMenu.signOutButton`, `CheckoutFlow.clickOutside`, exported `MENU_ITEM_FOR_ROUTE`
- **Problem:** Dead code.
- **What to do:** Remove, or keep deliberately when a planned test uses it.

### ⬜ R4.14 · P3 · `fillIfGiven`, `force` clicks, loose mutation matching

- **Where:** `pages/frontend/components/address-form.ts:73-77`, `payment-details-section.ts:19`, `graphql-traffic.ts:12-18`
- **Problem:** `fillIfGiven` skips `""`; `uncheck({ force: true })`; `isGraphqlMutation("")` matches any mutation and tests pass loose fragments (`"cart"`, `"wishlist"`).
- **What to do:** `!== undefined`; click the visible label; prefer `isGraphqlOperation(name)`.

---

## 5. API clients

### ⬜ R5.1 · P2 · Four different not-found conventions

- **Where:** 20+ clients in `api/rest/clients`
- **Problem:** Four different "not found" conventions (404, `null` body, empty text, 204); `promotions-client.ts` mixes two in one class.
- **What to do:** One `HttpResponse` helper (e.g. `jsonOrUndefined<T>()`) used by every `find*`.

### ⬜ R5.2 · P2 · `SecurityResult` returned without checking `succeeded`

- **Where:** `users-client.ts:28-93`, `roles-client.ts:24-26`
- **Problem:** `SecurityResult` returned without checking `succeeded`; the check is copy-pasted in arrange helpers and specs.
- **What to do:** Shared `expectSucceeded(result, label)`; keep raw methods for negative tests.

### ⬜ R5.3 · P2 · Unchecked `json<T>()` casts

- **Where:** `api/http/http-response.ts:51-53` + all clients
- **Problem:** `json<T>()` is an unchecked cast; only 2 clients validate with a schema; `requireFields` checks a few fields. Repeated `(results ?? []).map(requireFields)` and `requireFields(json(), FIELDS, label)` in every client.
- **What to do:** Shared helpers `requireJson(response, fields, label)` / `requireResults(...)`; decide whether `json()` returns `unknown`.

### ⬜ R5.4 · P2 · Inconsistent search result shapes

- **Where:** `orders-client.ts:86-89`, `platform-client.ts:54-63`, `notifications-client.ts:17-20`
- **Problem:** Some `search*` return the raw result unvalidated, others validated arrays.
- **What to do:** One shape for all.

### ⬜ R5.5 · P2 · Token refresh has no in-flight deduplication

- **Where:** `api/auth/token-manager.ts:29-68`
- **Problem:** No in-flight deduplication: parallel requests near expiry each refresh or sign in.
- **What to do:** Cache the pending `Promise<AuthToken>` per session.

### ⬜ R5.6 · P3 · Create/update verb names

- **Where:** Create/update verbs: `saveCatalog`/`updateCatalog`, `saveCategory`, `RolesClient.save` (PUT that creates), `saveCoupons` (POST `/add`), `saveEmployees` vs `createMany`
- **Problem:** Inconsistent names.
- **What to do:** `create` = POST, `update` = PUT, `save` only for real upserts.

### ⬜ R5.7 · P3 · Delete arity and factory names

- **Where:** Delete arity (single id vs arrays), `remove`/`removeMany` vs `delete`; "new template" factories (`getNew`, `getNewCategory`, `getNewAssignment`, `newPayment`, `newPublication`)
- **Problem:** Inconsistent.
- **What to do:** `delete(ids: readonly string[])`; one `new…()` pattern.

### ⬜ R5.8 · P3 · Rename `STOREFRONT_*` in `browser-sessions.ts`

- **Where:** `browser-sessions.ts:15-16,42-48,69-76`
- **Problem:** `STOREFRONT_*` / `storefront*` names break the "frontend" terminology.
- **What to do:** Rename to `FRONTEND_*` / `frontend*`.

### ⬜ R5.9 · P3 · Token-manager edge cases

- **Where:** `api/auth/token-manager.ts:31-32,50-54,70-78`, `browser-sessions.ts:27`
- **Problem:** Replaced token not revoked; `signOutAll` fails on the first error; expired tokens refreshed just to revoke them; cookie cache keyed by username only.
- **What to do:** Revoke replaced; `allSettled` + `AggregateError`; skip refresh on sign-out; key cookies by username + password.

### ⬜ R5.10 · P3 · HTTP client dead code and body checks

- **Where:** `api/http/http-client.ts:53-75`, `http-error.ts`, `graphql-error.ts:29-32`
- **Problem:** `patch()` and `header()` unused; `json`/`form`/`multipart` can be combined; header case not normalised; `HttpError` has no `method`/`url`; GraphQL error text omits `extensions.code`.
- **What to do:** Remove dead members; reject combined bodies; normalise headers; add fields and code.

### ⬜ R5.11 · P3 · Client consistency

- **Where:** `pricing-client.ts:48,133,146` untyped `QueryParams` criteria; `dynamic-content-client.ts` `protected` fields and in-client `*_FIELDS`; `oauth-apps-client.ts` and `notifications.ts` skip the `FIELDS`/`WithRequired` pattern; mutable `T[]` parameters (10 clients); path literals inline in `customers`/`platform` clients; mixed relative and alias imports
- **Problem:** Inconsistent.
- **What to do:** Align with the common client pattern.

### ⬜ R5.12 · P3 · Dead types

- **Where:** Unused: `OrdersClient.getChanges`, `MemberSearchResult`, `DynamicContent*SearchResult`, `ProductAsset`, `LockMembershipRequest` (use it), duplicate re-exports of `ModuleDescriptorData` and `ChangeLogSearchResult`, `QuantityControl`/`RangeFilterType` types
- **Problem:** Dead code.
- **What to do:** Remove or use.

---

## 6. Dataset and fixtures

### ⬜ R6.1 · P2 · `requireFields` should accept `null`

- **Where:** `core/required-fields.ts:4`
- **Problem:** Accepts `T | undefined` only, which causes `?? undefined` before every GraphQL result (13+ places). `""` passes as present.
- **What to do:** Accept `T | null | undefined`; optional non-empty-string check; remove all `?? undefined`.

### ⬜ R6.2 · P2 · Organization memberships seeded as `optional`

- **Where:** `dataset/manifest.json:165-172`
- **Problem:** `organizationMemberships` is `optional`, so every failure is only a warning.
- **What to do:** Make it idempotent (find → create) and remove `optional`.

### ⬜ R6.3 · P2 · Seeder errors lack item id and body

- **Where:** `dataset/seeder.ts:49-90`
- **Problem:** Failure messages keep only `METHOD url → status`: no item id, no response body, even for optional failures.
- **What to do:** Include item id and body.

### ⬜ R6.4 · P2 · Browser tests always resolve customer-account dependencies

- **Where:** `fixtures/browser.fixture.ts:34`, `customer-account.fixture.ts:53-67`
- **Problem:** Every browser test resolves `browserCustomerAccount` and therefore the platform admin client, cleanup stack, token manager and dataset, even when it returns `undefined`.
- **What to do:** Resolve the customer account only in `customer-account` mode.

### ⬜ R6.5 · P2 · Cleanup fixture ordering

- **Where:** `fixtures/cleanup.fixture.ts:10`
- **Problem:** Only `httpClient` is guaranteed to outlive the cleanup stack; cleanups through `platformAdminHttpClient` would break if a test requested the fixtures in a different order.
- **What to do:** Also depend on `anonymousHttpClient`; then `httpClient` dependency can go.

### ⬜ R6.6 · P2 · `STORE_ID` placeholder

- **Where:** `dataset/data/manifest.json:99`
- **Problem:** Only one place uses `${ENV:STORE_ID}` while `store-acme` is hard-coded 366 times; `STORE_ID` must be `store-acme` anyway.
- **What to do:** Hard-code it there too, and document that `STORE_ID` must match the dataset.

### ⬜ R6.7 · P2 · Seed setup duplication and timeouts

- **Where:** `tests/setup/seed.setup.ts:10-28`
- **Problem:** Duplicates the pages module id and re-fetches installed modules; "apply page statuses" is skipped when only `pagesContent` is re-seeded; the second test keeps the default 30 s timeout.
- **What to do:** Derive from the manifest and `resolveSeedScope`; include `pagesContent`; set a timeout on the `seed` project.

### ⬜ R6.8 · P3 · Dataset typing

- **Where:** `dataset/dataset.ts:27-51`, `frontend-context.ts:28,48-56`, `stock.ts:16,46`, `manifest.ts:37`, `seed-scope.ts:22-34`
- **Problem:** Casts of untyped dataset JSON spread across files; duplicated user lookup; `?? ""` fallbacks.
- **What to do:** Typed dataset accessors per manifest entity; one `findUser`; type guard for manifest names.

### ⬜ R6.9 · P3 · Shared seeded-constants module

- **Where:** New module
- **Problem:** Seeded ids and usernames repeated across tests (R3.9, R3.10).
- **What to do:** `dataset/seeded.ts` (or constants in builders) with seeded products, configurable product + options, users, organization; derive `SEEDED_CATALOG_ID` from the dataset store.

### ⬜ R6.10 · P3 · `getStoreContext`

- **Where:** `dataset/frontend-context.ts:21-26`, `fixtures/customer-account.fixture.ts:130`
- **Problem:** `getFrontendContext` needs an anonymous id even for signed-in users; the fixture calls it with `undefined` just to get the store part.
- **What to do:** Export `getStoreContext(dataset, storeId)`.

### ⬜ R6.11 · P3 · Cart helper duplication

- **Where:** `dataset/arrange/cart.ts:33-64,79,112-117`, `fixtures/cart.fixture.ts:32`
- **Problem:** `arrangeCart` and `arrangeDefaultCart` nearly identical; `withItems` registers the same cart removal twice; repeated shopper label fallbacks.
- **What to do:** One private helper; single registration; `describeShopper(context)`.

### ⬜ R6.12 · P3 · Fixture simplification

- **Where:** `fixtures/customer-account.fixture.ts:36-114`, `page-builder.fixture.ts:4`, `index.ts:18`, `api.fixture.ts:50-71`
- **Problem:** Nine dependencies listed twice; unused option `customerAccountOrganizationId`; page-builder fixture extends the shopper chain for nothing; redundant merges; two identical anonymous contexts per test.
- **What to do:** Simplify as described.

### ⬜ R6.13 · P3 · Builder fixes

- **Where:** Builders: `completeness.ts:13` sends the catalog id as name; `product-configuration.ts:9-16` silently skips invalid sections; three different test-address builders; `newNamedContent` unused; `ORDER_CURRENCY`/`PRICELIST_CURRENCY` duplicate "USD"; `newEmployee` repeats `newContact`; `toMemberAddressInput` copies 21 fields by hand; `searchProducts` stops at 100 silently
- **Problem:** Small correctness and duplication issues.
- **What to do:** Fix individually.

---

## 7. GraphQL documents

### ⬜ R7.1 · P2 · Unused operations

- **Where:** `operations/contact/delete-contact`, `contact/get-contact`, `user/delete-users` (+ fragment `identity-result`), `order/orders`, `quote/cancel-quote-request`, `shopping-list/add-bulk-item-to-shopping-list`
- **Problem:** Operations generated but never used. `cancelQuoteRequest`, own `orders` and bulk-add to a list are real coverage gaps.
- **What to do:** Add tests for the gaps (quote cancel, my orders, bulk add), delete the rest.

### ⬜ R7.2 · P2 · `ValidationError` fragment

- **Where:** 8 places (`cart`, `line-item` fragments; `get-cart-validation*`, `get-cart-line-validation`, `add-bulk-items-cart` operations)
- **Problem:** The validation-error selection is written out 8 times with different fields.
- **What to do:** `ValidationError` fragment; drop `GetCartLineValidation` (subset of `GetCartValidation`).

### ⬜ R7.3 · P2 · Over-fetching

- **Where:** `fragments/configuration-line-item.graphql:5-7`, `fragments/cart-with-list.graphql:5-7`, `contact/lock-` / `unlock-organization-contact`
- **Problem:** Over-fetching: full `...Product` per configuration option (only `id` is read); full `...Cart` for the saved-for-later list; full `...Contact` from lock/unlock (then a second query reads the status).
- **What to do:** Slim selections; assert the lock status from the mutation result.

### ⬜ R7.4 · P3 · Fields never read

- **Where:** `quote` (totals), `product` (vendor), `store-info` (settings), `user` (2 fields), pickup fragments (`workingHours`, `geoLocation`)
- **Problem:** Fields never read.
- **What to do:** Remove or move to detail fragments.

### ⬜ R7.5 · P3 · Operation naming

- **Where:** Operation names
- **Problem:** `Get` prefix used in half of the operations; shopping-list operations named differently from the xAPI fields (`DeleteShoppingList` → `removeWishlist`); `GetOrganizations` reads the current user's organizations.
- **What to do:** One naming rule; rename accordingly (file names follow).

### ⬜ R7.6 · P3 · Address fragment names

- **Where:** `pickup-address` / `pickup-location-address`, `cart-address` / `member-address` fragments
- **Problem:** Identical field lists on different types with unclear names.
- **What to do:** Names that show the pairing.

### ⬜ R7.7 · P3 · `...Role` in roles-in-organization

- **Where:** `contact/get-contact-roles-in-organization.graphql:3-6`
- **Problem:** Inline `id name` instead of `...Role`.
- **What to do:** Use the fragment.

---

## 8. Configuration, tooling, CI, docs

### ⬜ R8.1 · P1 · PR quality job

- **Where:** repo root
- **Problem:** **No CI pipeline** (the old workflows were removed).
- **What to do:** Per R0.3: PR job (`npm ci`, `biome ci .`, `npm run typecheck`).

### ✅ R8.2 · P1 · Automated test run

- **Where:** `.github/workflows/auto-tests.yml`
- **Problem:** No automated test run.
- **What to do:** **Done (manual runs):** `workflow_dispatch` calls the reusable `VirtoCommerce/.github` Playwright workflow, which starts the Docker stack, writes `.env` from a secret, installs Chromium, runs the `seed` project and re-indexing, runs the chosen suites with list/JUnit/JSON/Allure reporters, publishes a failed-tests summary and uploads `report/` and `test-results/`. Nightly runs: R8.20.

### ⬜ R8.3 · P2 · Destructive-test runner

- **Where:** repo root
- **Problem:** Destructive tests have no safe runner.
- **What to do:** Opt-in job and a `test:destructive` script with `--workers=1`.

### ⬜ R8.4 · P2 · Local compose file

- **Where:** repo root
- **Problem:** No committed way to start a platform with the right modules **locally**.
- **What to do:** CI is covered by the reusable workflow's `docker-env-full` action (once R8.17 is fixed). Remaining: a local `docker-compose.yml` (or instructions pointing at the shared one) with Elasticsearch given enough memory (at least 1 GB heap / 2 GB container); link from README Prerequisites.

### ⬜ R8.5 · P1 · `forbidOnly`

- **Where:** `playwright.config.ts:27`
- **Problem:** No `forbidOnly`: a committed `test.only` silently shrinks a CI run.
- **What to do:** `forbidOnly: Boolean(process.env["CI"])`; make `noFocusedTests` a Biome error.

### ⬜ R8.6 · P2 · API project timeouts

- **Where:** `playwright.config.ts:42-49`
- **Problem:** API projects use the default 30 s test timeout, equal to `REQUEST_TIMEOUT_MS`, so one slow request or sign-in retry exhausts the test.
- **What to do:** Explicit 60–90 s timeout for `restapi`/`graphql` (or derived from `requestTimeoutMs`).

### ⬜ R8.7 · P3 · Local Allure cleanup

- **Where:** `package.json`
- **Problem:** `allure-results/` is never cleaned locally, so `npm run report` mixes runs. (CI reporters are covered: the reusable action passes `--reporter=list,junit,json,allure-playwright` and starts from a clean checkout.)
- **What to do:** `clean` script / pre-test cleanup.

### ⬜ R8.8 · P2 · Unseeded-platform check locally

- **Where:** `playwright.config.ts:36-66`, README
- **Problem:** Locally, nothing detects an unseeded platform, and a bare `npx playwright test` runs `seed` alongside the tests. (CI seeds before the suites.)
- **What to do:** Exclude `seed` from bare runs; a cheap "is the dataset seeded" check with a clear message.

### ⬜ R8.9 · P2 · Env validation

- **Where:** `core/env.ts:20-27`, `.env.example`
- **Problem:** Empty `ADMIN_PASSWORD=` etc. pass validation; `PAGE_SIZE` is unused (and `.env.example` says 50 while the default is 20); `SEED_ONLY` validated only in the seed test; `.env.example` has no trailing newline.
- **What to do:** `min(1)`; remove `PAGE_SIZE`; validate `SEED_ONLY` in the schema; add commented `SEED_ONLY` line.

### ⬜ R8.10 · P2 · `ci` lint script

- **Where:** `package.json`
- **Problem:** No read-only lint for CI (`check` rewrites, `lint` passes on warnings).
- **What to do:** `"ci": "biome ci ."`; errors for `noFocusedTests`, `noUnusedImports`.

### ⬜ R8.11 · P2 · VS Code formatter

- **Where:** `.vscode/settings.json:12-14`
- **Problem:** TypeScript files are formatted by the built-in formatter on save, not Biome, which fights the pre-commit hook.
- **What to do:** `biomejs.biome` as TS formatter; commit `.vscode/extensions.json` (Biome, Playwright).

### ⬜ R8.12 · P2 · Codegen env

- **Where:** `codegen-graphql.ts:11`
- **Problem:** GraphQL codegen validates the full env (passwords etc.), REST codegen only needs `BACKEND_BASE_URL`; neither honours `VERIFY_SSL=false`.
- **What to do:** Read only `BACKEND_BASE_URL`; document or handle self-signed certificates.

### ⬜ R8.13 · P3 · `package.json` and `tsconfig`

- **Where:** `package.json`, `tsconfig.json`
- **Problem:** No `"private": true`; `@types/node` 26 vs `engines` 22; no `.nvmrc`; pre-commit uses `npx`; no `include` in tsconfig; `verbatimModuleSyntax` not enabled.
- **What to do:** Add/adjust; check `verbatimModuleSyntax` with the CJS/ESM mix.

### ⬜ R8.14 · P3 · Biome restrictions

- **Where:** `biome/layers.json`, `biome.json`
- **Problem:** Pages layer does not forbid `expect`/`test` from `@playwright/test`; core may import `@playwright/test`; no `vcs.defaultBranch`.
- **What to do:** Add restrictions; `defaultBranch: "dev"`.

### ⬜ R8.15 · P3 · `.gitignore`

- **Where:** `.gitignore`
- **Problem:** `.env.*`, `*.local.*`, probe/scratch folders, `*.tsbuildinfo`, IDE/OS files not ignored.
- **What to do:** Extend (keep `!.env.example`).

### ⬜ R8.16 · P3 · README and bug-report doc

- **Where:** `README.md`, `BUG-concurrent-token-sign-in-500.md`
- **Problem:** Hard-coded test counts will go stale; no note that `npm test` needs a seeded platform; project structure omits some dataset files; destructive commands lack `--workers=1`; bug report has no tracker key and its code block starts with a comment. (A CI section now exists.)
- **What to do:** Update README; file the bug, add the key, move to `docs/known-issues/`. When R8.18 is done, replace the `TS_ENV_SECRET_NAME` placeholder in the README CI section with the real secret name.

### ✅ R8.17 · P1 · `backend-packages.json` for CI

- **Where:** `.github/workflows/auto-tests.yml:38`, `backend-packages.json`
- **Problem:** **Blocker for CI:** `customPackagesJsonUrl` pointed at `backend-packages.json`, which was deleted in the `dev` merge.
- **What to do:** **Done:** restored from `dev` (platform image 3.1069.0, 86 modules, PageBuilder 3.1029.0). It contains all 13 modules the dataset manifest seeds, plus the xAPI modules and Elasticsearch 8. Referenced from README (Prerequisites, Project structure, Continuous integration). Then bumped to edge: platform image 3.1074.0 and the newest release of every module from the edge feed (`vc-modules/modules_v3.json`), 27 modules changed; this matches the local platform the tests were verified against.

### ⬜ R8.18 · P1 · Env-file secret for CI

- **Where:** `.github/workflows/auto-tests.yml:44`, repository secrets
- **Problem:** `testSecretEnvFile` uses the placeholder secret `TS_ENV_SECRET_NAME`.
- **What to do:** Create the secret with the full `.env` content for CI: `STORE_ID`, `ADMIN_PASSWORD`, `USERS_PASSWORD`, `GOOGLE_MAPS_API_KEY` (required in practice, see R1.1), `VERIFY_SSL`, optionally `E2E_WORKERS`; the action overrides `BACKEND_BASE_URL`, `FRONTEND_BASE_URL` and `ADMIN_USERNAME`. Then reference the real secret name.

### ⬜ R8.19 · P2 · Default database matrix runs everything three times

- **Where:** `.github/workflows/auto-tests.yml:31-45`
- **Problem:** The reusable workflow defaults to `databaseProviders: ["sqlserver","mysql","postgres"]`, so every manual run executes the whole suite **three times**.
- **What to do:** Pass `databaseProviders: '["postgres"]'` by default and expose it as an input for full-matrix runs.

### ⬜ R8.20 · P2 · Nightly schedule

- **Where:** `.github/workflows/auto-tests.yml:4`
- **Problem:** Only `workflow_dispatch`: no scheduled run.
- **What to do:** Add a nightly `schedule` (with the default inputs) once R8.17–R8.19 are done.

### ⬜ R8.21 · P2 · Reusable workflow pinned to a feature branch

- **Where:** `.github/workflows/auto-tests.yml:32`
- **Problem:** The reusable workflow (and its `run-playwright-tests` action) is pinned to the feature branch `vcst-6033-playwright-workflow`, so any push there changes our CI.
- **What to do:** Switch to the release tag once VCST-6033 is released; the TODO comment in the file can then go.

### ⬜ R8.22 · P3 · `workers` input not exposed

- **Where:** `.github/workflows/auto-tests.yml`
- **Problem:** The reusable workflow's `workers` input is not exposed, so the worker count on CI can only change through `E2E_WORKERS` in the env secret. Destructive tests can only be enabled by editing that secret.
- **What to do:** Expose `workers` as a dispatch input (it maps to `--workers`, which only lowers parallelism); for destructive runs see R8.3.
