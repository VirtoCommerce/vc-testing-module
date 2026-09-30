import * as allure from "allure-js-commons";

import { ASSETS_PATH, AssetsClient } from "@api/rest/clients/assets-client";
import { CatalogClient } from "@api/rest/clients/catalog-client";
import { uniqueId } from "@core/unique-id";
import { getCredentials, getProduct } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const SAMPLE_FILE_URL = "https://raw.githubusercontent.com/VirtoCommerce/vc-testing-module/dev/README.md";
const USERNAME = "acme_store_administrator@acme.com";
const PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai";

test.beforeEach(async () => {
  await allure.feature("Catalog / Assets");
});

test.describe("catalog assets (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create a blob folder", async ({ httpClient, cleanupStack }) => {
    const assetsClient = new AssetsClient(httpClient);
    const folderName = uniqueId("test-folder");
    cleanupStack.push(`remove folder ${folderName}`, () => assetsClient.removeFolder(folderName));

    await test.step("act: create folder", () => assetsClient.createFolder(folderName));

    await test.step("assert: folder is listed", async () => {
      const folder = await assetsClient.find(folderName);
      expect(folder?.name).toBe(folderName);
    });
  });

  test("upload a file from a URL", async ({ httpClient, cleanupStack }) => {
    const assetsClient = new AssetsClient(httpClient);
    const folderName = uniqueId("test-folder");
    cleanupStack.push(`remove folder ${folderName}`, () => assetsClient.removeFolder(folderName));

    const file = await test.step("act: upload file from URL", () =>
      assetsClient.uploadFromUrl(folderName, SAMPLE_FILE_URL));

    await test.step("assert: file is in the folder", async () => {
      expect(file).toMatchObject({ name: "README.md", url: expect.stringContaining(folderName) });
    });
  });

  test("list assets", async ({ httpClient, cleanupStack }) => {
    const assetsClient = new AssetsClient(httpClient);
    const folderName = uniqueId("test-folder");

    await test.step("arrange: folder", () => assetsClient.createFolder(folderName));
    cleanupStack.push(`remove folder ${folderName}`, () => assetsClient.removeFolder(folderName));

    const entries = await test.step("act: get assets", () => assetsClient.list());

    await test.step("assert: the folder is listed and every entry has a name and url", async () => {
      expect(entries.map(({ name }) => name)).toContain(folderName);
      for (const entry of entries) {
        expect(entry).toMatchObject({ name: expect.any(String), url: expect.any(String) });
      }
    });
  });

  test("add an asset to a product", async ({ httpClient, cleanupStack, dataset }) => {
    const assetsClient = new AssetsClient(httpClient);
    const catalogClient = new CatalogClient(httpClient);
    const folderName = uniqueId("test-product-assets");
    const productId = uniqueId("test-product");

    const product = await test.step("arrange: copy of a dataset product", () =>
      catalogClient.saveProduct({
        ...getProduct(dataset, PRODUCT_ID),
        id: productId,
        code: productId,
        seoInfos: [],
      }));
    cleanupStack.push(`delete product ${product.id}`, () => catalogClient.deleteProduct(product.id));

    cleanupStack.push(`remove folder ${folderName}`, () => assetsClient.removeFolder(folderName));
    const file = await test.step("arrange: uploaded file", () =>
      assetsClient.uploadFromUrl(folderName, SAMPLE_FILE_URL));

    await test.step("act: attach the file to the product", () =>
      catalogClient.saveProduct({ ...product, assets: [{ name: file.name, url: file.url, group: "default" }] }));

    await test.step("assert: product has the asset", async () => {
      const { assets } = await catalogClient.getProduct(product.id);
      expect(assets?.map(({ name }) => name)).toContain(file.name);
    });
  });

  test("delete an uploaded asset", async ({ httpClient, cleanupStack }) => {
    const assetsClient = new AssetsClient(httpClient);
    const folderName = uniqueId("test-folder");
    cleanupStack.push(`remove folder ${folderName}`, () => assetsClient.removeFolder(folderName));

    const file = await test.step("arrange: uploaded file", () =>
      assetsClient.uploadFromUrl(folderName, SAMPLE_FILE_URL));

    await test.step("act: delete file", () => assetsClient.remove(file.url));

    await test.step("assert: file is gone", async () => {
      expect(await assetsClient.find(file.name, folderName)).toBeUndefined();
    });
  });
});

test.describe("catalog assets (anonymous)", () => {
  test("cannot list assets", async ({ httpClient }) => {
    const response = await test.step("act: get assets anonymously", () => httpClient.get(ASSETS_PATH));

    await test.step("assert: access is denied", async () => {
      expect(response.status).toBe(401);
    });
  });
});
