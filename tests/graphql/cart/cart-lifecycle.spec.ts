import * as allure from "allure-js-commons";

import { ClearCartDocument, GetCartDocument } from "@api/graphql/generated/graphql";
import { uniqueId } from "@core/unique-id";
import { arrangeCart, cartScope } from "@dataset/arrange/cart";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const REGISTERED_USERNAME = "acme_store_maintainer_1@acme.com";
const PRODUCT_ID = "smartphone-apple-iphone-17-256gb-mist-blue";

test.beforeEach(async () => {
  await allure.feature("Cart / Lifecycle");
});

test.describe("cart lifecycle (anonymous)", () => {
  test("a cart that was never created is null", async ({ graphqlClient, frontendContext }) => {
    const cartName = uniqueId("test-missing-cart");

    const { cart } = await test.step(`act: get cart ${cartName}`, () =>
      graphqlClient.execute(GetCartDocument, { ...cartScope(frontendContext), cartName }));

    await test.step("assert: there is no cart", async () => {
      expect(cart).toBeNull();
    });
  });

  test("get the cart of an anonymous user", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("act: create cart with a product", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: PRODUCT_ID, quantity: 1 }]));

    await test.step("assert: cart is anonymous", async () => {
      expect(cart).toMatchObject({ isAnonymous: true, customerId: frontendContext.userId });
    });
  });

  test("clear a cart", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("arrange: cart with a product", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: PRODUCT_ID, quantity: 3 }]));

    const { clearCart } = await test.step("act: clear cart", () =>
      graphqlClient.execute(ClearCartDocument, { command: { ...cartScope(frontendContext), cartId: cart.id } }));

    await test.step("assert: cart is empty", async () => {
      expect(clearCart).toMatchObject({ id: cart.id, itemsCount: 0, items: [] });
    });
  });
});

test.describe("cart lifecycle (registered user)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, REGISTERED_USERNAME)) });

  test("get the cart of a registered user", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("act: create cart with a product", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: PRODUCT_ID, quantity: 1 }]));

    await test.step("assert: cart belongs to the registered user", async () => {
      expect(cart).toMatchObject({ isAnonymous: false, customerId: frontendContext.userId });
    });
  });
});
