# Refinements

Review of the whole repository (core, api, dataset, fixtures, pages, all test projects, tooling, docs), done on 2026-09-30 on branch `vcst-6033`. Each item names where the problem is, what to do, and how to know it is done.

## How to use this file

- Tick `[x]` when an item is merged; add the commit or PR in the **Done in** column if you like.
- `[-]` means **won't do**; write the reason next to it.
- Priority: **P1** fix first (wrong results, data leaks, broken setups), **P2** reliability and maintainability, **P3** polish and consistency.
- Items marked **decision** need a choice before work starts; they are collected in [Section 0](#0-decisions-needed).
- Line numbers are from the review date; search by symbol name if they have moved.

## Progress

| Section | Items | Done |
|---|---|---|
| 0. Decisions needed | 6 | 0 |
| 1. Correctness | 10 | 0 |
| 2. Isolation and cleanup | 12 | 0 |
| 3. Test quality | 14 | 0 |
| 4. Page objects and e2e | 14 | 0 |
| 5. API clients | 12 | 0 |
| 6. Dataset and fixtures | 13 | 0 |
| 7. GraphQL documents | 7 | 0 |
| 8. Configuration, tooling, CI, docs | 16 | 0 |

## Suggested order of work

1. **Section 0 decisions**, so nothing is blocked later.
2. **All P1 items** (sections 1 and 2): they make runs trustworthy and stop leaking data.
3. **CI pipeline (R8.1–R8.3)**, so every later refactoring is checked automatically.
4. **Shared helpers first, then their callers:** R5.1–R5.3 (response helpers) before R5.4+; R6.9 (seeded constants) before the duplicate-removal items in sections 3 and 4.
5. The remaining P2, then P3, section by section.

---

## 0. Decisions needed

| | ID | Decision | Options | Notes |
|---|---|---|---|---|
| [ ] | R0.1 | Sign-in retry for the concurrent same-user `/connect/token` 500 | a) longer exponential backoff with jitter (6 attempts, up to ~11 s); b) sign in once per run and share the token between workers | Bug report: [BUG-concurrent-token-sign-in-500.md](BUG-concurrent-token-sign-in-500.md). Current: 3 attempts ~0.2–0.6 s (`api/auth/token-auth-client.ts:68-73`). |
| [ ] | R0.2 | HTTP logging safety features that are expected but **not in the code**: secret redaction, `Secret` env values, `onExchange` listener, redacted network-error call logs | a) implement them; b) confirm they were dropped | Earlier design notes describe them as agreed; `api/http/http-client.ts` calls `context.fetch` directly and nothing redacts `Authorization` headers or passwords. |
| [ ] | R0.3 | Scope of the CI pipeline | quality job on every PR; e2e/API job manual + nightly; destructive tests opt-in | Blocks R8.1–R8.3. Needs a way to start the platform with the right modules (R8.4). |
| [ ] | R0.4 | Where platform-wide settings tests run | a) one serial project (`workers: 1`) for everything that changes global settings; b) keep them in their files but make restore undo only the test's own change | See R2.1. |
| [ ] | R0.5 | Tracking of known product issues | Every `test.fail(true, …)` and the `test.fixme` gets a tracker key in its reason | 6 `test.fail` (page builder toasts, duplicate permalink, verbatim permalinks, store without name) and 1 `fixme` (theme zip). |
| [ ] | R0.6 | Retries on CI | `retries: 1` on CI only, or none | Retries hide flakiness; they also stop a single slow-environment timeout from failing a nightly run. |

---

## 1. Correctness

Things that make results wrong or setups fail.

