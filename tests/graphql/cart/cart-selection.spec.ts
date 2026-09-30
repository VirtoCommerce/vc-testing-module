import * as allure from "allure-js-commons";

import {
  SelectCartItemsDocument,
  UnSelectAllCartItemsDocument,
  UnSelectCartItemsDocument,
} from "@api/graphql/generated/graphql";
import { arrangeCart, cartScope, lineItemFor } from "@dataset/arrange/cart";
import { expect, test } from "@fixtures";

const PRODUCT_IDS = ["smartphone-apple-iphone-17-256gb-black", "smartphone-apple-iphone-17-256gb-mist-blue"] as const;

test.beforeEach(async () => {
  await allure.feature("Cart / Item Selection");
});

test.describe("cart item selection (anonymous)", () => {
  test("unselect one line item for checkout", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("arrange: cart with two products", () =>
      arrangeCart(
        graphqlClient,
        cleanupStack,
        frontendContext,
        PRODUCT_IDS.map((productId) => ({ productId, quantity: 1 })),
      ));
    await test.step("assert: every line item is selected by default", async () => {
      expect(cart.items?.map(({ selectedForCheckout }) => selectedForCheckout)).toEqual([true, true]);
    });
    const unselected = lineItemFor(cart, PRODUCT_IDS[0]);
    const remaining = lineItemFor(cart, PRODUCT_IDS[1]);

    const { unSelectCartItems } = await test.step("act: unselect the first line item", () =>
      graphqlClient.execute(UnSelectCartItemsDocument, {
        command: { ...cartScope(frontendContext), cartId: cart.id, lineItemIds: [unselected.id] },
      }));

    await test.step("assert: only the first line item is unselected", async () => {
      expect(unSelectCartItems?.items).toEqual(
        expect.arrayContaining([
          expect.objectContaining({ id: unselected.id, selectedForCheckout: false }),
          expect.objectContaining({ id: remaining.id, selectedForCheckout: true }),
        ]),
      );
    });
  });

  test("select one line item after unselecting all", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("arrange: cart with two products", () =>
      arrangeCart(
        graphqlClient,
        cleanupStack,
        frontendContext,
        PRODUCT_IDS.map((productId) => ({ productId, quantity: 1 })),
      ));
    const { unSelectAllCartItems } = await test.step("arrange: unselect every line item", () =>
      graphqlClient.execute(UnSelectAllCartItemsDocument, {
        command: { ...cartScope(frontendContext), cartId: cart.id },
      }));
    await test.step("assert: no line item is selected", async () => {
      expect(unSelectAllCartItems?.items?.map(({ selectedForCheckout }) => selectedForCheckout)).toEqual([
        false,
        false,
      ]);
    });
    const selected = lineItemFor(cart, PRODUCT_IDS[0]);
    const remaining = lineItemFor(cart, PRODUCT_IDS[1]);

    const { selectCartItems } = await test.step("act: select the first line item", () =>
      graphqlClient.execute(SelectCartItemsDocument, {
        command: { ...cartScope(frontendContext), cartId: cart.id, lineItemIds: [selected.id] },
      }));

    await test.step("assert: only the first line item is selected", async () => {
      expect(selectCartItems?.items).toEqual(
        expect.arrayContaining([
          expect.objectContaining({ id: selected.id, selectedForCheckout: true }),
          expect.objectContaining({ id: remaining.id, selectedForCheckout: false }),
        ]),
      );
    });
  });
});
