import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { FrontendContext } from "@dataset/frontend-context";

import * as allure from "allure-js-commons";

import { PageContextDocument } from "@api/graphql/generated/graphql";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const REGISTERED_USERNAME = "acme_store_maintainer_1@acme.com";
const CATEGORY_PERMALINK = "smartphones";
const ANONYMOUS_USER_NAME = "Anonymous";

test.beforeEach(async () => {
  await allure.feature("Catalog / Page Context");
});

test.describe("page context (anonymous)", () => {
  test("describe the requested store", async ({ graphqlClient, frontendContext }) => {
    const pageContext = await test.step("act: get page context", () => getPageContext(graphqlClient, frontendContext));

    await test.step("assert: store, default language and currency match the request", async () => {
      expect(pageContext?.store).toMatchObject({
        storeId: frontendContext.storeId,
        catalogId: frontendContext.catalogId,
        defaultLanguage: { cultureName: frontendContext.cultureName },
        defaultCurrency: { code: frontendContext.currencyCode },
      });
      expect(pageContext?.store?.availableLanguages?.length).toBeGreaterThan(0);
      expect(pageContext?.store?.availableCurrencies?.length).toBeGreaterThan(0);
    });
  });

  test("resolve a category permalink", async ({ graphqlClient, frontendContext }) => {
    const pageContext = await test.step(`act: get page context for "${CATEGORY_PERMALINK}"`, () =>
      getPageContext(graphqlClient, frontendContext, CATEGORY_PERMALINK));

    await test.step("assert: permalink resolves to the category", async () => {
      expect(pageContext?.slugInfo?.entityInfo).toMatchObject({
        objectType: "Category",
        semanticUrl: CATEGORY_PERMALINK,
      });
    });
  });

  test("report the anonymous user", async ({ graphqlClient, frontendContext }) => {
    const pageContext = await test.step("act: get page context", () => getPageContext(graphqlClient, frontendContext));

    await test.step("assert: user is anonymous", async () => {
      expect(pageContext?.user?.userName).toBe(ANONYMOUS_USER_NAME);
    });
  });

  test("return white-labeling settings when configured", async ({ graphqlClient, frontendContext }) => {
    const pageContext = await test.step("act: get page context", () => getPageContext(graphqlClient, frontendContext));

    await test.step("assert: white-labeling menus are lists when settings exist", async () => {
      const settings = pageContext?.whiteLabelingSettings;
      if (settings == null) {
        test.info().annotations.push({ type: "not asserted", description: "store has no white-labeling settings" });
        return;
      }
      expect(Array.isArray(settings.footerLinks)).toBe(true);
      expect(Array.isArray(settings.mainMenuLinks)).toBe(true);
    });
  });

  test("combine store, user and slug in one context", async ({ graphqlClient, frontendContext }) => {
    const pageContext = await test.step(`act: get page context for "${CATEGORY_PERMALINK}"`, () =>
      getPageContext(graphqlClient, frontendContext, CATEGORY_PERMALINK));

    await test.step("assert: store, anonymous user and category slug are all present", async () => {
      expect(pageContext).toMatchObject({
        store: { storeId: frontendContext.storeId },
        user: { userName: ANONYMOUS_USER_NAME },
        slugInfo: { entityInfo: { objectType: "Category" } },
      });
    });
  });
});

test.describe("page context (registered user)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, REGISTERED_USERNAME)) });

  test("resolve a category permalink for a registered user", async ({ graphqlClient, frontendContext }) => {
    const pageContext = await test.step(`act: get page context for "${CATEGORY_PERMALINK}"`, () =>
      getPageContext(graphqlClient, frontendContext, CATEGORY_PERMALINK));

    await test.step("assert: permalink resolves to the category", async () => {
      expect(pageContext?.slugInfo?.entityInfo?.semanticUrl).toBe(CATEGORY_PERMALINK);
    });
  });

  test("report the registered user", async ({ graphqlClient, frontendContext }) => {
    const pageContext = await test.step("act: get page context", () => getPageContext(graphqlClient, frontendContext));

    await test.step("assert: user is the signed-in user", async () => {
      expect(pageContext?.user?.userName).toBe(REGISTERED_USERNAME);
    });
  });
});

async function getPageContext(graphqlClient: GraphqlClient, context: FrontendContext, permalink?: string) {
  const { pageContext } = await graphqlClient.execute(PageContextDocument, {
    storeId: context.storeId,
    userId: context.userId,
    cultureName: context.cultureName,
    organizationId: context.organizationId,
    ...(permalink === undefined ? {} : { permalink }),
  });
  return pageContext;
}
