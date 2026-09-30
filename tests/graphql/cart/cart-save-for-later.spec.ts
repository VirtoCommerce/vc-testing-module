import * as allure from "allure-js-commons";

import {
  GetSavedForLaterDocument,
  MoveFromSavedForLaterDocument,
  MoveToSavedForLaterDocument,
} from "@api/graphql/generated/graphql";
import { requireFields } from "@core/required-fields";
import { arrangeCart, cartScope, lineItemFor, registerCartRemoval, requireCart } from "@dataset/arrange/cart";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const REGISTERED_USERNAME = "acme_store_maintainer_1@acme.com";
const PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black";

test.beforeEach(async () => {
  await allure.feature("Cart / Save For Later");
});

test.describe("save for later (registered user)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, REGISTERED_USERNAME)) });

  test("move a line item to saved for later and back", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("arrange: cart with a product", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: PRODUCT_ID, quantity: 1 }]));

    const { moveToSavedForLater } = await test.step("act: move the line item to saved for later", () =>
      graphqlClient.execute(MoveToSavedForLaterDocument, {
        command: { ...cartScope(frontendContext), cartId: cart.id, lineItemIds: [lineItemFor(cart, PRODUCT_ID).id] },
      }));
    const savedList = requireFields(moveToSavedForLater?.list ?? undefined, ["id"], "Saved for later list");
    registerCartRemoval(graphqlClient, cleanupStack, frontendContext, savedList.id);
    await test.step("assert: product left the cart for the saved list", async () => {
      expect(moveToSavedForLater?.cart?.itemsCount).toBe(0);
      expect(savedList.items).toEqual([expect.objectContaining({ productId: PRODUCT_ID })]);
    });

    const { moveFromSavedForLater } = await test.step("act: move the product back to the cart", () =>
      graphqlClient.execute(MoveFromSavedForLaterDocument, {
        command: {
          ...cartScope(frontendContext),
          cartId: savedList.id,
          lineItemIds: [lineItemFor(savedList, PRODUCT_ID).id],
        },
      }));
    registerCartRemoval(
      graphqlClient,
      cleanupStack,
      frontendContext,
      requireCart(moveFromSavedForLater?.cart, "Cart after moving back").id,
    );
    await test.step("assert: product is back in the cart and the saved list is empty", async () => {
      expect(moveFromSavedForLater?.list?.itemsCount).toBe(0);
      expect(moveFromSavedForLater?.cart?.items).toEqual([expect.objectContaining({ productId: PRODUCT_ID })]);
    });
  });
});

test.describe("save for later (customer account)", () => {
  test("read the saved-for-later list", async ({ customerAccount, cleanupStack }) => {
    const { graphqlClient, context } = customerAccount;
    const cart = await test.step("arrange: cart with a product", () =>
      arrangeCart(graphqlClient, cleanupStack, context, [{ productId: PRODUCT_ID, quantity: 1 }]));
    await test.step("arrange: move the line item to saved for later", async () => {
      const { moveToSavedForLater } = await graphqlClient.execute(MoveToSavedForLaterDocument, {
        command: { ...cartScope(context), cartId: cart.id, lineItemIds: [lineItemFor(cart, PRODUCT_ID).id] },
      });
      registerCartRemoval(
        graphqlClient,
        cleanupStack,
        context,
        requireCart(moveToSavedForLater?.list, "Saved list").id,
      );
    });

    const { getSavedForLater } = await test.step("act: get the saved-for-later list", () =>
      graphqlClient.execute(GetSavedForLaterDocument, cartScope(context)));

    await test.step("assert: the list holds exactly the saved product", async () => {
      expect(getSavedForLater).toMatchObject({ customerId: customerAccount.userId, itemsQuantity: 1 });
      expect(getSavedForLater?.items).toEqual([expect.objectContaining({ productId: PRODUCT_ID, quantity: 1 })]);
    });
  });
});
