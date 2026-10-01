import * as allure from "allure-js-commons";

import { searchProducts } from "@dataset/arrange/catalog";
import { expect, test } from "@fixtures";

const SMARTPHONES_CATEGORY_ID = "category-acme-electronics-smartphones";
const PRODUCT_NAME = "Google Pixel 10 Pro Jade";
const PRODUCT_CODE = "smartphone-google-pixel-10-pro-jade";
const BRAND = "Google";

test.beforeEach(async () => {
  await allure.feature("Catalog / Search");
});

test.describe("catalog search (anonymous)", () => {
  test("find a product by its full name", async ({ graphqlClient, frontendContext }) => {
    const products = await test.step(`act: search "${PRODUCT_NAME}"`, () =>
      searchProducts(graphqlClient, frontendContext, { query: PRODUCT_NAME }));

    await test.step("assert: product is found", async () => {
      expect(products.map(({ name }) => name)).toContain(PRODUCT_NAME);
    });
  });

  test("find a product by a fragment of its name", async ({ graphqlClient, frontendContext }) => {
    const fragment = PRODUCT_NAME.slice(0, 4);

    const products = await test.step(`act: search "${fragment}"`, () =>
      searchProducts(graphqlClient, frontendContext, { query: fragment }));

    await test.step("assert: product is found", async () => {
      expect(products.map(({ name }) => name)).toContain(PRODUCT_NAME);
    });
  });

  test("find a product by its code", async ({ graphqlClient, frontendContext }) => {
    const products = await test.step(`act: search "${PRODUCT_CODE}"`, () =>
      searchProducts(graphqlClient, frontendContext, { query: PRODUCT_CODE }));

    await test.step("assert: product is found", async () => {
      expect(products.map(({ code }) => code)).toContain(PRODUCT_CODE);
    });
  });

  test("filter a category by availability", async ({ graphqlClient, frontendContext }) => {
    const category = `category.subtree:${frontendContext.catalogId}/${SMARTPHONES_CATEGORY_ID}`;
    const all = await test.step("arrange: every product of the category", () =>
      searchProducts(graphqlClient, frontendContext, { filter: category }));

    const inStock = await test.step("act: filter the category by InStock", () =>
      searchProducts(graphqlClient, frontendContext, { filter: `${category} availability:InStock` }));

    await test.step("assert: in-stock products are a smaller, non-empty subset", async () => {
      expect(inStock.length).toBeGreaterThan(0);
      expect(inStock.length).toBeLessThan(all.length);
      expect(all.map(({ id }) => id)).toEqual(expect.arrayContaining(inStock.map(({ id }) => id)));
    });
  });

  test("filter a category by brand", async ({ graphqlClient, frontendContext }) => {
    const category = `category.subtree:${frontendContext.catalogId}/${SMARTPHONES_CATEGORY_ID}`;
    const all = await test.step("arrange: every product of the category", () =>
      searchProducts(graphqlClient, frontendContext, { filter: category }));

    const branded = await test.step(`act: filter the category by brand ${BRAND}`, () =>
      searchProducts(graphqlClient, frontendContext, { filter: `${category} brand:${BRAND}` }));

    await test.step(`assert: only ${BRAND} products are returned`, async () => {
      expect(branded.length).toBeGreaterThan(0);
      expect(branded.length).toBeLessThan(all.length);
      expect(branded.filter(({ name }) => !name?.startsWith(BRAND))).toEqual([]);
    });
  });
});
