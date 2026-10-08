import type { CatalogProduct, ProductImage } from "@api/rest/types/catalog";

import * as allure from "allure-js-commons";

import { CatalogClient } from "@api/rest/clients/catalog-client";
import { SettingsClient } from "@api/rest/clients/settings-client";
import { uniqueId } from "@core/unique-id";
import { newCatalog, newCategory, newProduct } from "@dataset/builders/catalog";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const REVIEW_TYPES_SETTING = "Catalog.EditorialReviewTypes";
const IMAGE = {
  name: "qa-image.svg",
  url: "/qa-images/qa-image.svg",
  relativeUrl: "/qa-images/qa-image.svg",
  group: "images",
  sortOrder: 1,
} satisfies ProductImage;

test.beforeEach(async () => {
  await allure.feature("Catalog / Products");
});

test.describe("products (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create a product", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const category = await test.step("arrange: category", () => catalogClient.saveCategory(newCategory(catalog.id)));
    const draft = newProduct(catalog.id, category.id);

    const product = await test.step("act: create product", () => catalogClient.saveProduct(draft));

    await test.step("assert: product is in the category", async () => {
      expect(product).toMatchObject({
        name: draft.name,
        code: draft.code,
        catalogId: catalog.id,
        categoryId: category.id,
      });
    });
  });

  test("rename a product and change its weight", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const product = await test.step("arrange: product", () => createProduct(catalogClient, catalog.id));
    const newName = `${product.name}-renamed`;

    await test.step("act: update product", () => catalogClient.saveProduct({ ...product, name: newName, weight: 2.5 }));

    await test.step("assert: product has the new name and weight", async () => {
      expect(await catalogClient.getProduct(product.id)).toMatchObject({ name: newName, weight: 2.5 });
    });
  });

  test("get a product by id", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const product = await test.step("arrange: product", () => createProduct(catalogClient, catalog.id));

    const reloaded = await test.step("act: get product", () => catalogClient.getProduct(product.id));

    await test.step("assert: fields match the created product", async () => {
      expect(reloaded).toMatchObject({ id: product.id, name: product.name, code: product.code });
    });
  });

  test("delete a product", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const product = await test.step("arrange: product", () => createProduct(catalogClient, catalog.id));

    await test.step("act: delete product", () => catalogClient.deleteListEntries([product.id]));

    await test.step("assert: product is not found", async () => {
      expect(await catalogClient.findProduct(product.id)).toBeUndefined();
    });
  });

  test("add an image to a product", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const product = await test.step("arrange: product", () => createProduct(catalogClient, catalog.id));

    await test.step("act: attach image", () => catalogClient.saveProduct({ ...product, images: [IMAGE] }));

    await test.step("assert: product has the image", async () => {
      const { images } = await catalogClient.getProduct(product.id);
      expect(images?.map(({ url }) => url)).toContainEqual(expect.stringContaining(IMAGE.url));
    });
  });

  test("get a product clone", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const product = await test.step("arrange: product", () => createProduct(catalogClient, catalog.id));

    const clone = await test.step("act: get clone", () => catalogClient.getProductClone(product.id));

    await test.step("assert: clone copies the product", async () => {
      expect(clone).toMatchObject({ name: product.name, catalogId: product.catalogId });
    });
  });

  test("save a product clone as a new product", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
    const product = await test.step("arrange: product", () => createProduct(catalogClient, catalog.id));
    const clone = await test.step("arrange: clone", () => catalogClient.getProductClone(product.id));
    const code = uniqueId("test-product-clone");

    const created = await test.step("act: save clone", () => catalogClient.saveProduct({ ...clone, id: null, code }));

    await test.step("assert: clone is a separate product", async () => {
      expect(created.id).not.toBe(product.id);
      expect(created.code).toBe(code);
    });
  });

  test("move a product to another catalog", async ({ httpClient, cleanupStack }) => {
    const catalogClient = new CatalogClient(httpClient);
    const source = await test.step("arrange: source catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${source.id}`, () => catalogClient.deleteCatalog(source.id));
    const target = await test.step("arrange: target catalog", () => catalogClient.saveCatalog(newCatalog()));
    cleanupStack.push(`delete catalog ${target.id}`, () => catalogClient.deleteCatalog(target.id));
    const product = await test.step("arrange: product", () => createProduct(catalogClient, source.id));

    await test.step("act: move product", () =>
      catalogClient.moveListEntries({
        catalog: target.id,
        listEntries: [
          {
            id: product.id,
            type: "product",
            name: product.name,
            code: product.code,
            catalogId: product.catalogId,
            isActive: true,
          },
        ],
      }));

    await test.step("assert: product is in the target catalog", async () => {
      expect((await catalogClient.getProduct(product.id)).catalogId).toBe(target.id);
    });
  });

  test("add and rename an editorial review type", async ({ httpClient, cleanupStack }) => {
    const settingsClient = new SettingsClient(httpClient);
    const original = await test.step("arrange: current review types", () => settingsClient.get(REVIEW_TYPES_SETTING));
    cleanupStack.push(`restore setting ${REVIEW_TYPES_SETTING}`, () => settingsClient.save([original]));
    const originalValues = original.allowedValues ?? [];
    const reviewType = uniqueId("test-review-type");
    const renamedType = `${reviewType}-renamed`;

    await test.step("act: add review type", () =>
      settingsClient.save([{ ...original, allowedValues: [...originalValues, reviewType] }]));

    await test.step("assert: review type is added", async () => {
      expect((await settingsClient.get(REVIEW_TYPES_SETTING)).allowedValues).toContain(reviewType);
    });

    await test.step("act: rename review type", () =>
      settingsClient.save([{ ...original, allowedValues: [...originalValues, renamedType] }]));

    await test.step("assert: review type is renamed", async () => {
      const { allowedValues } = await settingsClient.get(REVIEW_TYPES_SETTING);
      expect(allowedValues).toContain(renamedType);
      expect(allowedValues).not.toContain(reviewType);
    });
  });

  test("get a missing product", async ({ httpClient }) => {
    const catalogClient = new CatalogClient(httpClient);

    const product = await test.step("act: get product by a missing id", () =>
      catalogClient.findProduct(uniqueId("test-missing-product")));

    await test.step("assert: product is not found", async () => {
      expect(product).toBeUndefined();
    });
  });
});

async function createProduct(catalogClient: CatalogClient, catalogId: string): Promise<CatalogProduct> {
  const category = await catalogClient.saveCategory(newCategory(catalogId));
  return catalogClient.saveProduct(newProduct(catalogId, category.id));
}
