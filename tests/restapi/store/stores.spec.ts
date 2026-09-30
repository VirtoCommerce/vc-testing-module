import * as allure from "allure-js-commons";

import { STORES_PATH, StoresClient } from "@api/rest/clients/stores-client";
import { uniqueId } from "@core/unique-id";
import { SEEDED_CATALOG_ID } from "@dataset/builders/catalog";
import { newStore } from "@dataset/builders/store";
import { getCredentials, getUser } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Store");
});

test.describe("stores (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create a store", async ({ httpClient, cleanupStack }) => {
    const storesClient = new StoresClient(httpClient);
    const draft = newStore();
    cleanupStack.push(`delete store ${draft.id}`, () => storesClient.delete(draft.id));

    const store = await test.step("act: create store", () => storesClient.create(draft));

    await test.step("assert: store uses the seeded catalog", async () => {
      expect(store).toMatchObject({ id: draft.id, name: draft.name, catalog: SEEDED_CATALOG_ID });
    });
  });

  test("reject a store without a name", async ({ httpClient, cleanupStack }) => {
    test.fail(true, "Platform returns 500 (database not-null violation) instead of a validation error");
    const id = uniqueId("test-store");
    cleanupStack.push(`delete store ${id}`, () => new StoresClient(httpClient).delete(id));

    const response = await test.step("act: create store without a name", () =>
      httpClient.post(STORES_PATH, { json: { id, catalog: SEEDED_CATALOG_ID } }));

    await test.step("assert: request is rejected as invalid", async () => {
      expect(response.status).toBeGreaterThanOrEqual(400);
      expect(response.status).toBeLessThan(500);
    });
  });

  test("get a store by id", async ({ httpClient, cleanupStack }) => {
    const storesClient = new StoresClient(httpClient);
    const store = await test.step("arrange: store", () => storesClient.create(newStore()));
    cleanupStack.push(`delete store ${store.id}`, () => storesClient.delete(store.id));

    const reloaded = await test.step("act: get store", () => storesClient.get(store.id));

    await test.step("assert: fields match the created store", async () => {
      expect(reloaded).toMatchObject({ id: store.id, name: store.name });
    });
  });

  test("list all stores", async ({ httpClient, env }) => {
    const storesClient = new StoresClient(httpClient);

    const stores = await test.step("act: list stores", () => storesClient.search({ take: 1000 }));

    await test.step("assert: seeded store is listed", async () => {
      expect(stores.map(({ id }) => id)).toContain(env.storeId);
    });
  });

  test("search stores by keyword", async ({ httpClient, cleanupStack }) => {
    const storesClient = new StoresClient(httpClient);
    const store = await test.step("arrange: store", () => storesClient.create(newStore()));
    cleanupStack.push(`delete store ${store.id}`, () => storesClient.delete(store.id));

    const found = await test.step("act: search by store name", () => storesClient.search({ keyword: store.name }));

    await test.step("assert: store is in the results", async () => {
      expect(found.map(({ id }) => id)).toContain(store.id);
    });
  });

  test("rename a store", async ({ httpClient, cleanupStack }) => {
    const storesClient = new StoresClient(httpClient);
    const store = await test.step("arrange: store", () => storesClient.create(newStore()));
    cleanupStack.push(`delete store ${store.id}`, () => storesClient.delete(store.id));
    const newName = `${store.name}-renamed`;

    await test.step("act: rename store", () => storesClient.update({ ...store, name: newName }));

    await test.step("assert: store has the new name", async () => {
      expect((await storesClient.get(store.id)).name).toBe(newName);
    });
  });

  test("create, rename, find and delete a store", async ({ httpClient, cleanupStack }) => {
    const storesClient = new StoresClient(httpClient);
    const draft = newStore();
    cleanupStack.push(`delete store ${draft.id}`, () => storesClient.delete(draft.id));
    const newName = `${draft.name}-renamed`;

    const store = await test.step("act: create store", () => storesClient.create(draft));
    await test.step("assert: store is readable", async () => {
      expect((await storesClient.get(store.id)).name).toBe(draft.name);
    });

    await test.step("act: rename store", () => storesClient.update({ ...store, name: newName }));
    await test.step("assert: store is found by the new name", async () => {
      expect((await storesClient.search({ keyword: newName })).map(({ id }) => id)).toContain(store.id);
    });

    await test.step("act: delete store", () => storesClient.delete(store.id));
    await test.step("assert: store is not found", async () => {
      expect(await storesClient.find(store.id)).toBeUndefined();
    });
  });

  test("delete a store", async ({ httpClient, cleanupStack }) => {
    const storesClient = new StoresClient(httpClient);
    const store = await test.step("arrange: store", () => storesClient.create(newStore()));
    cleanupStack.push(`delete store ${store.id}`, () => storesClient.delete(store.id));

    await test.step("act: delete store", () => storesClient.delete(store.id));

    await test.step("assert: store is not found", async () => {
      expect(await storesClient.find(store.id)).toBeUndefined();
    });
  });

  test("list stores allowed for a store administrator", async ({ httpClient, dataset, env }) => {
    const storesClient = new StoresClient(httpClient);
    const administrator = getUser(dataset, USERNAME);

    const stores = await test.step("act: list allowed stores", () => storesClient.listAllowed(administrator.id));

    await test.step("assert: seeded store is allowed", async () => {
      expect(stores.map(({ id }) => id)).toContain(env.storeId);
    });
  });

  test("get the seeded store", async ({ httpClient, env }) => {
    const storesClient = new StoresClient(httpClient);

    const store = await test.step("act: get seeded store", () => storesClient.get(env.storeId));

    await test.step("assert: store uses the seeded catalog", async () => {
      expect(store).toMatchObject({ id: env.storeId, catalog: SEEDED_CATALOG_ID });
    });
  });
});
