import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { FrontendContext } from "@dataset/frontend-context";

import * as allure from "allure-js-commons";

import {
  CategoriesDocument,
  CategoryDocument,
  ProductDocument,
  ProductsDocument,
} from "@api/graphql/generated/graphql";
import { StoresClient } from "@api/rest/clients/stores-client";
import { requireFields } from "@core/required-fields";
import { SEEDED_CATALOG_ID } from "@dataset/builders/catalog";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const CATEGORY_ID = "category-acme-electronics-laptops";
const REGISTERED_USERNAME = "acme_store_employee_1@acme.com";
const ALLOW_ANONYMOUS_SETTING = "Stores.AllowAnonymousUsers";
const UNAUTHORIZED = "Unauthorized";
const SETTING_PROPAGATION_TIMEOUT_MS = 60_000;

test.beforeEach(async () => {
  await allure.feature("Catalog / Browsing");
});

test.describe("catalog browsing (anonymous)", () => {
  test("browse from a category to a product", async ({ graphqlClient, frontendContext }) => {
    await browseCategoryToProduct(graphqlClient, frontendContext);
  });
});

test.describe("catalog browsing (registered user)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, REGISTERED_USERNAME)) });

  test("browse from a category to a product", async ({ graphqlClient, frontendContext }) => {
    await browseCategoryToProduct(graphqlClient, frontendContext);
  });
});

test.describe("catalog browsing (store closed to anonymous users)", () => {
  test.describe.configure({ mode: "serial" });

  test("anonymous catalog queries are unauthorized", { tag: "@destructive" }, async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
  }) => {
    const storesClient = new StoresClient(platformAdminHttpClient);
    await test.step(`arrange: turn off ${ALLOW_ANONYMOUS_SETTING}`, async () => {
      cleanupStack.push(`turn ${ALLOW_ANONYMOUS_SETTING} back on`, async () => {
        await setAllowAnonymousUsers(storesClient, frontendContext.storeId, true);
        await expect
          .poll(() => categoriesErrorCode(graphqlClient, frontendContext), {
            timeout: SETTING_PROPAGATION_TIMEOUT_MS,
          })
          .toBeUndefined();
      });
      await setAllowAnonymousUsers(storesClient, frontendContext.storeId, false);
    });

    await test.step("act: wait for anonymous category queries to be rejected", async () => {
      await expect
        .poll(() => categoriesErrorCode(graphqlClient, frontendContext), { timeout: SETTING_PROPAGATION_TIMEOUT_MS })
        .toBe(UNAUTHORIZED);
    });

    await test.step("assert: category, product list and product queries are unauthorized too", async () => {
      const scope = catalogScope(frontendContext);
      const responses = await Promise.all([
        graphqlClient.executeRaw(CategoryDocument, { ...scope, id: CATEGORY_ID }),
        graphqlClient.executeRaw(ProductsDocument, { ...scope, filter: categoryFilter(CATEGORY_ID) }),
        graphqlClient.executeRaw(ProductDocument, { ...scope, id: "smartphone-apple-iphone-17-256gb-black" }),
      ]);
      expect(responses.map((response) => response.errors[0]?.extensions?.["code"])).toEqual([
        UNAUTHORIZED,
        UNAUTHORIZED,
        UNAUTHORIZED,
      ]);
    });
  });
});

async function browseCategoryToProduct(graphqlClient: GraphqlClient, context: FrontendContext): Promise<void> {
  const scope = catalogScope(context);

  const { categories } = await test.step(`act: list the categories of ${SEEDED_CATALOG_ID}`, () =>
    graphqlClient.execute(CategoriesDocument, {
      ...scope,
      filter: `category.subtree:${SEEDED_CATALOG_ID}`,
      first: 50,
    }));
  await test.step(`assert: ${CATEGORY_ID} is listed`, async () => {
    expect(categories?.items?.map((category) => category?.id)).toContain(CATEGORY_ID);
  });

  const { category } = await test.step(`act: open ${CATEGORY_ID}`, () =>
    graphqlClient.execute(CategoryDocument, { ...scope, id: CATEGORY_ID }));
  await test.step("assert: the category opens", async () => {
    expect(category?.id).toBe(CATEGORY_ID);
  });

  const { products } = await test.step(`act: list the products of ${CATEGORY_ID}`, () =>
    graphqlClient.execute(ProductsDocument, { ...scope, filter: categoryFilter(CATEGORY_ID) }));
  const listedProduct = requireFields(
    products?.items?.[0] ?? undefined,
    ["id", "name"],
    `First product of ${CATEGORY_ID}`,
  );

  const { product } = await test.step(`act: open ${listedProduct.id}`, () =>
    graphqlClient.execute(ProductDocument, { ...scope, id: listedProduct.id }));
  await test.step("assert: the product opens with the listed name", async () => {
    expect(product).toMatchObject({ id: listedProduct.id, name: listedProduct.name });
  });
}

interface CatalogScope {
  readonly storeId: string;
  readonly userId: string;
  readonly cultureName: string;
  readonly currencyCode: string;
}

function catalogScope(context: FrontendContext): CatalogScope {
  return {
    storeId: context.storeId,
    userId: context.userId,
    cultureName: context.cultureName,
    currencyCode: context.currencyCode,
  };
}

function categoryFilter(categoryId: string): string {
  return `category.subtree:${SEEDED_CATALOG_ID}/${categoryId}`;
}

async function categoriesErrorCode(graphqlClient: GraphqlClient, context: FrontendContext): Promise<unknown> {
  const response = await graphqlClient.executeRaw(CategoriesDocument, {
    ...catalogScope(context),
    filter: `category.subtree:${SEEDED_CATALOG_ID}`,
    first: 1,
  });
  return response.errors[0]?.extensions?.["code"];
}

async function setAllowAnonymousUsers(storesClient: StoresClient, storeId: string, allowed: boolean): Promise<void> {
  const store = await storesClient.get(storeId);
  await storesClient.update({
    ...store,
    settings: (store.settings ?? []).map((setting) =>
      setting.name === ALLOW_ANONYMOUS_SETTING ? { ...setting, value: allowed } : setting,
    ),
  });
}