| | ID | P | Where | Problem | What to do | Done when |
|---|---|---|---|---|---|---|
| [ ] | R1.1 | P1 | `core/env.ts:32`, `dataset/data/stores/acme_electronics.json:81`, `core/interpolate.ts:16` | `GOOGLE_MAPS_API_KEY` is declared optional, but the store data interpolates it and interpolation throws when it is missing, so an unset key breaks **every** test that loads the dataset. | Either make it required (`string().min(1)`), or support an empty default in interpolation; align README and `.env.example`. | Unset key: either a clear start-up error or tests run. |
| [ ] | R1.2 | P1 | `dataset/seeder.ts:76` | Seeding only checks the HTTP status. User creation answers `200 {succeeded:false}` (existing user, rejected password), so users are "seeded" without error and a changed `USERS_PASSWORD` is never applied. | Check `succeeded` for security endpoints (manifest flag or dedicated user upsert: find → create / reset password). | Re-seed with a new password actually changes it; a rejected password fails the seed. |
| [ ] | R1.3 | P1 | `tests/graphql/cart/cart-validation.spec.ts:232-260` | `readCartValidation` returns `undefined` errors when the cart is missing, and `expectNoQuantityError(undefined)` passes: five "no error" tests can pass vacuously. | `requireFields` on the returned cart before reading errors. | The tests fail when the cart is null. |
| [ ] | R1.4 | P1 | `dataset/seeder.ts:40-46`, `dataset/seed-requests.ts:13` | An entity with no items still sends a request; for array payloads that is `PUT []`, which can wipe e.g. store aggregation properties. | `continue` after the "no items" warning. | Empty entity folder sends nothing. |
| [ ] | R1.5 | P2 | `api/graphql/graphql-client.ts:49` | For an unnamed document the placeholder `"(anonymous)"` is sent as `operationName`, which the server rejects. (All current documents are named.) | Send `operationName` only when found; keep the placeholder for messages. | Unnamed document executes. |
| [ ] | R1.6 | P2 | `api/graphql/graphql-client.ts:54-59` | The body is parsed before the status is checked, so a 502 HTML page or empty 401 fails with "not valid JSON" instead of the HTTP error. | Check `!response.ok` first, parse leniently. | 502 shows the status error. |
| [ ] | R1.7 | P2 | `tests/graphql/orders/orders.spec.ts:51-53` | `orders[0]` is called "newest organization order" but the query has no sort. | Pass `sort: "createdDate:desc"`. | Deterministic order. |
| [ ] | R1.8 | P2 | `tests/restapi/search/indexes.spec.ts:59-73` | "cancel an indexation" asserts `completed === true`; a one-document indexation finishes on its own, so the test passes whether cancel works or not. | Cancel a long job and assert an aborted/cancelled state, or drop the test. | Test fails if cancel is a no-op. |
| [ ] | R1.9 | P2 | `tests/restapi/orders/orders.spec.ts:101-103` | Tautology: `typeof enabled === "boolean"`. | Compare with the known configuration, or remove. | Assertion can fail. |
| [ ] | R1.10 | P2 | `dataset/stock.ts:12-27` | `getStockQuantity` throws "missing" for a center that has an inventory record with 0 stock, because zero-stock records are filtered out first. | Look up the raw record; return 0 or throw "not stocked". | Zero-stock center gives 0 or a clear error. |

---

## 2. Isolation and cleanup

Data leaks and interference between parallel tests.

| | ID | P | Where | Problem | What to do | Done when |
|---|---|---|---|---|---|---|
| [ ] | R2.1 | P1 | `tests/restapi/platform/settings.spec.ts:65-91`, `content/validation.spec.ts:79-91`, `content/files.spec.ts:90-97`, `catalog-personalization/tags.spec.ts:40-53,205-213`, `catalog/products.spec.ts:159-182`, `search/indexes.spec.ts`, `platform/system.spec.ts:62-73` | Several files change the same global platform settings (file-extension blacklist, indexing jobs, member groups, tag inheritance, editorial review types) and restore a snapshot; files run in parallel, so restores overwrite each other. `files.spec` relies on the blacklist without arranging it. `mode: "default"` in three files does not help (the race is between files). | Per decision R0.4. Also: `files.spec` arranges its own blacklist entry; remove the three `test.describe.configure({ mode: "default" })`. | Global-settings tests cannot overlap; `files.spec` passes alone. |
| [ ] | R2.2 | P1 | `tests/e2e/frontend/catalog/category.spec.ts:118-206`, `catalog/product-configuration.spec.ts:23-153`, `wishlists/wishlist-items.spec.ts:122`, `cart/cart-merge.spec.ts:51-79`; `fixtures/shopper.fixture.ts:32` | Tests that add to the cart only through the UI do not request `shopper`, so the default cart is never removed. | Register default-cart removal inside `storageState` when `app === "frontend"` (it already knows the credentials / anonymous id), so every frontend test cleans up without asking. Do **not** make `storageState` depend on `frontendContext` (breaks the backend project, where `user` is the platform admin). | No carts left for test users after a frontend run. |
| [ ] | R2.3 | P1 | `tests/graphql/cart/cart-save-for-later.spec.ts:20-56` | Uses the seeded `acme_store_maintainer_1`; the saved-for-later list is one per user and the cleanup deletes the whole list; exact `toEqual` breaks if anything else saved items. | Use `customerAccount`, as the second describe in the file does. | No seeded user's list is modified. |
| [ ] | R2.4 | P1 | `tests/e2e/frontend/checkout/checkout-order.spec.ts:45-54` | Order cleanup is registered only after the assertion and only if a number was found: a timeout leaks the order. | Capture the order from the create-order GraphQL response (or register cleanup by order number before asserting), `requireFields` instead of `if`. | Failed run leaves no order. |
| [ ] | R2.5 | P2 | `contacts/contacts.spec.ts:98-132`, `contacts/employees.spec.ts:56-77`, `contacts/members.spec.ts:75-146`, `contacts/organizations.spec.ts:58-166`, `marketing/dynamic-content.spec.ts:123-126` | `Promise.all` creates two entities and registers cleanup only after both succeed; if one fails, the other leaks. | Register cleanup by draft id first (builders set ids), then create. | Pattern gone from REST specs. |
| [ ] | R2.6 | P2 | `tests/restapi/marketing/promotions.spec.ts:110-170` | Coupon cleanup registered after assertions / inside an `assert:` step. | Register by code before `saveCoupons` (find-then-delete). | — |
| [ ] | R2.7 | P2 | `dataset/arrange/security.ts:29-32`, `dataset/arrange/page-builder.ts:11-12` | `arrangeApiKey` and `arrangePage` register cleanup after the create/validation, so a failing check leaks. | Register first, find by key value / unique name inside the cleanup. | — |
| [ ] | R2.8 | P2 | `dataset/arrange/contact.ts:17-42` | `saveMemberAddress(es)` registers no cleanup; with a seeded organization (option `customerAccountOrganizationId`) test addresses stay forever. | Take `cleanupStack`, register removal, rename to `arrangeMemberAddress(es)`. | — |
| [ ] | R2.9 | P2 | `dataset/arrange/customer-account.ts:62-69`, `fixtures/customer-account.fixture.ts:124` | Fresh accounts stay in the worker token cache after the user is deleted; `signOutAll` later refreshes/revokes tokens of deleted users. | Push `tokenManager.signOut(username, storeId)` to `cleanupStack` right after the user is created. | Token cache holds no deleted users at worker end. |
| [ ] | R2.10 | P2 | `dataset/arrange/customer-account.ts:80-91` | `addOrganizationMembership` has no find-or-create guard and no role, unlike `arrangeCustomerAccount`. | Shared `ensureMembership(userId, organizationId, role)`. | — |
| [ ] | R2.11 | P2 | `tests/restapi/platform/notifications.spec.ts:28-36` | "mark all as read" then expects `newCount === 0` for the shared admin while other files create notifications. | Run as a fresh user. | — |
| [ ] | R2.12 | P3 | `tests/restapi/platform/assets.spec.ts:55-65` | Local-storage upload leaves a file behind (the platform cannot delete local-storage uploads). | Document as a known limitation in the test (unique name already), or skip on shared environments. | Decision recorded. |

