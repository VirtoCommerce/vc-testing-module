import * as allure from "allure-js-commons";

import { OAuthAppsClient } from "@api/rest/clients/oauth-apps-client";
import { uniqueId } from "@core/unique-id";
import { newPassword } from "@dataset/builders/security";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Platform / OAuth Apps");
});

test.describe("OAuth apps (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create an OAuth app", async ({ httpClient, cleanupStack }) => {
    const oauthAppsClient = new OAuthAppsClient(httpClient);
    const clientId = uniqueId("test-client");
    cleanupStack.push(`delete OAuth app ${clientId}`, () => oauthAppsClient.delete([clientId]));

    const app = await test.step("act: create OAuth app", () =>
      oauthAppsClient.create({ clientId, clientSecret: newPassword(), displayName: clientId }));

    await test.step("assert: app is a confidential client", async () => {
      expect(app).toMatchObject({ clientId, displayName: clientId, clientType: "confidential" });
    });
  });

  test("search OAuth apps", async ({ httpClient, cleanupStack }) => {
    const oauthAppsClient = new OAuthAppsClient(httpClient);
    const clientId = uniqueId("test-client");
    cleanupStack.push(`delete OAuth app ${clientId}`, () => oauthAppsClient.delete([clientId]));
    await test.step("arrange: OAuth app", () =>
      oauthAppsClient.create({ clientId, clientSecret: newPassword(), displayName: clientId }));

    const found = await test.step("act: search by client id", () => oauthAppsClient.search({ keyword: clientId }));

    await test.step("assert: app is found without its secret", async () => {
      expect(found).toEqual([expect.objectContaining({ clientId, clientSecret: "" })]);
    });
  });

  test("delete an OAuth app", async ({ httpClient, cleanupStack }) => {
    const oauthAppsClient = new OAuthAppsClient(httpClient);
    const clientId = uniqueId("test-client");
    cleanupStack.push(`delete OAuth app ${clientId}`, () => oauthAppsClient.delete([clientId]));
    await test.step("arrange: OAuth app", () =>
      oauthAppsClient.create({ clientId, clientSecret: newPassword(), displayName: clientId }));

    await test.step("act: delete OAuth app", () => oauthAppsClient.delete([clientId]));

    await test.step("assert: app is not found", async () => {
      expect(await oauthAppsClient.search({ keyword: clientId })).toEqual([]);
    });
  });
});
