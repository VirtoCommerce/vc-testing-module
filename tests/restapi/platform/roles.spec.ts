import type { Role, RoleData } from "@api/rest/types/security";
import type { CleanupStack } from "@core/cleanup-stack";

import * as allure from "allure-js-commons";

import { RolesClient } from "@api/rest/clients/roles-client";
import { UsersClient } from "@api/rest/clients/users-client";
import { arrangeUser } from "@dataset/arrange/security";
import { newRole, newUser } from "@dataset/builders/security";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const CALL_API_PERMISSION = "security:call_api";
const RESET_CACHE_PERMISSION = "cache:reset";

test.beforeEach(async () => {
  await allure.feature("Platform / Roles");
});

test.describe("roles (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create a role", async ({ httpClient, cleanupStack }) => {
    const rolesClient = new RolesClient(httpClient);
    const draft = newRole([CALL_API_PERMISSION]);

    const role = await test.step("act: create role", () => arrangeRole(rolesClient, cleanupStack, draft));

    await test.step("assert: role has its permission", async () => {
      expect(role.name).toBe(draft.name);
      expect(role.permissions?.map(({ name }) => name)).toEqual([CALL_API_PERMISSION]);
    });
  });

  test("get a role by name", async ({ httpClient, cleanupStack }) => {
    const rolesClient = new RolesClient(httpClient);
    const role = await test.step("arrange: role", () =>
      arrangeRole(rolesClient, cleanupStack, newRole([CALL_API_PERMISSION])));

    const reloaded = await test.step("act: get role", () => rolesClient.get(role.name));

    await test.step("assert: fields match the created role", async () => {
      expect(reloaded).toMatchObject({ id: role.id, name: role.name });
    });
  });

  test("search roles by keyword", async ({ httpClient, cleanupStack }) => {
    const rolesClient = new RolesClient(httpClient);
    const role = await test.step("arrange: role", () => arrangeRole(rolesClient, cleanupStack, newRole()));

    const found = await test.step("act: search by role name", () => rolesClient.search({ keyword: role.name }));

    await test.step("assert: role is found", async () => {
      expect(found.map(({ id }) => id)).toEqual([role.id]);
    });
  });

  test("describe a role", async ({ httpClient, cleanupStack }) => {
    const rolesClient = new RolesClient(httpClient);
    const role = await test.step("arrange: role", () => arrangeRole(rolesClient, cleanupStack, newRole()));
    const description = `Description of ${role.name}`;

    await test.step("act: set role description", () => rolesClient.save({ ...role, description }));

    await test.step("assert: role has the description", async () => {
      expect((await rolesClient.get(role.name)).description).toBe(description);
    });
  });

  test("delete a role", async ({ httpClient, cleanupStack }) => {
    const rolesClient = new RolesClient(httpClient);
    const role = await test.step("arrange: role", () => arrangeRole(rolesClient, cleanupStack, newRole()));

    await test.step("act: delete role", () => rolesClient.delete([role.id]));

    await test.step("assert: role is not found", async () => {
      expect(await rolesClient.find(role.name)).toBeUndefined();
      expect(await rolesClient.search({ keyword: role.name })).toEqual([]);
    });
  });

  test("remove a permission from a role", async ({ httpClient, cleanupStack }) => {
    const rolesClient = new RolesClient(httpClient);
    const role = await test.step("arrange: role with two permissions", () =>
      arrangeRole(rolesClient, cleanupStack, newRole([CALL_API_PERMISSION, RESET_CACHE_PERMISSION])));

    await test.step(`act: remove ${RESET_CACHE_PERMISSION}`, () =>
      rolesClient.save({ ...role, permissions: [{ name: CALL_API_PERMISSION }] }));

    await test.step(`assert: only ${CALL_API_PERMISSION} remains`, async () => {
      expect((await rolesClient.get(role.name)).permissions?.map(({ name }) => name)).toEqual([CALL_API_PERMISSION]);
    });
  });

  test("list all permissions", async ({ httpClient }) => {
    const rolesClient = new RolesClient(httpClient);

    const permissions = await test.step("act: list permissions", () => rolesClient.listPermissions());

    await test.step("assert: platform permissions are listed", async () => {
      expect(permissions.map(({ name }) => name)).toEqual(
        expect.arrayContaining([RESET_CACHE_PERMISSION, "platform:setting:read"]),
      );
    });
  });

  test("assign a role to a user and revoke it", async ({ httpClient, cleanupStack, env }) => {
    const rolesClient = new RolesClient(httpClient);
    const usersClient = new UsersClient(httpClient);
    const role = await test.step("arrange: role", () =>
      arrangeRole(rolesClient, cleanupStack, newRole([CALL_API_PERMISSION])));
    const user = await test.step("arrange: user", () => arrangeUser(usersClient, cleanupStack, newUser(env.storeId)));

    await test.step("act: assign role", () =>
      usersClient.update({ ...user, roles: [{ id: role.id, name: role.name }] }));
    await test.step("assert: user has the role", async () => {
      expect((await usersClient.get(user.userName)).roles?.map(({ id }) => id)).toEqual([role.id]);
    });

    await test.step("act: revoke role", async () =>
      usersClient.update({ ...(await usersClient.get(user.userName)), roles: [] }));
    await test.step("assert: user has no roles", async () => {
      expect((await usersClient.get(user.userName)).roles).toEqual([]);
    });
  });
});

async function arrangeRole(
  rolesClient: RolesClient,
  cleanupStack: CleanupStack,
  draft: RoleData & { name: string },
): Promise<Role> {
  cleanupStack.push(`delete role ${draft.name}`, async () => {
    const role = await rolesClient.find(draft.name);
    if (role !== undefined) {
      await rolesClient.delete([role.id]);
    }
  });
  const result = await rolesClient.save(draft);
  if (result.succeeded !== true) {
    throw new Error(`Cannot create role ${draft.name}: ${JSON.stringify(result.errors)}`);
  }
  return rolesClient.get(draft.name);
}
