import * as allure from "allure-js-commons";

import { AddItemsCartDocument, MergeCartDocument, ProductConfigurationDocument } from "@api/graphql/generated/graphql";
import { GraphqlClient } from "@api/graphql/graphql-client";
import { requireFields } from "@core/required-fields";
import { uniqueId } from "@core/unique-id";
import { arrangeCart, cartScope, lineItemFor, registerCartRemoval, requireCart } from "@dataset/arrange/cart";
import { optionOfEachSection } from "@dataset/builders/product-configuration";
import { getCredentials } from "@dataset/dataset";
import { getFrontendContext } from "@dataset/frontend-context";
import { expect, test } from "@fixtures";

const REGISTERED_USERNAME = "acme_store_employee_1@acme.com";
const PRODUCT_IDS = ["smartphone-apple-iphone-17-256gb-black", "smartphone-apple-iphone-17-256gb-mist-blue"] as const;
const REGULAR_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black";
const CONFIGURABLE_PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai";

test.beforeEach(async () => {
  await allure.feature("Cart / Merge");
});

test.describe("cart merge (anonymous, then signed in)", () => {
  test("merge an anonymous cart into a registered user's cart", async ({
    graphqlClient,
    anonymousHttpClient,
    tokenManager,
    cleanupStack,
    frontendContext,
    dataset,
    env,
  }) => {
    const anonymousCart = await test.step("arrange: anonymous cart with two products", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [
        { productId: PRODUCT_IDS[0], quantity: 2 },
        { productId: PRODUCT_IDS[1], quantity: 1 },
      ]));
    const userContext = getFrontendContext(dataset, env.storeId, REGISTERED_USERNAME, frontendContext.userId);
    const userClient = await test.step(`arrange: sign in as ${REGISTERED_USERNAME}`, async () =>
      new GraphqlClient(
        await tokenManager.authorize(anonymousHttpClient, getCredentials(dataset, REGISTERED_USERNAME), env.storeId),
      ));
    const cartName = uniqueId("test-cart");

    const { mergeCart } = await test.step("act: merge the anonymous cart into the user's cart", () =>
      userClient.execute(MergeCartDocument, {
        command: { ...cartScope(userContext), cartName, secondCartId: anonymousCart.id },
      }));
    registerCartRemoval(userClient, cleanupStack, userContext, requireCart(mergeCart, "Merged cart").id);

    await test.step("assert: user's cart has the anonymous cart items", async () => {
      expect(mergeCart?.itemsCount).toBe(2);
      expect(lineItemFor(mergeCart, PRODUCT_IDS[0]).quantity).toBe(2);
      expect(lineItemFor(mergeCart, PRODUCT_IDS[1]).quantity).toBe(1);
    });
  });

  test("merge a cart with a configured item into a cart with a regular item", async ({
    graphqlClient,
    anonymousHttpClient,
    tokenManager,
    cleanupStack,
    frontendContext,
    dataset,
    env,
  }) => {
    const { productConfiguration } = await test.step("arrange: configuration of the configurable product", () =>
      graphqlClient.execute(ProductConfigurationDocument, {
        configurableProductId: CONFIGURABLE_PRODUCT_ID,
        ...cartScope(frontendContext),
      }));
    const selection = optionOfEachSection(
      requireFields(productConfiguration ?? undefined, ["configurationSections"], "Product configuration"),
    );
    const anonymousCart = await test.step("arrange: anonymous cart with the configured product", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: CONFIGURABLE_PRODUCT_ID, quantity: 1 }], {
        configurationSections: selection,
      }));
    const userContext = getFrontendContext(dataset, env.storeId, REGISTERED_USERNAME, frontendContext.userId);
    const userClient = await test.step(`arrange: sign in as ${REGISTERED_USERNAME}`, async () =>
      new GraphqlClient(
        await tokenManager.authorize(anonymousHttpClient, getCredentials(dataset, REGISTERED_USERNAME), env.storeId),
      ));
    const cartName = uniqueId("test-cart");
    const { addItemsCart } = await test.step("arrange: user's cart with a regular product", () =>
      userClient.execute(AddItemsCartDocument, {
        command: { ...cartScope(userContext), cartName, cartItems: [{ productId: REGULAR_PRODUCT_ID, quantity: 2 }] },
      }));
    registerCartRemoval(userClient, cleanupStack, userContext, requireCart(addItemsCart, "User cart").id);

    const { mergeCart } = await test.step("act: merge the anonymous cart into the user's cart", () =>
      userClient.execute(MergeCartDocument, {
        command: { ...cartScope(userContext), cartName, secondCartId: anonymousCart.id },
      }));

    await test.step("assert: merged cart has the regular and the configured item", async () => {
      expect(mergeCart?.itemsCount).toBe(2);
      expect(lineItemFor(mergeCart, REGULAR_PRODUCT_ID).quantity).toBe(2);
      const configuredItem = lineItemFor(mergeCart, CONFIGURABLE_PRODUCT_ID);
      expect(configuredItem.sku).toBe(`Configuration-${CONFIGURABLE_PRODUCT_ID}`);
      expect(new Set(configuredItem.configurationItems?.map((item) => item?.productId))).toEqual(
        new Set(selection.map(({ option }) => option?.productId)),
      );
    });
  });
});