---

## 3. Test quality

Weak assertions, duplicates, hard-coded data.

| | ID | P | Where | Problem | What to do |
|---|---|---|---|---|---|
| [ ] | R3.1 | P1 | `tests/restapi/catalog-publishing/channels.spec.ts:132-141`, `tests/restapi/platform/user-passwords.spec.ts:79-84` | Tests without any assertion ("save evaluated product completeness", "send a verification email"). | Assert the stored result / returned status. |
| [ ] | R3.2 | P2 | REST: `channels.spec.ts:104-108,122-128`, `tags.spec.ts:32-37,189-191`, `orders.spec.ts:78-80,125-127`, `notifications.spec.ts:22-25`, `changelog.spec.ts:22-46`, `system.spec.ts:27-29,70-72`, `health.spec.ts:21`, `authorization.spec.ts:47`, `assignments.spec.ts:72`, `prices.spec.ts:156-157`, `indexes.spec.ts:38,55`, `organizations.spec.ts:152` | Assertions that pass on empty or arbitrary data (`length > 0` on shared data, `expect.any(...)`, `Array.isArray`, `every` on possibly empty list, job started but not finished). | Assert the specific arranged entity / exact value; wait for jobs to finish. |
| [ ] | R3.3 | P2 | GraphQL: `product-variations.spec.ts:40-53`, `page-context.spec.ts:54-66`, `cart-validation.spec.ts:263-271`, `cart-promotions.spec.ts:44-66`, `current-addresses.spec.ts:106,126`, `contact-search.spec.ts:31,41` | Same kind: comparisons that pass on empty results, an assertion helper that returns early without asserting, `>=` where exact counts are known. | Assert non-empty, exact counts, specific gift/discount values. |
| [ ] | R3.4 | P2 | `tests/graphql/cart/cart-lifecycle.spec.ts:28-60` | "get the cart of …" never calls the `cart` query. | Arrange with `arrangeCart`, act with `GetCartDocument`. |
| [ ] | R3.5 | P2 | REST duplicates: `catalog/assets.spec.ts` vs `platform/assets.spec.ts`; `organizations.spec.ts:112-159`; `members.spec.ts:17-59,175-188`; `stores.spec.ts:92-112`; `users.spec.ts:111-121` vs `authorization.spec.ts:20-31`; `pricelists.spec.ts:95-110` vs `prices.spec.ts:20-35,75-90`; `health.spec.ts:42-50` vs `indexes.spec.ts:21-29` | Tests repeating each other. | Keep one of each; remove combined "create, rename, delete" variants. |
| [ ] | R3.6 | P2 | GraphQL duplicates: `pickup-locations.spec.ts:276-305` (Berlin/Billund) vs `:221-250`; `page-context.spec.ts:68-92` | Same. | Merge or remove. |
| [ ] | R3.7 | P2 | `tests/restapi/catalog/assets.spec.ts:9`, `platform/assets.spec.ts:9-10` | Upload-from-URL tests download from `raw.githubusercontent.com/.../dev/`: network or rename breaks them. | Upload a local fixture first, then upload-from-URL that asset. |
| [ ] | R3.8 | P2 | e2e backend: `search-and-validation.spec.ts:131-135,161-166,95-100` | Duplicate-permalink check spins through 15 reloads when correctly rejected; special-character assertions only run `if` the page exists (vacuous); required-fields case depends on the previous loop iteration. | Assert explicitly on both outcomes; give both fields per case. |
| [ ] | R3.9 | P2 | Seeded ids repeated across specs: `laptop-acer-predator-helios-neo-16-ai` (7 REST + 3 GraphQL + 3 e2e files), `smartphone-apple-iphone-17-256gb-black` (12 GraphQL), `…-mist-blue`, `sodimm-crucial-ddr4-2400-8gb`, `smartphone-samsung-galaxy-a57-5g` (5 e2e), configurable memory option names, variation SKUs | Hard-coded in many files. | Use the shared seeded-data constants from R6.9. |
| [ ] | R3.10 | P3 | `USERNAME = "acme_store_administrator@acme.com"` + identical `test.use` in all 40 REST files; seeded usernames in GraphQL | Repeated. | Export seeded user constants (R6.9) and an `asStoreAdministrator` option or shared `test.use` value. |
| [ ] | R3.11 | P3 | REST local helpers: `arrangeRole` (roles.spec.ts:129-145), `arrangeOrder`/`orderWithLineItem` (orders.spec.ts:230-242), `createCategoryWithProduct`/`createProduct` (tags.spec.ts, products.spec.ts), settings save/restore (6 places), `newApiKey` (5 places), `/connect/token` form bodies | Helpers duplicated in specs. | Move to `dataset/arrange/*` / builders (`arrangeSettingValue`, `arrange/order.ts`, `arrangeRole`, `newApiKey`); export `TOKEN_PATH`. |
| [ ] | R3.12 | P3 | GraphQL local helpers: product configuration fetch (3 files), `Configuration-${id}` SKU (2), pickup helpers duplicated between `cart-pickup-locations` and `pickup-locations` specs, `quoteFromCart`/`registerQuoteRemoval`, invite helper, "create list + add item", manual `new GraphqlClient(await tokenManager.authorize(...))` | Duplicated. | Move to `dataset/arrange` (`quote.ts`, `pickup-location.ts`, `catalog.ts`), reuse `signInGraphqlClient`. |
| [ ] | R3.13 | P3 | `?? ""`, `?? []`, `?? 0`, `?? undefined`, `?.` hiding missing data in REST (settings, catalogs, changelog, orders, dynamic-content, promotions, assignments), GraphQL (cart-validation, pickup-locations, current-addresses, organizations-locked, contact-registration) and e2e (wishlist-items, wishlist-lists, checkout-pickup, shared-list) specs | Violates the "no fallbacks" convention. | `requireFields` / explicit assertions; see R6.1 for `null` support. |
| [ ] | R3.14 | P3 | Test naming and steps: imperative vs statement titles (REST health, seo, changelog, assets, user-lock); `act:` steps that only call arrange helpers; actions/assertions outside steps (several e2e and GraphQL specs); combined "act and assert:" steps; `orders.spec.ts:217-220` hard-codes 65 instead of `MAX_ORDER_NUMBER_LENGTH + 1` | Inconsistent. | One title style (imperative); every action in an `arrange:`/`act:`/`assert:` step. |

