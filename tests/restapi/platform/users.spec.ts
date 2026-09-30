import * as allure from "allure-js-commons";

import { TokenAuthClient } from "@api/auth/token-auth-client";
import { UsersClient } from "@api/rest/clients/users-client";
import { requireFields } from "@core/required-fields";
import { arrangeUser } from "@dataset/arrange/security";
import { credentialsOf, newUser } from "@dataset/builders/security";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Platform / Users");
});

test.describe("platform users (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create a user", async ({ httpClient, cleanupStack, env }) => {
    const usersClient = new UsersClient(httpClient);
    const draft = newUser(env.storeId);
    cleanupStack.push(`delete user ${draft.userName}`, () => usersClient.delete([draft.userName]));

    const result = await test.step("act: create user", () => usersClient.create(draft));

    await test.step("assert: user is created and searchable", async () => {
      expect(result.succeeded).toBe(true);
      expect((await usersClient.search({ searchPhrase: draft.userName })).map(({ userName }) => userName)).toContain(
        draft.userName,
      );
    });
  });

  test("reject a duplicate user", async ({ httpClient, cleanupStack, env }) => {
    const usersClient = new UsersClient(httpClient);
    const draft = newUser(env.storeId);
    await test.step("arrange: user", () => arrangeUser(usersClient, cleanupStack, draft));

    const result = await test.step("act: create the same user again", () => usersClient.create(draft));

    await test.step("assert: user name and email are already taken", async () => {
      expect(result.succeeded).toBe(false);
      expect(result.errors).toEqual(
        expect.arrayContaining([expect.stringContaining(`Username '${draft.userName}' is already taken`)]),
      );
    });
  });

  test("search users by name", async ({ httpClient, cleanupStack, env }) => {
    const usersClient = new UsersClient(httpClient);
    const user = await test.step("arrange: user", () => arrangeUser(usersClient, cleanupStack, newUser(env.storeId)));

    const found = await test.step("act: search by user name", () =>
      usersClient.search({ searchPhrase: user.userName }));

    await test.step("assert: user is found", async () => {
      expect(found.map(({ id }) => id)).toContain(user.id);
    });
  });

  test("change the email of a user", async ({ httpClient, cleanupStack, env }) => {
    const usersClient = new UsersClient(httpClient);
    const user = await test.step("arrange: user", () => arrangeUser(usersClient, cleanupStack, newUser(env.storeId)));
    const email = `updated-${user.email}`;

    const result = await test.step("act: change email", () => usersClient.update({ ...user, email }));

    await test.step("assert: user has the new email", async () => {
      expect(result.succeeded).toBe(true);
      expect((await usersClient.get(user.userName)).email).toBe(email);
    });
  });

  test("delete a user", async ({ httpClient, cleanupStack, env }) => {
    const usersClient = new UsersClient(httpClient);
    const user = await test.step("arrange: user", () => arrangeUser(usersClient, cleanupStack, newUser(env.storeId)));

    await test.step("act: delete user", () => usersClient.delete([user.userName]));

    await test.step("assert: user is not found", async () => {
      expect(await usersClient.find(user.userName)).toBeUndefined();
      expect((await usersClient.search({ searchPhrase: user.userName })).map(({ id }) => id)).not.toContain(user.id);
    });
  });

  test("get a user by id", async ({ httpClient, cleanupStack, env }) => {
    const usersClient = new UsersClient(httpClient);
    const draft = newUser(env.storeId);
    const user = await test.step("arrange: user", () => arrangeUser(usersClient, cleanupStack, draft));

    const reloaded = await test.step("act: get user by id", () => usersClient.getById(user.id));

    await test.step("assert: fields match the created user", async () => {
      expect(reloaded).toMatchObject({ id: user.id, userName: draft.userName, email: draft.email });
    });
  });

  test("get a user by name", async ({ httpClient, cleanupStack, env }) => {
    const usersClient = new UsersClient(httpClient);
    const draft = newUser(env.storeId);
    await test.step("arrange: user", () => arrangeUser(usersClient, cleanupStack, draft));

    const user = await test.step("act: get user by name", () => usersClient.get(draft.userName));

    await test.step("assert: user is a manager without roles", async () => {
      expect(user).toMatchObject({ userName: draft.userName, userType: "Manager", roles: [] });
    });
  });

  test("sign a user in and out", async ({ httpClient, anonymousHttpClient, cleanupStack, env }) => {
    const usersClient = new UsersClient(httpClient);
    const tokenAuthClient = new TokenAuthClient(anonymousHttpClient);
    const draft = newUser(env.storeId);
    await test.step("arrange: user", () => arrangeUser(usersClient, cleanupStack, draft));

    const token = await test.step("act: sign in", () =>
      tokenAuthClient.requestToken(credentialsOf(draft), env.storeId));
    await test.step("assert: user gets a refreshable token", async () => {
      expect(token).toMatchObject({ accessToken: expect.any(String), refreshToken: expect.any(String) });
    });

    const { refreshToken } = requireFields(token, ["refreshToken"], `Token of ${draft.userName}`);

    await test.step("act: sign out", () => tokenAuthClient.revokeToken(token));
    await test.step("assert: revoked session cannot be refreshed", async () => {
      await expect(tokenAuthClient.refreshToken(refreshToken)).rejects.toMatchObject({ status: 400 });
    });
  });
});
