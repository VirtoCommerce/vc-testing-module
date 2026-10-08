import * as allure from "allure-js-commons";

import {
  AddBulkItemsCartDocument,
  AddItemDocument,
  RemoveCartItemDocument,
  UpdateCartQuantityDocument,
} from "@api/graphql/generated/graphql";
import { uniqueId } from "@core/unique-id";
import { arrangeCart, cartScope, lineItemFor, registerCartRemoval, requireCart } from "@dataset/arrange/cart";
import { expect, test } from "@fixtures";

const PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black";
const VARIATION_ID = "smartphone-apple-iphone-17-256gb-mist-blue";

test.beforeEach(async () => {
  await allure.feature("Cart / Items");
});

test.describe("cart items (anonymous)", () => {
  test("add several products in one mutation", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const items = [
      { productId: PRODUCT_ID, quantity: 3 },
      { productId: VARIATION_ID, quantity: 4 },
    ];

    const cart = await test.step("act: add two products", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, items));

    await test.step("assert: both products are in the cart with their quantities", async () => {
      expect(cart.items).toEqual(expect.arrayContaining(items.map((item) => expect.objectContaining(item))));
    });
  });

  for (const { title, productId } of [
    { title: "product", productId: PRODUCT_ID },
    { title: "variation", productId: VARIATION_ID },
  ]) {
    test(`add a single ${title} to a new cart`, async ({ graphqlClient, cleanupStack, frontendContext }) => {
      const { addItem } = await test.step(`act: add the ${title} ×1`, () =>
        graphqlClient.execute(AddItemDocument, {
          command: { ...cartScope(frontendContext), cartName: uniqueId("test-cart"), productId, quantity: 1 },
        }));
      const cart = requireCart(addItem, `Cart with the ${title}`);
      registerCartRemoval(graphqlClient, cleanupStack, frontendContext, cart.id);

      await test.step(`assert: a cart of the current user holds the ${title} ×1`, async () => {
        expect(cart).toMatchObject({ customerId: frontendContext.userId, itemsQuantity: 1 });
        expect(lineItemFor(cart, productId).quantity).toBe(1);
      });
    });
  }

  test("add products by SKU in bulk", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const items = [
      { productSku: PRODUCT_ID, quantity: 5 },
      { productSku: VARIATION_ID, quantity: 10 },
    ];

    const { addBulkItemsCart } = await test.step("act: add two SKUs in bulk", () =>
      graphqlClient.execute(AddBulkItemsCartDocument, {
        command: { ...cartScope(frontendContext), cartName: uniqueId("test-cart"), cartItems: items },
      }));
    const cart = requireCart(addBulkItemsCart?.cart, "Bulk cart");
    registerCartRemoval(graphqlClient, cleanupStack, frontendContext, cart.id);

    await test.step("assert: both SKUs are in the cart without errors", async () => {
      expect(addBulkItemsCart?.errors).toEqual([]);
      expect(cart.itemsQuantity).toBe(15);
      expect(cart.items).toEqual(
        expect.arrayContaining(
          items.map(({ productSku, quantity }) => expect.objectContaining({ sku: productSku, quantity })),
        ),
      );
    });
  });

  for (const { title, productId } of [
    { title: "product", productId: PRODUCT_ID },
    { title: "variation", productId: VARIATION_ID },
  ]) {
    test(`change the quantity of a ${title} line item`, async ({ graphqlClient, cleanupStack, frontendContext }) => {
      const cart = await test.step(`arrange: cart with the ${title} ×3`, () =>
        arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId, quantity: 3 }]));

      const { updateCartQuantity } = await test.step(`act: set ${title} quantity to 5`, () =>
        graphqlClient.execute(UpdateCartQuantityDocument, {
          command: { ...cartScope(frontendContext), cartId: cart.id, items: [{ productId, quantity: 5 }] },
        }));

      await test.step(`assert: cart has the ${title} ×5`, async () => {
        expect(updateCartQuantity?.items).toEqual([expect.objectContaining({ productId, quantity: 5 })]);
      });
    });
  }

  test("remove a line item", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("arrange: cart with a product", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: PRODUCT_ID, quantity: 1 }]));
    const lineItem = lineItemFor(cart, PRODUCT_ID);

    const { removeCartItem } = await test.step("act: remove the line item", () =>
      graphqlClient.execute(RemoveCartItemDocument, {
        command: { ...cartScope(frontendContext), cartId: cart.id, lineItemId: lineItem.id },
      }));

    await test.step("assert: cart is empty", async () => {
      expect(removeCartItem).toMatchObject({ itemsCount: 0, items: [] });
    });
  });
});