---

## 4. Page objects and e2e

| | ID | P | Where | Problem | What to do |
|---|---|---|---|---|---|
| [ ] | R4.1 | P1 | `pages/backend/page-builder/page-builder-shell.ts:79-100`, `pages-list-blade.ts:82-87` | `waitUntilListed`, `waitUntilCounterMatchesList`, `waitForRows` are manual `waitForTimeout` loops that **give up silently**; tests then fail later on a vague check. Callers wrap them in one-shot assertions (5 places). | Replace with `expect.poll` / `toPass` that fail with a clear message; callers assert directly. |
| [ ] | R4.2 | P2 | `pages/backend/page-builder/pages-list-blade.ts:38-43` | Search waits for any `page-builder-pages/search` response (can be a previous keyword) and casts the body with `?? 0`. | Match the request's keyword; validate the body. |
| [ ] | R4.3 | P2 | `pages/backend/page-builder/page-builder-shell.ts:45-46,57-65` | List/details blades picked by position (`first()`/`last()`); `open()` navigates twice and waits for `networkidle`. | Locate blades by title; navigate once and wait for the grid. |
| [ ] | R4.4 | P2 | `pages/backend/shell/controls.ts:101-118`, `pages/frontend/components/product-configuration.ts:43-47` | Date picker checks the new month before it renders and uses `.first()` over neighbour-month cells; closes by clicking a blade title. Configuration `expand()` does not wait for the expanded state. | Wait for the month header change; exclude off-month cells; close with `Escape`; wait for `vc-widget--collapsed` to disappear. |
| [ ] | R4.5 | P2 | `pages/frontend/pages/category-page.ts:31-50` | `scrollToProduct` is an endless loop with `catch` as control flow and a string `evaluate`. | Bounded loop or `expect.poll` over the loaded cards. |
| [ ] | R4.6 | P2 | `pages/frontend/pages/account-pages.ts:28`, `components/wishlist.ts:51-52`, `select-address-modal.ts:20-22`, `address-filters.ts:36-38`, `product-configuration.ts:51,76`, `address-form.ts:47,52` | Substring `hasText` + `.first()` (e.g. `card("list-x")` also matches `list-x-edited`); wishlist menu items page-wide `:visible`. | Use `exactText`; scope menus to the opened card. |
| [ ] | R4.7 | P2 | `[data-product-sku]` page-wide in `cart-page.ts`, `account-pages.ts`, `checkout-pages.ts`, `category-page.ts`; `lineItem(sku)` copy-pasted 3 times | Unscoped and duplicated. | Scope to each list container; one shared helper. |
| [ ] | R4.8 | P2 | Duplicated e2e helpers: `signIn` + `waitForURL` (organizations-menu, cart-merge), ship-to-test-address (3 checkout specs), pick saved address (2), `addConfiguration` (2), `openDraft`/`openFrom` + "open then openPage" (4 files), `saveAndWaitForToast` (4 places), toolbar enabled/disabled checks (7 places) | Duplicated in specs. | `SignInPage.signIn(credentials)` that waits; checkout helpers in `checkout-support.ts`; `ProductPage.configure`; `PageBuilderShell.openPage(name, route)`, `PageDetailsBlade.save()`; `BladeToolbar` enabled/disabled locators. |
| [ ] | R4.9 | P2 | `tests/e2e/backend/page-builder/page-status.spec.ts:234`, `search-and-validation.spec.ts:128,154` | `waitForLoadState("networkidle")` after publish/save. | Wait for the response, toast or badge. |
| [ ] | R4.10 | P2 | `tests/e2e/frontend/catalog/category.spec.ts:150-151,205-206` | Add-to-cart-button variants don't wait for the mutation (stepper variants do). | `Promise.all([waitForResponse, click])`. |
| [ ] | R4.11 | P3 | `pages/backend/shell/controls.ts:3,34,58`, `pages/backend/shell/controls.ts:24,178-185`, `product-configuration.ts:39` | Mixed wait styles (`expect` vs `waitFor`) in page objects; `getAttribute("class") ?? ""`; `AppMenu.counter` returns 0 for a missing badge (a broken badge "matches" an empty list). | One wait style; class checks via locators; counter returns `undefined`/throws. |
| [ ] | R4.12 | P3 | Naming/style: `ProductPage.addToCartButton` is a `Locator` while elsewhere a component; `okButton` vs `confirmButton`; `dropdownButton` vs `toggle`; modal constructors take `Page` or a root; duplicated `navigate`/`clickOutside` in two layouts; `CartPage.shippingCostLabel` duplicates the layout's; `title='Add to cart'` selectors depend on UI language | Inconsistent. | Align names and constructor convention; common base layout; `data-test-id` for cart buttons (request from frontend if missing). |
| [ ] | R4.13 | P3 | Unused page-object members (about 35), e.g. `BladeToolbar.itemIds`, `Blade.label`, `Card.title/body`, `ConfirmationPopup.cancel`, `ListToolbar.refresh`, `Chip.textLabel/closeButton`, `TopHeader.signInLink/signUpLink`, `AccountMenu.signOutButton`, `CheckoutFlow.clickOutside`, exported `MENU_ITEM_FOR_ROUTE` | Dead code. | Remove, or keep deliberately when a planned test uses it. |
| [ ] | R4.14 | P3 | `pages/frontend/components/address-form.ts:73-77`, `payment-details-section.ts:19`, `graphql-traffic.ts:12-18` | `fillIfGiven` skips `""`; `uncheck({ force: true })`; `isGraphqlMutation("")` matches any mutation and tests pass loose fragments (`"cart"`, `"wishlist"`). | `!== undefined`; click the visible label; prefer `isGraphqlOperation(name)`. |

