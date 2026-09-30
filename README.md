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
- [Code generation](#code-generation)
- [Code quality](#code-quality)
- [Known platform issues](#known-platform-issues)

## Prerequisites

- **Node.js 22.18 or later** (`engines` in `package.json`).
- **A running Virto Commerce platform** with the modules the tests cover (Catalog, Pricing, Inventory, Orders, Cart/xAPI, Customer, Marketing, Content, Shipping + xPickup, PageBuilder, …). The seeder skips entities whose module is not installed.
- **A running vc-frontend** connected to that platform, for `e2e-frontend` only.
- A platform **admin account** (the one used to seed data and call admin APIs).

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
| `VERIFY_SSL` | `true` | Set `false` for self-signed certificates |
| `RUN_DESTRUCTIVE_TESTS` | `false` | Include `@destructive` tests |
| `PAGE_SIZE` | `20` | Default page size for list/search requests |
| `QUANTITY_CONTROL` | `stepper` | Frontend quantity control: `stepper` or `button` |
| `RANGE_FILTER_TYPE` | `slider` | Frontend price filter: `slider` or `default` (checkboxes) |
| `CHECKOUT_MODE` | `single-page` | Frontend checkout: `single-page` or `multi-step` |
| `GOOGLE_MAPS_API_KEY` | — | Optional, for map-based frontend features |
| `SEED_ONLY` | — | Comma-separated entities to seed (see above) |

`QUANTITY_CONTROL`, `RANGE_FILTER_TYPE` and `CHECKOUT_MODE` must match how the frontend theme is configured. Tests that only apply to the other variant are skipped; checkout tests adapt to `CHECKOUT_MODE`.

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
playwright.config.ts Projects, timeouts and reporters
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

## Known platform issues

- **Parallel sign-ins of the same user fail.** Concurrent `POST /connect/token` requests for one user sometimes return HTTP 500, so the first test of a worker can fail at sign-in. See [BUG-concurrent-token-sign-in-500.md](BUG-concurrent-token-sign-in-500.md).
- **Page-builder search window.** The page search applies the keyword only to the newest 20 pages of the default sort; one reason `e2e-backend` runs with a single worker.
