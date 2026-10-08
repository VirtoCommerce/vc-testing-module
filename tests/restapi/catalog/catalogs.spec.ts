import * as allure from "allure-js-commons";

import { CatalogClient } from "@api/rest/clients/catalog-client";
import { uniqueId } from "@core/unique-id";
import { DEFAULT_LANGUAGE, newCatalog, newCategory, newProduct } from "@dataset/builders/catalog";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Catalog / Catalogs");
});

test.describe("catalogs (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create a physical catalog with a default language", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const name = uniqueId("test-catalog");

    const catalog = await test.step("act: create catalog", () => catalogClient.saveCatalog(newCatalog(name)));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));

    await test.step("assert: catalog is physical with en-US as the default language", async () => {
      expect(catalog).toMatchObject({ name, isVirtual: false });
      expect(catalog.languages).toContainEqual(expect.objectContaining(DEFAULT_LANGUAGE));
    });
  });

  test("create a virtual catalog", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const name = uniqueId("test-virtual-catalog");

    const catalog = await test.step("act: create virtual catalog", () =>
      catalogClient.saveCatalog({ ...newCatalog(name), isVirtual: true }));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));

    await test.step("assert: catalog is virtual", async () => {
      expect(catalog.isVirtual).toBe(true);
    });

    await test.step("assert: catalog is found as virtual", async () => {
      const found = await catalogClient.searchCatalogs({ keyword: name });
      expect(found.find(({ id }) => id === catalog.id)).toMatchObject({ isVirtual: true });
    });
  });

  test("rename a catalog", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const newName = `${catalog.name}-renamed`;

    await test.step("act: rename catalog", () =>
      catalogClient.updateCatalog({ ...catalog, name: newName, properties: catalog.properties ?? [] }));

    await test.step("assert: catalog is found by the new name", async () => {
      const found = await catalogClient.searchCatalogs({ keyword: newName });
      expect(found.map(({ name }) => name)).toContain(newName);
    });
  });

  test("search catalogs by keyword", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));

    const found = await test.step("act: search by catalog name", () =>
      catalogClient.searchCatalogs({ keyword: catalog.name }));

    await test.step("assert: catalog is in the results", async () => {
      expect(found.map(({ id }) => id)).toContain(catalog.id);
    });
  });

  test("delete a catalog", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));

    await test.step("act: delete catalog", () => catalogClient.deleteCatalog(catalog.id));

    await test.step("assert: catalog is not found", async () => {
      const found = await catalogClient.searchCatalogs({ keyword: catalog.name });
      expect(found.map(({ id }) => id)).not.toContain(catalog.id);
    });
  });

  test("search list entries within a category", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const category = await test.step("arrange: category", () => catalogClient.saveCategory(newCategory(catalog.id)));
    const product = await test.step("arrange: product in the category", () =>
      catalogClient.saveProduct(newProduct(catalog.id, category.id)));

    const entries = await test.step("act: search list entries", () =>
      catalogClient.searchListEntries({
        catalogId: catalog.id,
        categoryId: category.id,
        responseGroup: "withCategories, withProducts",
        take: 200,
      }));

    await test.step("assert: product is in the list entries", async () => {
      expect(entries.map(({ id }) => id)).toContain(product.id);
    });
  });
});
