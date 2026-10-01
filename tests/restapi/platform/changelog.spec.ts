import * as allure from "allure-js-commons";

import { PlatformClient } from "@api/rest/clients/platform-client";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const TRACKED_OBJECT_TYPE = "ApplicationUser";

test.beforeEach(async () => {
  await allure.feature("Platform / Change Log");
});

test.describe("change log (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("get the last modified date", async ({ httpClient }) => {
    const platformClient = new PlatformClient(httpClient);

    const lastModifiedDate = await test.step("act: get last modified date", () => platformClient.getLastModifiedDate());

    await test.step("assert: date is a valid timestamp", async () => {
      expect(Number.isNaN(Date.parse(lastModifiedDate))).toBe(false);
    });
  });

  test("forcing changes moves the last modified date forward", async ({ httpClient }) => {
    const platformClient = new PlatformClient(httpClient);
    const before = await test.step("arrange: current last modified date", () => platformClient.getLastModifiedDate());

    await test.step("act: force changes", () => platformClient.forceChanges());

    await test.step("assert: last modified date is later", async () => {
      expect(Date.parse(await platformClient.getLastModifiedDate())).toBeGreaterThan(Date.parse(before));
    });
  });

  test("search the change log", async ({ httpClient }) => {
    const platformClient = new PlatformClient(httpClient);

    const result = await test.step("act: search change log", () => platformClient.searchChangeLog({ take: 10 }));

    await test.step("assert: change log has entries", async () => {
      expect(result.totalCount).toBeGreaterThan(0);
      expect(result.results?.length).toBeGreaterThan(0);
    });
  });

  test("filter the change log by object type", async ({ httpClient }) => {
    const platformClient = new PlatformClient(httpClient);

    const result = await test.step(`act: search ${TRACKED_OBJECT_TYPE} changes`, () =>
      platformClient.searchChangeLog({ objectType: TRACKED_OBJECT_TYPE, take: 20 }));

    await test.step(`assert: only ${TRACKED_OBJECT_TYPE} changes are returned`, async () => {
      const objectTypes = (result.results ?? []).map(({ objectType }) => objectType);
      expect(objectTypes.length).toBeGreaterThan(0);
      expect(new Set(objectTypes)).toEqual(new Set([TRACKED_OBJECT_TYPE]));
    });
  });
});
