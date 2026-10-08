import * as allure from "allure-js-commons";

import { CATEGORIES_PATH, CatalogClient } from "@api/rest/clients/catalog-client";
import { uniqueId } from "@core/unique-id";
import { newCatalog, newCategory } from "@dataset/builders/catalog";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Catalog / Categories");
});

test.describe("categories (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create a category", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const draft = newCategory(catalog.id);

    const category = await test.step("act: create category", () => catalogClient.saveCategory(draft));

    await test.step("assert: category belongs to the catalog", async () => {
      expect(category).toMatchObject({ name: draft.name, code: draft.code, catalogId: catalog.id });
    });
  });

  test("rename a category", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const category = await test.step("arrange: category", () => catalogClient.saveCategory(newCategory(catalog.id)));
    const newName = `${category.name}-renamed`;

    await test.step("act: rename category", () => catalogClient.saveCategory({ ...category, name: newName }));

    await test.step("assert: category has the new name", async () => {
      expect((await catalogClient.getCategory(category.id)).name).toBe(newName);
    });
  });

  test("get a category by id", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const category = await test.step("arrange: category", () => catalogClient.saveCategory(newCategory(catalog.id)));

    const reloaded = await test.step("act: get category", () => catalogClient.getCategory(category.id));

    await test.step("assert: fields match the created category", async () => {
      expect(reloaded).toMatchObject({
        id: category.id,
        name: category.name,
        code: category.code,
        catalogId: category.catalogId,
      });
    });
  });

  test("find a category in the catalog list entries", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const category = await test.step("arrange: category", () => catalogClient.saveCategory(newCategory(catalog.id)));

    const entries = await test.step("act: search list entries", () =>
      catalogClient.searchListEntries({ catalogId: catalog.id, responseGroup: "withCategories" }));

    await test.step("assert: category is in the list entries", async () => {
      expect(entries.map(({ id }) => id)).toContain(category.id);
    });
  });

  test("get a new category template", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));

    const template = await test.step("act: get new category template", () => catalogClient.getNewCategory(catalog.id));

    await test.step("assert: template has the Category SEO type", async () => {
      expect(template.seoObjectType).toBe("Category");
    });
  });

  test("create a nested category", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const parent = await test.step("arrange: parent category", () =>
      catalogClient.saveCategory(newCategory(catalog.id)));

    const child = await test.step("act: create child category", () =>
      catalogClient.saveCategory({ ...newCategory(catalog.id), parentId: parent.id }));

    await test.step("assert: child is under the parent in the same catalog", async () => {
      expect(await catalogClient.getCategory(child.id)).toMatchObject({
        parentId: parent.id,
        catalogId: parent.catalogId,
      });
    });
  });

  test("delete a category", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const category = await test.step("arrange: category", () => catalogClient.saveCategory(newCategory(catalog.id)));

    await test.step("act: delete category", () => catalogClient.deleteListEntries([category.id]));

    await test.step("assert: category is not found", async () => {
      const response = await httpClient.get(`${CATEGORIES_PATH}/${encodeURIComponent(category.id)}`);
      expect(response.status).toBe(404);
    });
  });

  test("get a missing category", async ({ httpClient }) => {
    const response = await test.step("act: get category by a missing id", () =>
      httpClient.get(`${CATEGORIES_PATH}/${uniqueId("test-missing-category")}`));

    await test.step("assert: category is not found", async () => {
      expect(response.status).toBe(404);
    });
  });
});
