import * as allure from "allure-js-commons";

import { SlugInfoDocument } from "@api/graphql/generated/graphql";
import { expect, test } from "@fixtures";

const CATEGORY_SLUG = "smartphones";
const PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black";
const PRODUCT_PERMALINK = "smartphones/apple-iphone-17-256gb-black";
const PRODUCT_SEMANTIC_URL = "apple-iphone-17-256gb-black";

test.beforeEach(async () => {
  await allure.feature("Catalog / SEO");
});

test.describe("SEO slugs (anonymous)", () => {
  test("resolve a category slug", async ({ graphqlClient, frontendContext }) => {
    const { slugInfo } = await test.step(`act: resolve slug "${CATEGORY_SLUG}"`, () =>
      graphqlClient.execute(SlugInfoDocument, {
        storeId: frontendContext.storeId,
        userId: frontendContext.userId,
        cultureName: frontendContext.cultureName,
        slug: CATEGORY_SLUG,
      }));

    await test.step("assert: slug resolves to the category", async () => {
      expect(slugInfo?.entityInfo).toMatchObject({ semanticUrl: CATEGORY_SLUG, objectType: "Category" });
    });
  });

  test("resolve a product permalink", async ({ graphqlClient, frontendContext }) => {
    const { slugInfo } = await test.step(`act: resolve permalink "${PRODUCT_PERMALINK}"`, () =>
      graphqlClient.execute(SlugInfoDocument, {
        storeId: frontendContext.storeId,
        userId: frontendContext.userId,
        cultureName: frontendContext.cultureName,
        permalink: PRODUCT_PERMALINK,
      }));

    await test.step("assert: permalink resolves to the active product page", async () => {
      expect(slugInfo?.entityInfo).toMatchObject({
        objectId: PRODUCT_ID,
        objectType: "CatalogProduct",
        semanticUrl: PRODUCT_SEMANTIC_URL,
        storeId: frontendContext.storeId,
        isActive: true,
        languageCode: frontendContext.cultureName,
        pageTitle: expect.any(String),
      });
    });
  });
});
