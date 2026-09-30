# vc-testing-module

Automated tests for the Virto Commerce **platform** (REST API and xAPI GraphQL), the **frontend** (vc-frontend) and the **page-builder shell** in the platform admin. Written in TypeScript on [Playwright Test](https://playwright.dev/docs/test-intro), with Allure reporting.

| Project | What it tests | Tests |
|---|---|---|
| `restapi` | Platform REST API (`/api/...`) | 298 (+3 destructive) |
| `graphql` | xAPI GraphQL (`/graphql`) | 156 (+1 destructive) |
| `e2e-frontend` | vc-frontend in a browser | 68 |
| `e2e-backend` | Page-builder shell in the platform admin | 30 |
| `seed` | Loads the test dataset into the platform (setup, not tests) | 2 |

## Contents

- [Prerequisites](#prerequisites)
- [Local setup](#local-setup)
- [Running tests](#running-tests)
- [Configuration](#configuration)
- [Project structure](#project-structure)
- [How tests are written](#how-tests-are-written)
- [Signed-in users and prefilled carts in e2e tests](#signed-in-users-and-prefilled-carts-in-e2e-tests)
- [Code generation](#code-generation)
- [Code quality](#code-quality)
- [Continuous integration](#continuous-integration)
- [Known platform issues](#known-platform-issues)

## Prerequisites

- **Node.js 22.18 or later** (`engines` in `package.json`).
- **A running Virto Commerce platform** with the modules the tests cover (Catalog, Pricing, Inventory, Orders, Cart/xAPI, Customer, Marketing, Content, Shipping + xPickup, PageBuilder, …). The seeder skips entities whose module is not installed.
- **A running vc-frontend** connected to that platform, for `e2e-frontend` only.
- A platform **admin account** (the one used to seed data and call admin APIs).

The platform version and module versions CI runs against are listed in [`backend-packages.json`](backend-packages.json); a local platform with other versions works as long as it has the modules the dataset needs.

The defaults assume a local setup: platform at `http://localhost:8090`, frontend at `https://localhost:3000`.

## Local setup

Commands in `shell` blocks are the same in PowerShell and bash; where the syntax differs, both versions are shown.

1. **Install dependencies.** This also installs the git pre-commit hook (see [Code quality](#code-quality)).

   ```shell
   npm install
   ```

2. **Install the browser** used by the e2e projects:

   ```shell
   npx playwright install chromium
   ```

3. **Create `.env`** from the template and fill in the secrets:

   ```powershell
   # PowerShell
   Copy-Item .env.example .env
   ```

   ```bash
   # bash
   cp .env.example .env
   ```

   At minimum set `ADMIN_PASSWORD` and `USERS_PASSWORD` (the password of every seeded dataset user). For a local frontend with a self-signed certificate set `VERIFY_SSL=false`. All variables are described in [Configuration](#configuration).

4. **Seed the dataset** into the platform:

   ```shell
   npm run seed
   ```

   This loads everything in `dataset/data` (store, catalog, products, prices, inventory, contacts, organizations, users, pages, …) and then moves page-builder pages to the status each page file declares (pages are always created as Draft). Running it again updates the existing records; re-seeded pages drop back to Draft and are moved to their declared status again. The seed step is allowed up to 15 minutes.

5. **Check the setup** with a quick run:

   ```shell
   npx playwright test --project=restapi tests/restapi/health-check
   ```

## Running tests

| Command | Runs |
|---|---|
| `npm test` | All four test projects |
| `npm run test:restapi` | REST API tests |
| `npm run test:graphql` | GraphQL tests |
| `npm run test:e2e` | Frontend and page-builder e2e tests |
| `npm run test:e2e:frontend` | Frontend e2e tests |
| `npm run test:e2e:backend` | Page-builder shell e2e tests |

Useful Playwright options:

```shell
npx playwright test --project=graphql tests/graphql/cart          # one folder
npx playwright test --project=e2e-frontend -g "place an order"    # by title
npx playwright test --project=e2e-frontend --headed               # watch the browser
npx playwright test --project=e2e-frontend --ui                   # interactive UI mode
npx playwright show-trace test-results/<test-folder>/trace.zip    # inspect a failure
```

### Destructive tests

Tests tagged `@destructive` change platform-wide state (reload modules, restart the platform, drop and rebuild the product index, turn off anonymous access to the store). They are excluded unless explicitly enabled, and should run on their own:

```powershell
# PowerShell
$env:RUN_DESTRUCTIVE_TESTS = 'true'; npx playwright test --grep "@destructive"
```

```bash
# bash
RUN_DESTRUCTIVE_TESTS=true npx playwright test --grep "@destructive"
```

### Seeding options

| Command | Does |
|---|---|
| `npm run seed` | Seeds everything and applies page statuses |
| `npm run seed:page-statuses` | Re-applies page-builder page statuses only (no-op when they already match) |

To seed only some entities, set `SEED_ONLY` to their names from `dataset/data/manifest.json`:

```powershell
# PowerShell
$env:SEED_ONLY = 'products,prices'; npm run seed
```

```bash
# bash
SEED_ONLY=products,prices npm run seed
```

In PowerShell, `$env:` variables stay set for the rest of the session; remove one with `Remove-Item Env:SEED_ONLY`. The bash form applies to that one command only.

### Reports

Every run writes Allure results to `allure-results/`, plus traces and screenshots of failed tests to `test-results/`.

```shell
npm run report        # build the HTML report into allure-report/
npm run report:open   # open it
```

The report tree is grouped by suite, then spec file, then `describe` block (`restapi › restapi/marketing/dynamic-content.spec.ts › dynamic content (admin) › …`). The grouping is set in [`allurerc.mjs`](allurerc.mjs) and uses the `parentSuite` (Playwright project), `suite` (spec file) and `subSuite` (`describe`) labels that `allure-playwright` sets on every result.

`allure-results/` is not cleared between runs, so a report built after several runs mixes their results. For a report of one run, delete it first:

```powershell
Remove-Item -Recurse -Force allure-results
```

```bash
rm -rf allure-results
```

A CI run uploads a `playwright-test-results-…` artifact with the HTML report in `report/allure-report/` and the failed tests' traces in `test-results/`. The report loads its data over HTTP, so opening `index.html` from disk doesn't work: unzip the artifact and serve the report from this repo.

```shell
npx allure open <unzipped artifact>/report/allure-report
npx playwright show-trace <unzipped artifact>/test-results/<test>/trace.zip   # a failed test's trace
```

## Configuration

All settings come from environment variables, loaded from `.env` when it exists and validated at start-up by `core/env.ts` (an invalid or missing value fails fast with a clear message).

| Variable | Default | Meaning |
|---|---|---|
| `BACKEND_BASE_URL` | — | Platform URL, e.g. `http://localhost:8090` |
| `FRONTEND_BASE_URL` | — | Frontend URL, e.g. `https://localhost:3000` |
| `PAGE_BUILDER_PATH` | `/apps/page-builder-shell/` | Path of the page-builder shell app on the platform |
| `STORE_ID` | — | Store the tests use (`store-acme` in the dataset) |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | — | Platform admin account |
| `USERS_PASSWORD` | — | Password of the seeded dataset users |
| `REQUEST_TIMEOUT_MS` | `30000` | Timeout of API requests |
| `VERIFY_SSL` | `true` | Set `false` for self-signed certificates, including a local frontend dev server on `https://localhost:3000` (Node does not trust it even when the browser does) |
| `RUN_DESTRUCTIVE_TESTS` | `false` | Include `@destructive` tests |
| `PAGE_SIZE` | `20` | Default page size for list/search requests |
| `E2E_WORKERS` | 2 on CI, otherwise half the CPU cores | Parallel browser workers for `e2e-frontend` (`e2e-backend` always uses 1) |
| `QUANTITY_CONTROL` | `stepper` | Frontend quantity control: `stepper` or `button` |
| `RANGE_FILTER_TYPE` | `slider` | Frontend price filter: `slider` or `default` (checkboxes) |
| `CHECKOUT_MODE` | `single-page` | Frontend checkout: `single-page` or `multi-step` |
| `GOOGLE_MAPS_API_KEY` | — | Optional, for map-based frontend features |
| `SEED_ONLY` | — | Comma-separated entities to seed (see above) |

`QUANTITY_CONTROL`, `RANGE_FILTER_TYPE` and `CHECKOUT_MODE` must match how the frontend theme is configured. Tests that only apply to the other variant are skipped; checkout tests adapt to `CHECKOUT_MODE`.

### Parallel e2e workers (`E2E_WORKERS`)

`E2E_WORKERS` sets how many browsers the `e2e-frontend` project runs at the same time. Each worker is a separate browser that loads frontend pages, and every page load sends catalog, cart and menu queries through xAPI to the platform, which answers most of them from Elasticsearch. So the right number depends on how much concurrent traffic **the platform and its search engine** can serve, not on how many CPU cores the test machine has.

How the number is chosen:

| Situation | `e2e-frontend` workers |
|---|---|
| `E2E_WORKERS` is set (environment or `.env`) | that value, always |
| not set, running on CI (the `CI` variable is set, as on GitHub Actions and most CI systems) | 2 |
| not set, running locally | Playwright's default: half the logical CPU cores |

Other projects are not affected: `e2e-backend` always runs with 1 worker (the page builder's counters, status lists and search are shared state), and `restapi` / `graphql` use Playwright's default because they do not render pages.

Choosing a value:

- **Start low on a new environment** (2–4) and raise it while the run stays green.
- **Too many workers shows up as timeouts, not assertion failures:** pages stuck on a loading spinner, a main menu without categories, a cart that never renders, or plain API calls in `arrange:` steps timing out after 30 s. Lower `E2E_WORKERS` before investigating individual tests.
- **Check the search engine first when the suite degrades under load.** With Elasticsearch capped at a 512 MB heap (1 GiB container) and Kibana attached to the same node, 8 workers pushed it into long garbage-collection pauses and restarts; platform responses then stalled for up to 30 s. Giving Elasticsearch more memory fixes the cause; fewer workers only reduce the pressure.
- **A Vite dev server as `FRONTEND_BASE_URL`** (for example `https://localhost:3000` from a local vc-frontend checkout) serves unbundled sources, about 4,000 requests per page load, so each page is slower than against a production build. Prefer fewer workers there.

Examples:

```powershell
# PowerShell: one run with 2 workers
$env:E2E_WORKERS = '2'; npm run test:e2e:frontend; Remove-Item Env:E2E_WORKERS
```

```bash
# bash: one run with 2 workers
E2E_WORKERS=2 npm run test:e2e:frontend
```

To make it permanent for your machine, put `E2E_WORKERS=4` (or another value) in `.env`. On CI, set it as a pipeline variable when the runner can take more or less than the default 2. Playwright's `--workers` option caps the whole run, so it can only lower the number further (for example `npx playwright test --project=e2e-frontend --workers=1` to run one test at a time); to raise it, change `E2E_WORKERS`.

## Project structure

```
api/                 Clients for the platform: HTTP, auth, REST and GraphQL
  auth/                Token and cookie sign-in, token cache, browser sessions
  http/                HttpClient: typed wrapper over Playwright's APIRequestContext
  rest/
    clients/           One client class per REST area (catalog, orders, stores, …)
    types/             Named types over the generated API model, with required fields
    generated/         Generated from the platform swagger (do not edit)
  graphql/
    fragments/         Reusable GraphQL fragments (*.graphql)
    operations/        Queries and mutations by area (*.graphql)
    generated/         Typed documents generated from the platform schema (do not edit)
    graphql-client.ts  Executes typed documents; throws on GraphQL errors
core/                Framework-free utilities: env, logger, cleanup stack, unique ids, …
dataset/             Test data and everything that creates it
  data/                JSON records seeded into the platform, plus manifest.json
  builders/            new…() functions returning valid drafts (contacts, pages, carts, …)
  arrange/             arrange…() functions that create data and register its cleanup
  seeder.ts            Seeds dataset/data in manifest order
  page-statuses.ts     Moves seeded pages to their declared status
  stock.ts             Queries over seeded inventory (which center stocks what)
pages/               Page objects (Playwright locators and UI actions, no API calls)
  frontend/            vc-frontend: pages, layouts, components, CheckoutFlow
  backend/             Platform admin: vc-shell controls and the page-builder shell
fixtures/            Playwright fixtures shared by all tests (merged in fixtures/index.ts)
tests/
  setup/               The seed project
  restapi/             REST API specs, one folder per platform area
  graphql/             GraphQL specs, one folder per xAPI area
  e2e/frontend/        Frontend specs: account, cart, catalog, checkout, site, wishlists
  e2e/backend/         Page-builder shell specs
biome/               Lint, import-order and layer rules (extended by biome.json)
.github/workflows/   CI: manual test runs (see Continuous integration)
backend-packages.json Platform image and module versions the CI stack installs
playwright.config.ts Projects, timeouts and reporters
allurerc.mjs         Allure report settings (tree grouped by suite)
codegen-rest.mts     REST types generation
codegen-graphql.ts   GraphQL types generation
```

### Layers

Each folder is a layer that may only depend on the layers below it. Biome enforces this (`biome/layers.json`), so an import across the rules fails the lint:

| Layer | May import |
|---|---|
| `core` | nothing else |
| `api` | `core` |
| `pages` | `core` (no API calls or data setup in page objects) |
| `dataset` | `api`, `core` |
| `fixtures` | everything except `tests` |
| `tests` | everything; `test` and `expect` must come from `@fixtures`, not `@playwright/test` |

Import aliases: `@core/*`, `@api/*`, `@dataset/*`, `@pages/*`, `@fixtures`.

### Fixtures

Tests get their clients and data through fixtures (`fixtures/`):

| Fixture | Gives |
|---|---|
| `env`, `dataset` | Validated settings; the loaded `dataset/data` |
| `httpClient`, `graphqlClient` | Clients signed in as the `user` option, or anonymous |
| `platformAdminHttpClient` | REST client signed in as the platform admin |
| `anonymousHttpClient` | A fresh unauthenticated client |
| `frontendContext` | Store, catalog, currency, culture and user ids for the current user |
| `customerAccount` | A **fresh** organization + contact + customer user, signed in, deleted after the test |
| `cleanupStack` | Undo actions registered during the test, run last-first at the end |
| `shopper` | Who is in the browser (anonymous, dataset user, or the customer account) |
| `cart` | The shopper's default cart; prefill it with `test.use({ cart: withItems([...]) })` |
| `pageBuilder`, `pageBuilderClient` | Page-builder shell page object; page-builder REST client |

Options set with `test.use(...)`:

- `user`: sign in as a dataset user, e.g. `test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, "acme_store_employee_1@acme.com")) })`.
- `shopperAccount: "customer-account"`: sign a fresh customer account into the browser.
- `customerAccountRole` (`org-employee` or `org-maintainer`) and `customerAccountOrganizationId`.

The `e2e-backend` project signs the browser in as the platform admin by default.

## How tests are written

- **Arrange / act / assert steps.** Every test is split into `test.step("arrange: …")`, `test.step("act: …")` and `test.step("assert: …")`, so reports read as a script.
- **Own your data.** A test that changes state creates what it needs through `dataset/arrange` or a fixture, and registers the undo in `cleanupStack` right after creating it. Tests that change account state (carts, lists, addresses, organizations) use `customerAccount` instead of shared seeded users, so they can run in parallel. Seeded data is read-only.
- **Unique names** via `uniqueId(prefix)` for anything a test creates.
- **Wait with the web-first API**, never with sleeps: `expect(locator)…` for the UI, `expect.poll(...)` for eventually-consistent APIs (search indexes, pickup locations).
- **Known product issues** are marked with `test.fail(true, "<reason>")`. They pass while the issue exists and fail once it is fixed, so the reason gets revisited.
- **Page objects** expose locators and user actions; assertions stay in the tests.
- The `e2e-backend` project runs with **one worker**: page-builder counters, status lists and search are global state that parallel tests would disturb.

## Signed-in users and prefilled carts in e2e tests

Most e2e tests are about one screen: the cart, a checkout step, a wishlist. Getting there through the UI (open the sign-in page, type credentials, add products one by one) would make every test slower and dependent on screens it does not test, and a sign-in or add-to-cart hiccup would fail tests about something else. So the fixtures prepare the browser **before the test starts**: the browser is already signed in, and the cart already holds the products the test needs.

### How the browser is signed in

The `storageState` fixture (`fixtures/browser.fixture.ts`) builds the browser's initial storage from API calls, so the first page the test opens is already in the right state:

| Who | How | Where it lives in the browser |
|---|---|---|
| Anonymous visitor (default) | A random user id per test | `localStorage["user-id"]` on the frontend origin |
| Dataset user (`user` option) | A token from `/connect/token` | `localStorage["auth"]` on the frontend origin |
| Fresh customer account (`shopperAccount: "customer-account"`) | The account is created, then its token is issued | `localStorage["auth"]` on the frontend origin |
| Platform admin (`e2e-backend` default) | Cookie sign-in through `/api/platform/security/login` | the platform identity cookie |

Browser tokens are requested through the frontend (`FRONTEND_BASE_URL/connect/token`), not directly from the platform. The platform checks a token's issuer against the host a request arrives on and treats a mismatch as anonymous without an error, so a token issued by `BACKEND_BASE_URL` would not sign the browser in behind a proxy that forwards the frontend host (the CI nginx does). Going through the frontend's proxy makes the issuer match in every setup. Because of this, the Node side must trust the frontend's certificate: with a self-signed local dev server set `VERIFY_SSL=false`, or point `NODE_EXTRA_CA_CERTS` at its root CA.

Tokens come from a per-worker token cache, so a user signs in once per worker, not once per test. The random anonymous id means two anonymous tests never see each other's cart.

The `shopper` fixture describes whoever is in the browser: their `credentials`, a `graphqlClient` signed in as them, and their `context` (store, currency, culture, user id). Use it to arrange data for that same person through the API.

### Which account to use

- **Anonymous (the default)** for anything a guest can do: catalog, cart, guest checkout.
- **A fresh customer account** whenever the test changes account data: cart, saved-for-later, wishlists, addresses, organizations. Each test gets its own organization, contact and user, deleted afterwards, so tests can run in parallel without touching each other's data.

  ```ts
  import { saveMemberAddress } from "@dataset/arrange/contact";
  import { newMemberAddress } from "@dataset/builders/address";
  import { test } from "@fixtures";

  test.use({ shopperAccount: "customer-account" });

  test("pick a saved address", async ({ page, customerAccount }) => {
    await saveMemberAddress(customerAccount.graphqlClient, customerAccount.organizationId, newMemberAddress("test"));
    // the browser is signed in as customerAccount
  });
  ```

  `customerAccount` is the same account the browser is signed in as. Set `customerAccountRole: "org-maintainer"` for maintainer-only screens.

- **A dataset user** (`user` option) only for read-only checks of seeded data. Seeded users are shared by every worker, so a test that changes their cart or lists interferes with other tests.

### How the cart is prefilled

Use `withItems` in `test.use`:

```ts
import { test, withItems } from "@fixtures";
import { CartPage } from "@pages/frontend/pages/cart-page";

test.describe("cart line items", () => {
  test.use({
    shopperAccount: "customer-account",
    cart: withItems([{ productId: "smartphone-samsung-galaxy-a57-5g", quantity: 3 }]),
  });

  test("remove a line item", async ({ page }) => {
    const cartPage = new CartPage(page);
    await cartPage.navigate();
    // the cart already holds the product ×3
  });
});
```

Before the test starts, `withItems`:

1. adds the items to the shopper's **default cart** with xAPI `addItemsCart`, in the store's default currency and culture: the cart the frontend shows;
2. waits until that cart can be read back, so the first page load never races the create;
3. registers its removal in `cleanupStack`.

The `cart` fixture is automatic: without `withItems` it does nothing. The test can read the created cart when it needs ids or totals: `async ({ page, cart }) => …`.

When a test uses `withItems` or the `shopper` fixture, the shopper's whole default cart is removed after the test, including anything the test added through the UI. A test that only adds products through the UI and uses neither leaves a cart behind for its (random) anonymous id; request `shopper` in such tests to have it removed.

### When not to use them

- **The sign-in itself is under test.** Sign in through `SignInPage.signIn(...)` with `customerAccount.credentials`, and leave the browser anonymous. This also applies to cart merge (the browser must start anonymous) and to organization locks: locking a membership revokes the user's sessions, so lock first, then sign in through the UI.
- **The way products get into the cart is under test** (add-to-cart buttons, configurable products, wishlists): use the UI.
- **Configurable products** cannot be prefilled with `withItems`; they need their configuration sections, so add them through the product page.

### Things to keep in mind

- **Default cart vs named carts.** API and GraphQL tests use `arrangeCart`, which creates a cart with a unique name so parallel tests never share one. The frontend only shows the unnamed default cart, which is why e2e tests use `withItems` (or `arrangeDefaultCart` for an account other than the shopper, as in the cart-merge test).
- **The frontend signs in with an e-mail.** Fresh accounts therefore use their e-mail address as user name.
- **Product links may open a new tab.** The frontend opens product pages from cards according to the theme setting `details_browser_target` (`_blank` in release builds); its dev server always uses the same tab. Follow such links through the page object (for example `ProductCard.openConfigurations()`, which returns the page the product opened in), never by clicking and then asserting on the original `page`.
- **Storage is fixed when the page opens.** Anything that affects the session itself (a lock, a password change) must happen before a UI sign-in, not before a pre-signed-in page.

## Code generation

The API types are generated from the running platform and committed. Regenerate after a platform or module upgrade, or after adding `.graphql` documents:

```shell
npm run codegen           # both
npm run codegen:graphql   # GraphQL: schema from BACKEND_BASE_URL/graphql + documents in api/graphql
npm run codegen:rest      # REST: swagger from BACKEND_BASE_URL/docs/PlatformUI/swagger.json
```

To add a GraphQL operation: put the `.graphql` file under `api/graphql/operations/<area>/`, run `npm run codegen:graphql`, then use the generated `…Document` constant with `graphqlClient.execute(...)`.

## Code quality

| Command | Does |
|---|---|
| `npm run check` | Biome lint + format + import order, fixing what it can |
| `npm run lint` | Biome lint only |
| `npm run format` | Biome format only |
| `npm run typecheck` | TypeScript type check (`tsc --noEmit`) |

A **pre-commit hook** ([simple-git-hooks](https://github.com/toplenboren/simple-git-hooks), installed by `npm install`) runs `biome check` on the staged files and `tsc --noEmit`. If it blocks a commit, run `npm run check`, stage the fixes and commit again. To skip it once:

```powershell
# PowerShell
$env:SKIP_SIMPLE_GIT_HOOKS = '1'; git commit -m "..."; Remove-Item Env:SKIP_SIMPLE_GIT_HOOKS
```

```bash
# bash
SKIP_SIMPLE_GIT_HOOKS=1 git commit -m "..."
```

## Continuous integration

Tests run on GitHub Actions through [`.github/workflows/auto-tests.yml`](.github/workflows/auto-tests.yml), started by hand: **Actions → Auto Tests Docker → Run workflow**, on the branch whose tests should run.

| Input | Default | Meaning |
|---|---|---|
| `frontendZipUrl` | `latest` | vc-frontend build to deploy |
| `testSuites` | `all` | `all` (= `graphql`, `restapi`, `e2e`), or one of `graphql`, `restapi`, `e2e` (both e2e projects), `e2e-frontend`, `e2e-backend` |
| `grep` | empty | Playwright `--grep` pattern applied to every suite, e.g. a test title or tag |

The workflow calls the shared Playwright workflow from [`VirtoCommerce/.github`](https://github.com/VirtoCommerce/.github), which for each **database × search engine** combination:

1. starts the platform in Docker with the image and modules listed in [`backend-packages.json`](backend-packages.json), plus the frontend build (search engine: the one the module list installs, Elasticsearch 8 today; databases: SQL Server, MySQL and PostgreSQL by default, so a run executes the suites once per database);
2. writes `.env` from the env-file secret, setting `BACKEND_BASE_URL=http://localhost:8090`, `FRONTEND_BASE_URL=http://localhost` (the production frontend build, not a dev server) and the admin account;
3. installs dependencies and Chromium, runs the `seed` project and a full re-index;
4. runs the chosen suites one project at a time with list, JUnit, JSON and Allure reporters (the `CI` variable is set, so `e2e-frontend` uses 2 workers unless `E2E_WORKERS` is in the env secret);
5. builds the Allure report, lists failed tests in the run summary, and uploads a `playwright-test-results-<run>-<attempt>-<database>-<engine>` artifact (see [Reports](#reports) for opening it).

**Secrets** used by the workflow:

| Secret | Holds |
|---|---|
| `REPO_TOKEN` | Token for the shared workflow to fetch packages and repositories |
| env-file secret (placeholder `TS_ENV_SECRET_NAME` for now) | The whole `.env` for CI: at least `STORE_ID`, `ADMIN_PASSWORD`, `USERS_PASSWORD`, `GOOGLE_MAPS_API_KEY`; optionally `E2E_WORKERS`, and `RUN_DESTRUCTIVE_TESTS=true` to include destructive tests |
| `SENDGRID_APIKEY_4E2E_AUTOTESTS` | E-mail sending on the CI platform (notification flows such as the password-reset e-mail) |
| `E2E_APPINSIGHTSINSTRUMENTATIONKEY` | Optional platform telemetry |

**Keeping `backend-packages.json` current:** it pins the platform image (`PlatformImageTag`) and every module version CI installs. Tests target the edge versions: the latest platform release and, for each module, the newest release in the edge feed [`modules_v3.json`](https://raw.githubusercontent.com/VirtoCommerce/vc-modules/master/modules_v3.json) (its first version without a `VersionTag`). Bump the file to the current edge versions when new releases come out, and in the same change as tests that depend on them.

The shared workflow is currently referenced by a feature branch (`vcst-6033-playwright-workflow`); it moves to a release tag once VCST-6033 is released. Open CI work is tracked in [REFINEMENTS.md](REFINEMENTS.md) (section 8).

## Known platform issues

- **Parallel sign-ins of the same user fail.** Concurrent `POST /connect/token` requests for one user sometimes return HTTP 500, so the first test of a worker can fail at sign-in. See [BUG-concurrent-token-sign-in-500.md](BUG-concurrent-token-sign-in-500.md).
- **Page-builder search window.** The page search applies the keyword only to the newest 20 pages of the default sort; one reason `e2e-backend` runs with a single worker.
