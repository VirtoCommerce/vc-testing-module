import * as allure from "allure-js-commons";

import { JobsClient } from "@api/rest/clients/jobs-client";
import { ModulesClient } from "@api/rest/clients/modules-client";
import { PlatformClient } from "@api/rest/clients/platform-client";
import { SearchIndexesClient } from "@api/rest/clients/search-indexes-client";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const CATALOG_MODULE_ID = "VirtoCommerce.Catalog";
const INDEXED_PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai";
const RESTART_TIMEOUT_MS = 300_000;

test.beforeEach(async () => {
  await allure.feature("Platform / System");
});

test.describe("platform system (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("list installed apps", async ({ httpClient }) => {
    const platformClient = new PlatformClient(httpClient);

    const apps = await test.step("act: list apps", () => platformClient.listApps());

    await test.step("assert: apps are installed", async () => {
      expect(apps.length).toBeGreaterThan(0);
    });
  });

  test("get system info", async ({ httpClient }) => {
    const platformClient = new PlatformClient(httpClient);

    const systemInfo = await test.step("act: get system info", () => platformClient.getSystemInfo());

    await test.step("assert: system info reports the platform version and process", async () => {
      expect(systemInfo).toMatchObject({ platformVersion: expect.any(String), is64BitProcess: expect.any(Boolean) });
    });
  });

  test("no module has load errors", async ({ httpClient }) => {
    const platformClient = new PlatformClient(httpClient);

    const modules = await test.step("act: list modules with errors", () => platformClient.listModulesWithErrors());

    await test.step("assert: no module failed to load", async () => {
      expect(modules.map(({ id }) => id)).toEqual([]);
    });
  });

  test("list installed modules", async ({ httpClient }) => {
    const modulesClient = new ModulesClient(httpClient);

    const moduleIds = await test.step("act: list installed modules", () => modulesClient.getInstalledIds());

    await test.step("assert: catalog module is installed", async () => {
      expect([...moduleIds]).toContain(CATALOG_MODULE_ID);
    });
  });

  test("get the status of a background job", async ({ httpClient }) => {
    const searchIndexesClient = new SearchIndexesClient(httpClient);
    const jobsClient = new JobsClient(httpClient);
    const { jobId } = await test.step("arrange: started indexation job", () =>
      searchIndexesClient.startIndexation([{ documentType: "Product", documentIds: [INDEXED_PRODUCT_ID] }]));

    const job = await test.step("act: get job status", () => jobsClient.get(jobId));

    await test.step("assert: job reports its state", async () => {
      expect(job).toMatchObject({ id: jobId, state: expect.any(String), completed: expect.any(Boolean) });
    });
  });

  test("reload modules", { tag: "@destructive" }, async ({ httpClient }) => {
    const modulesClient = new ModulesClient(httpClient);

    await test.step("act: reload modules", () => modulesClient.reload());

    await test.step("assert: catalog module is still installed", async () => {
      expect([...(await modulesClient.getInstalledIds())]).toContain(CATALOG_MODULE_ID);
    });
  });

  test("restart the platform", { tag: "@destructive" }, async ({ httpClient }) => {
    test.setTimeout(RESTART_TIMEOUT_MS + 30_000);
    const modulesClient = new ModulesClient(httpClient);
    const platformClient = new PlatformClient(httpClient);

    await test.step("act: restart platform", () => modulesClient.restart());

    await test.step("assert: platform comes back", async () => {
      await expect
        .poll(
          async () => {
            try {
              return (await platformClient.getSystemInfo()).platformVersion;
            } catch {
              return undefined;
            }
          },
          { timeout: RESTART_TIMEOUT_MS, intervals: [5_000] },
        )
        .toEqual(expect.any(String));
    });
  });
});
