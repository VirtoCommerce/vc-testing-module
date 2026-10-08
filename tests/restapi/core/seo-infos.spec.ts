import * as allure from "allure-js-commons";

import { SeoInfosClient } from "@api/rest/clients/seo-infos-client";
import { SEEDED_CATALOG_ID } from "@dataset/builders/catalog";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Core / SEO");
});

test.describe("seo infos (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("seeded catalog has no SEO duplicates", async ({ httpClient }) => {
    const seoInfosClient = new SeoInfosClient(httpClient);

    const duplicates = await test.step("act: find SEO duplicates", () =>
      seoInfosClient.findDuplicates("Catalog", SEEDED_CATALOG_ID));

    await test.step("assert: there are no duplicates", async () => {
      expect(duplicates).toEqual([]);
    });
  });
});
