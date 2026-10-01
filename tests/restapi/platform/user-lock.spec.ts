import * as allure from "allure-js-commons";

import { TokenAuthClient } from "@api/auth/token-auth-client";
import { UsersClient } from "@api/rest/clients/users-client";
import { arrangeApiKey, arrangeUser } from "@dataset/arrange/security";
import { credentialsOf, newUser } from "@dataset/builders/security";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const PROTECTED_PATH = "/api/platform/settings/VirtoCommerce.Search.IndexingJobs.Enable";

test.beforeEach(async () => {
  await allure.feature("Platform / User Lock");
});

test.describe("user lock (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("a locked user cannot sign in until unlocked", async ({
    httpClient,
    anonymousHttpClient,
    cleanupStack,
    env,
  }) => {
    const usersClient = new UsersClient(httpClient);
    const tokenAuthClient = new TokenAuthClient(anonymousHttpClient);
    const draft = newUser(env.storeId);
    const user = await test.step("arrange: user", () => arrangeUser(usersClient, cleanupStack, draft));

    await test.step("act: lock user", () => usersClient.lock(user.id));
    await test.step("assert: sign-in is rejected", async () => {
      await expect(tokenAuthClient.requestToken(credentialsOf(draft), env.storeId)).rejects.toMatchObject({
        status: 400,
      });
    });

    await test.step("act: unlock user", () => usersClient.unlock(user.id));
    await test.step("assert: user signs in again", async () => {
      await expect(tokenAuthClient.requestToken(credentialsOf(draft), env.storeId)).resolves.toMatchObject({
        accessToken: expect.any(String),
      });
    });
  });

  test("a deleted user cannot sign in", async ({ httpClient, anonymousHttpClient, cleanupStack, env }) => {
    const usersClient = new UsersClient(httpClient);
    const tokenAuthClient = new TokenAuthClient(anonymousHttpClient);
    const draft = newUser(env.storeId);
    await test.step("arrange: user", () => arrangeUser(usersClient, cleanupStack, draft));

    await test.step("act: delete user", () => usersClient.delete([draft.userName]));

    await test.step("assert: sign-in is rejected", async () => {
      await expect(tokenAuthClient.requestToken(credentialsOf(draft), env.storeId)).rejects.toMatchObject({
        status: 400,
      });
    });
  });

  test("a deactivated API key is rejected", async ({ httpClient, anonymousHttpClient, cleanupStack, env }) => {
    const usersClient = new UsersClient(httpClient);
    const user = await test.step("arrange: user", () => arrangeUser(usersClient, cleanupStack, newUser(env.storeId)));
    const apiKey = crypto.randomUUID().replaceAll("-", "");
    const key = await test.step("arrange: active API key", () =>
      arrangeApiKey(usersClient, cleanupStack, user, apiKey));

    await test.step("assert: active key authenticates the user", async () => {
      expect((await anonymousHttpClient.get(PROTECTED_PATH, { headers: { api_key: apiKey } })).status).toBe(403);
    });

    await test.step("act: deactivate API key", () => usersClient.updateApiKey({ ...key, isActive: false }));

    await test.step("assert: deactivated key is not authenticated", async () => {
      expect((await anonymousHttpClient.get(PROTECTED_PATH, { headers: { api_key: apiKey } })).status).toBe(401);
    });
  });
});
