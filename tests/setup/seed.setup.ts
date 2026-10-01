import { ModulesClient } from "@api/rest/clients/modules-client";
import { PageBuilderClient } from "@api/rest/clients/page-builder-client";
import { ShippingMethodsClient } from "@api/rest/clients/shipping-methods-client";
import { createLogger } from "@core/logger";
import { applyPageStatuses } from "@dataset/page-statuses";
import { parseSeedOnly } from "@dataset/seed-scope";
import { seedDataset } from "@dataset/seeder";
import { ensureShippingMethods } from "@dataset/shipping-methods";
import { test } from "@fixtures";

const SEED_TIMEOUT_MS = 15 * 60_000;
const PAGE_BUILDER_MODULE_ID = "VirtoCommerce.PageBuilderModule";
const SHIPPING_MODULE_ID = "VirtoCommerce.Shipping";

test.use({ user: async ({ env }, use) => use(env.admin) });
test.describe.configure({ mode: "serial" });

test("seed dataset", async ({ httpClient, dataset, env }) => {
  test.setTimeout(SEED_TIMEOUT_MS);

  await seedDataset(httpClient, dataset, createLogger("seed"), { only: parseSeedOnly(env.seedOnly) });
});

test("apply page statuses", async ({ httpClient, dataset, env }) => {
  const only = parseSeedOnly(env.seedOnly);
  test.skip(only !== undefined && !only.includes("pages"), "Pages are not part of SEED_ONLY");
  const installed = await new ModulesClient(httpClient).getInstalledIds();
  test.skip(!installed.has(PAGE_BUILDER_MODULE_ID), `${PAGE_BUILDER_MODULE_ID} is not installed`);

  await applyPageStatuses(new PageBuilderClient(httpClient), dataset, createLogger("page-statuses"));
});

test("verify shipping methods", async ({ httpClient, dataset, env }) => {
  const only = parseSeedOnly(env.seedOnly);
  test.skip(only !== undefined && !only.includes("shippingMethods"), "Shipping methods are not part of SEED_ONLY");
  const installed = await new ModulesClient(httpClient).getInstalledIds();
  test.skip(!installed.has(SHIPPING_MODULE_ID), `${SHIPPING_MODULE_ID} is not installed`);

  await ensureShippingMethods(new ShippingMethodsClient(httpClient), dataset, createLogger("shipping-methods"));
});