---

## 5. API clients

| | ID | P | Where | Problem | What to do |
|---|---|---|---|---|---|
| [ ] | R5.1 | P2 | 20+ clients in `api/rest/clients` | Four different "not found" conventions (404, `null` body, empty text, 204); `promotions-client.ts` mixes two in one class. | One `HttpResponse` helper (e.g. `jsonOrUndefined<T>()`) used by every `find*`. |
| [ ] | R5.2 | P2 | `users-client.ts:28-93`, `roles-client.ts:24-26` | `SecurityResult` returned without checking `succeeded`; the check is copy-pasted in arrange helpers and specs. | Shared `expectSucceeded(result, label)`; keep raw methods for negative tests. |
| [ ] | R5.3 | P2 | `api/http/http-response.ts:51-53` + all clients | `json<T>()` is an unchecked cast; only 2 clients validate with a schema; `requireFields` checks a few fields. Repeated `(results ?? []).map(requireFields)` and `requireFields(json(), FIELDS, label)` in every client. | Shared helpers `requireJson(response, fields, label)` / `requireResults(...)`; decide whether `json()` returns `unknown`. |
| [ ] | R5.4 | P2 | `orders-client.ts:86-89`, `platform-client.ts:54-63`, `notifications-client.ts:17-20` | Some `search*` return the raw result unvalidated, others validated arrays. | One shape for all. |
| [ ] | R5.5 | P2 | `api/auth/token-manager.ts:29-68` | No in-flight deduplication: parallel requests near expiry each refresh or sign in. | Cache the pending `Promise<AuthToken>` per session. |
| [ ] | R5.6 | P3 | Create/update verbs: `saveCatalog`/`updateCatalog`, `saveCategory`, `RolesClient.save` (PUT that creates), `saveCoupons` (POST `/add`), `saveEmployees` vs `createMany` | Inconsistent names. | `create` = POST, `update` = PUT, `save` only for real upserts. |
| [ ] | R5.7 | P3 | Delete arity (single id vs arrays), `remove`/`removeMany` vs `delete`; "new template" factories (`getNew`, `getNewCategory`, `getNewAssignment`, `newPayment`, `newPublication`) | Inconsistent. | `delete(ids: readonly string[])`; one `new…()` pattern. |
| [ ] | R5.8 | P3 | `browser-sessions.ts:15-16,42-48,69-76` | `STOREFRONT_*` / `storefront*` names break the "frontend" terminology. | Rename to `FRONTEND_*` / `frontend*`. |
| [ ] | R5.9 | P3 | `api/auth/token-manager.ts:31-32,50-54,70-78`, `browser-sessions.ts:27` | Replaced token not revoked; `signOutAll` fails on the first error; expired tokens refreshed just to revoke them; cookie cache keyed by username only. | Revoke replaced; `allSettled` + `AggregateError`; skip refresh on sign-out; key cookies by username + password. |
| [ ] | R5.10 | P3 | `api/http/http-client.ts:53-75`, `http-error.ts`, `graphql-error.ts:29-32` | `patch()` and `header()` unused; `json`/`form`/`multipart` can be combined; header case not normalised; `HttpError` has no `method`/`url`; GraphQL error text omits `extensions.code`. | Remove dead members; reject combined bodies; normalise headers; add fields and code. |
| [ ] | R5.11 | P3 | `pricing-client.ts:48,133,146` untyped `QueryParams` criteria; `dynamic-content-client.ts` `protected` fields and in-client `*_FIELDS`; `oauth-apps-client.ts` and `notifications.ts` skip the `FIELDS`/`WithRequired` pattern; mutable `T[]` parameters (10 clients); path literals inline in `customers`/`platform` clients; mixed relative and alias imports | Inconsistent. | Align with the common client pattern. |
| [ ] | R5.12 | P3 | Unused: `OrdersClient.getChanges`, `MemberSearchResult`, `DynamicContent*SearchResult`, `ProductAsset`, `LockMembershipRequest` (use it), duplicate re-exports of `ModuleDescriptorData` and `ChangeLogSearchResult`, `QuantityControl`/`RangeFilterType` types | Dead code. | Remove or use. |

