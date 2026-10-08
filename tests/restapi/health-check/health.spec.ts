import * as allure from "allure-js-commons";

import { HealthClient } from "@api/rest/clients/health-client";
import { SearchIndexesClient } from "@api/rest/clients/search-indexes-client";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Health Check");
});

test.describe("health check (anonymous)", () => {
  test("backend reports its health", async ({ httpClient }) => {
    const healthClient = new HealthClient(httpClient);

    const report = await test.step("act: get health report", () => healthClient.getReport());

    await test.step("assert: report lists health checks", async () => {
      expect(Object.keys(report).length).toBeGreaterThan(0);
    });
  });

  test("no health check is unhealthy", async ({ httpClient }) => {
    const healthClient = new HealthClient(httpClient);

    const report = await test.step("act: get health report", () => healthClient.getReport());

    await test.step("assert: every check is healthy or degraded", async () => {
      const unhealthy = Object.entries(report)
        .filter(([, check]) => check.Status === "Unhealthy")
        .map(([name, check]) => `${name}: ${check.Description}`);
      expect(unhealthy).toEqual([]);
    });
  });
});

test.describe("health check (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("search engine is reachable", async ({ httpClient }) => {
    const searchIndexesClient = new SearchIndexesClient(httpClient);

    const indexes = await test.step("act: get search indexes", () => searchIndexesClient.list());

    await test.step("assert: search provider reports its indexes", async () => {
      expect(indexes.length).toBeGreaterThan(0);
    });
  });
});
