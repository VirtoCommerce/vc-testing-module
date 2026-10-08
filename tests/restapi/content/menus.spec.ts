import * as allure from "allure-js-commons";

import { MenuLinkListsClient } from "@api/rest/clients/menu-link-lists-client";
import { uniqueId } from "@core/unique-id";
import { newMenuLinkList } from "@dataset/builders/content";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const LANGUAGE = "en-US";

test.beforeEach(async () => {
  await allure.feature("Content / Menus");
});

test.describe("menu link lists (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("list menu link lists", async ({ httpClient, cleanupStack, env }) => {
    const menuLinkListsClient = new MenuLinkListsClient(httpClient, env.storeId);
    const draft = newMenuLinkList(env.storeId);
    cleanupStack.push(`delete menu link list ${draft.id}`, () => menuLinkListsClient.delete(draft.id));
    await test.step("arrange: menu link list", () => menuLinkListsClient.save(draft));

    const lists = await test.step("act: list menu link lists", () => menuLinkListsClient.list());

    await test.step("assert: menu link list is listed", async () => {
      expect(lists.map(({ id }) => id)).toContain(draft.id);
    });
  });

  test("create a menu link list", async ({ httpClient, cleanupStack, env }) => {
    const menuLinkListsClient = new MenuLinkListsClient(httpClient, env.storeId);
    const draft = newMenuLinkList(env.storeId);
    cleanupStack.push(`delete menu link list ${draft.id}`, () => menuLinkListsClient.delete(draft.id));

    await test.step("act: create menu link list", () => menuLinkListsClient.save(draft));

    await test.step("assert: menu link list has its links", async () => {
      const list = await menuLinkListsClient.get(draft.id);
      expect(list).toMatchObject({ name: draft.name, storeId: env.storeId, language: LANGUAGE });
      expect(list.menuLinks?.map(({ title }) => title)).toEqual(draft.menuLinks?.map(({ title }) => title));
    });
  });

  test("check menu link list name availability", async ({ httpClient, cleanupStack, env }) => {
    const menuLinkListsClient = new MenuLinkListsClient(httpClient, env.storeId);
    const draft = newMenuLinkList(env.storeId);

    await test.step("assert: unused name is available", async () => {
      expect(await menuLinkListsClient.isNameAvailable(draft.name, LANGUAGE)).toBe(true);
    });

    cleanupStack.push(`delete menu link list ${draft.id}`, () => menuLinkListsClient.delete(draft.id));
    await test.step("act: create menu link list", () => menuLinkListsClient.save(draft));

    await test.step("assert: name is taken for other lists", async () => {
      expect(await menuLinkListsClient.isNameAvailable(draft.name, LANGUAGE)).toBe(false);
    });
    await test.step("assert: name is available to the list that owns it", async () => {
      expect(await menuLinkListsClient.isNameAvailable(draft.name, LANGUAGE, draft.id)).toBe(true);
    });
  });

  test("rename a menu link list", async ({ httpClient, cleanupStack, env }) => {
    const menuLinkListsClient = new MenuLinkListsClient(httpClient, env.storeId);
    const draft = newMenuLinkList(env.storeId);
    cleanupStack.push(`delete menu link list ${draft.id}`, () => menuLinkListsClient.delete(draft.id));
    await test.step("arrange: menu link list", () => menuLinkListsClient.save(draft));
    const newName = uniqueId("test-menu-renamed");

    await test.step("act: rename menu link list", () => menuLinkListsClient.save({ ...draft, name: newName }));

    await test.step("assert: menu link list has the new name", async () => {
      expect((await menuLinkListsClient.get(draft.id)).name).toBe(newName);
    });
  });

  test("delete a menu link list", async ({ httpClient, cleanupStack, env }) => {
    const menuLinkListsClient = new MenuLinkListsClient(httpClient, env.storeId);
    const draft = newMenuLinkList(env.storeId);
    cleanupStack.push(`delete menu link list ${draft.id}`, () => menuLinkListsClient.delete(draft.id));
    await test.step("arrange: menu link list", () => menuLinkListsClient.save(draft));

    await test.step("act: delete menu link list", () => menuLinkListsClient.delete(draft.id));

    await test.step("assert: menu link list is not found", async () => {
      expect(await menuLinkListsClient.find(draft.id)).toBeUndefined();
      expect((await menuLinkListsClient.list()).map((list) => list.id)).not.toContain(draft.id);
    });
  });
});