---

## 6. Dataset and fixtures

| | ID | P | Where | Problem | What to do |
|---|---|---|---|---|---|
| [ ] | R6.1 | P2 | `core/required-fields.ts:4` | Accepts `T \| undefined` only, which causes `?? undefined` before every GraphQL result (13+ places). `""` passes as present. | Accept `T \| null \| undefined`; optional non-empty-string check; remove all `?? undefined`. |
| [ ] | R6.2 | P2 | `dataset/manifest.json:165-172` | `organizationMemberships` is `optional`, so every failure is only a warning. | Make it idempotent (find → create) and remove `optional`. |
| [ ] | R6.3 | P2 | `dataset/seeder.ts:49-90` | Failure messages keep only `METHOD url → status`: no item id, no response body, even for optional failures. | Include item id and body. |
| [ ] | R6.4 | P2 | `fixtures/browser.fixture.ts:34`, `customer-account.fixture.ts:53-67` | Every browser test resolves `browserCustomerAccount` and therefore the platform admin client, cleanup stack, token manager and dataset, even when it returns `undefined`. | Resolve the customer account only in `customer-account` mode. |
| [ ] | R6.5 | P2 | `fixtures/cleanup.fixture.ts:10` | Only `httpClient` is guaranteed to outlive the cleanup stack; cleanups through `platformAdminHttpClient` would break if a test requested the fixtures in a different order. | Also depend on `anonymousHttpClient`; then `httpClient` dependency can go. |
| [ ] | R6.6 | P2 | `dataset/data/manifest.json:99` | Only one place uses `${ENV:STORE_ID}` while `store-acme` is hard-coded 366 times; `STORE_ID` must be `store-acme` anyway. | Hard-code it there too, and document that `STORE_ID` must match the dataset. |
| [ ] | R6.7 | P2 | `tests/setup/seed.setup.ts:10-28` | Duplicates the pages module id and re-fetches installed modules; "apply page statuses" is skipped when only `pagesContent` is re-seeded; the second test keeps the default 30 s timeout. | Derive from the manifest and `resolveSeedScope`; include `pagesContent`; set a timeout on the `seed` project. |
| [ ] | R6.8 | P3 | `dataset/dataset.ts:27-51`, `frontend-context.ts:28,48-56`, `stock.ts:16,46`, `manifest.ts:37`, `seed-scope.ts:22-34` | Casts of untyped dataset JSON spread across files; duplicated user lookup; `?? ""` fallbacks. | Typed dataset accessors per manifest entity; one `findUser`; type guard for manifest names. |
| [ ] | R6.9 | P3 | New module | Seeded ids and usernames repeated across tests (R3.9, R3.10). | `dataset/seeded.ts` (or constants in builders) with seeded products, configurable product + options, users, organization; derive `SEEDED_CATALOG_ID` from the dataset store. |
| [ ] | R6.10 | P3 | `dataset/frontend-context.ts:21-26`, `fixtures/customer-account.fixture.ts:130` | `getFrontendContext` needs an anonymous id even for signed-in users; the fixture calls it with `undefined` just to get the store part. | Export `getStoreContext(dataset, storeId)`. |
| [ ] | R6.11 | P3 | `dataset/arrange/cart.ts:33-64,79,112-117`, `fixtures/cart.fixture.ts:32` | `arrangeCart` and `arrangeDefaultCart` nearly identical; `withItems` registers the same cart removal twice; repeated shopper label fallbacks. | One private helper; single registration; `describeShopper(context)`. |
| [ ] | R6.12 | P3 | `fixtures/customer-account.fixture.ts:36-114`, `page-builder.fixture.ts:4`, `index.ts:18`, `api.fixture.ts:50-71` | Nine dependencies listed twice; unused option `customerAccountOrganizationId`; page-builder fixture extends the shopper chain for nothing; redundant merges; two identical anonymous contexts per test. | Simplify as described. |
| [ ] | R6.13 | P3 | Builders: `completeness.ts:13` sends the catalog id as name; `product-configuration.ts:9-16` silently skips invalid sections; three different test-address builders; `newNamedContent` unused; `ORDER_CURRENCY`/`PRICELIST_CURRENCY` duplicate "USD"; `newEmployee` repeats `newContact`; `toMemberAddressInput` copies 21 fields by hand; `searchProducts` stops at 100 silently | Small correctness and duplication issues. | Fix individually. |

---

## 7. GraphQL documents

| | ID | P | Where | Problem | What to do |
|---|---|---|---|---|---|
| [ ] | R7.1 | P2 | `operations/contact/delete-contact`, `contact/get-contact`, `user/delete-users` (+ fragment `identity-result`), `order/orders`, `quote/cancel-quote-request`, `shopping-list/add-bulk-item-to-shopping-list` | Operations generated but never used. `cancelQuoteRequest`, own `orders` and bulk-add to a list are real coverage gaps. | Add tests for the gaps (quote cancel, my orders, bulk add), delete the rest. |
| [ ] | R7.2 | P2 | 8 places (`cart`, `line-item` fragments; `get-cart-validation*`, `get-cart-line-validation`, `add-bulk-items-cart` operations) | The validation-error selection is written out 8 times with different fields. | `ValidationError` fragment; drop `GetCartLineValidation` (subset of `GetCartValidation`). |
| [ ] | R7.3 | P2 | `fragments/configuration-line-item.graphql:5-7`, `fragments/cart-with-list.graphql:5-7`, `contact/lock-` / `unlock-organization-contact` | Over-fetching: full `...Product` per configuration option (only `id` is read); full `...Cart` for the saved-for-later list; full `...Contact` from lock/unlock (then a second query reads the status). | Slim selections; assert the lock status from the mutation result. |
| [ ] | R7.4 | P3 | `quote` (totals), `product` (vendor), `store-info` (settings), `user` (2 fields), pickup fragments (`workingHours`, `geoLocation`) | Fields never read. | Remove or move to detail fragments. |
| [ ] | R7.5 | P3 | Operation names | `Get` prefix used in half of the operations; shopping-list operations named differently from the xAPI fields (`DeleteShoppingList` → `removeWishlist`); `GetOrganizations` reads the current user's organizations. | One naming rule; rename accordingly (file names follow). |
| [ ] | R7.6 | P3 | `pickup-address` / `pickup-location-address`, `cart-address` / `member-address` fragments | Identical field lists on different types with unclear names. | Names that show the pairing. |
| [ ] | R7.7 | P3 | `contact/get-contact-roles-in-organization.graphql:3-6` | Inline `id name` instead of `...Role`. | Use the fragment. |

---

## 8. Configuration, tooling, CI, docs

| | ID | P | Where | Problem | What to do |
|---|---|---|---|---|---|
| [ ] | R8.1 | P1 | repo root | **No CI pipeline** (the old workflows were removed). | Per R0.3: PR job (`npm ci`, `biome ci .`, `npm run typecheck`). |
| [ ] | R8.2 | P1 | repo root | No automated test run. | Manual + nightly job: start the stack, wait for health, write `.env` from secrets, install Chromium, `npm run seed`, run the four projects, always upload `allure-results/` and `test-results/`, job timeout. |
| [ ] | R8.3 | P2 | repo root | Destructive tests have no safe runner. | Opt-in job and a `test:destructive` script with `--workers=1`. |
| [ ] | R8.4 | P1 | repo root | No committed way to start a platform with the right modules (module manifest and compose file were deleted). | Commit a module list and `docker-compose.yml` (or `ci/`), including Elasticsearch with enough memory (at least 1 GB heap / 2 GB container); link from README Prerequisites. |
| [ ] | R8.5 | P1 | `playwright.config.ts:27` | No `forbidOnly`: a committed `test.only` silently shrinks a CI run. | `forbidOnly: Boolean(process.env["CI"])`; make `noFocusedTests` a Biome error. |
| [ ] | R8.6 | P2 | `playwright.config.ts:42-49` | API projects use the default 30 s test timeout, equal to `REQUEST_TIMEOUT_MS`, so one slow request or sign-in retry exhausts the test. | Explicit 60–90 s timeout for `restapi`/`graphql` (or derived from `requestTimeoutMs`). |
| [ ] | R8.7 | P2 | `playwright.config.ts:30`, `package.json` | CI reporters missing; `allure-results/` never cleaned, so reports mix runs. | `github` + `junit` on CI; `clean` script / pre-test cleanup. |
| [ ] | R8.8 | P2 | `playwright.config.ts:36-66`, README | Test projects don't depend on `seed` and nothing detects an unseeded platform; a bare `npx playwright test` also runs `seed` alongside the tests. | Exclude `seed` from bare runs or add CI-only `dependencies: ["seed"]`; a cheap "is the dataset seeded" check with a clear message. |
| [ ] | R8.9 | P2 | `core/env.ts:20-27`, `.env.example` | Empty `ADMIN_PASSWORD=` etc. pass validation; `PAGE_SIZE` is unused (and `.env.example` says 50 while the default is 20); `SEED_ONLY` validated only in the seed test; `.env.example` has no trailing newline. | `min(1)`; remove `PAGE_SIZE`; validate `SEED_ONLY` in the schema; add commented `SEED_ONLY` line. |
| [ ] | R8.10 | P2 | `package.json` | No read-only lint for CI (`check` rewrites, `lint` passes on warnings). | `"ci": "biome ci ."`; errors for `noFocusedTests`, `noUnusedImports`. |
| [ ] | R8.11 | P2 | `.vscode/settings.json:12-14` | TypeScript files are formatted by the built-in formatter on save, not Biome, which fights the pre-commit hook. | `biomejs.biome` as TS formatter; commit `.vscode/extensions.json` (Biome, Playwright). |
| [ ] | R8.12 | P2 | `codegen-graphql.ts:11` | GraphQL codegen validates the full env (passwords etc.), REST codegen only needs `BACKEND_BASE_URL`; neither honours `VERIFY_SSL=false`. | Read only `BACKEND_BASE_URL`; document or handle self-signed certificates. |
| [ ] | R8.13 | P3 | `package.json`, `tsconfig.json` | No `"private": true`; `@types/node` 26 vs `engines` 22; no `.nvmrc`; pre-commit uses `npx`; no `include` in tsconfig; `verbatimModuleSyntax` not enabled. | Add/adjust; check `verbatimModuleSyntax` with the CJS/ESM mix. |
| [ ] | R8.14 | P3 | `biome/layers.json`, `biome.json` | Pages layer does not forbid `expect`/`test` from `@playwright/test`; core may import `@playwright/test`; no `vcs.defaultBranch`. | Add restrictions; `defaultBranch: "dev"`. |
| [ ] | R8.15 | P3 | `.gitignore` | `.env.*`, `*.local.*`, probe/scratch folders, `*.tsbuildinfo`, IDE/OS files not ignored. | Extend (keep `!.env.example`). |
| [ ] | R8.16 | P3 | `README.md`, `BUG-concurrent-token-sign-in-500.md` | Hard-coded test counts will go stale; no note that `npm test` needs a seeded platform; project structure omits some dataset files; destructive commands lack `--workers=1`; bug report has no tracker key and its code block starts with a comment. | Update README; file the bug, add the key, move to `docs/known-issues/`. |
