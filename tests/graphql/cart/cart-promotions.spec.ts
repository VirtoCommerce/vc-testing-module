import * as allure from "allure-js-commons";

import { AddCouponDocument, RemoveCouponDocument } from "@api/graphql/generated/graphql";
import { arrangeCart, cartScope, lineItemFor } from "@dataset/arrange/cart";
import { expect, test } from "@fixtures";

const COUPON_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black";
const COUPON_CODE = "COUPON-100-OFF";
const ITEM_DISCOUNT_PRODUCT_ID = "smartphone-samsung-galaxy-a57-5g";
const SUBTOTAL_DISCOUNT_PRODUCT_ID = "smartphone-samsung-galaxy-s26-black";
const GIFT_PRODUCT_ID = "smartphone-samsung-galaxy-a17-5g-black";
const GIFT_THRESHOLD_QUANTITY = 20;

test.beforeEach(async () => {
  await allure.feature("Cart / Promotions");
});

test.describe("cart promotions (anonymous)", () => {
  test("add and remove a coupon", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("arrange: cart with a product", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: COUPON_PRODUCT_ID, quantity: 3 }]));
    const command = { ...cartScope(frontendContext), cartId: cart.id, couponCode: COUPON_CODE };

    const { addCoupon } = await test.step(`act: add coupon ${COUPON_CODE}`, () =>
      graphqlClient.execute(AddCouponDocument, { command }));
    await test.step("assert: coupon is applied", async () => {
      expect(addCoupon?.coupons).toEqual([expect.objectContaining({ code: COUPON_CODE, isAppliedSuccessfully: true })]);
    });

    const { removeCoupon } = await test.step(`act: remove coupon ${COUPON_CODE}`, () =>
      graphqlClient.execute(RemoveCouponDocument, { command }));
    await test.step("assert: cart has no coupons", async () => {
      expect(removeCoupon?.coupons).toEqual([]);
    });
  });

  test("apply an item discount to a discounted product", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("act: add the discounted product", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [
        { productId: ITEM_DISCOUNT_PRODUCT_ID, quantity: 1 },
      ]));

    await test.step("assert: line item has a discount", async () => {
      expect(lineItemFor(cart, ITEM_DISCOUNT_PRODUCT_ID).discountAmount?.amount).toBeGreaterThan(0);
    });
  });

  test("apply a subtotal discount above the threshold", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("act: add five products that reach the threshold", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [
        { productId: SUBTOTAL_DISCOUNT_PRODUCT_ID, quantity: 5 },
      ]));

    await test.step("assert: subtotal is discounted", async () => {
      expect(cart.subTotalDiscount?.amount).toBeGreaterThan(0);
    });
  });

  test("grant a gift above the quantity threshold", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step(`act: add ${GIFT_THRESHOLD_QUANTITY} products`, () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [
        { productId: GIFT_PRODUCT_ID, quantity: GIFT_THRESHOLD_QUANTITY },
      ]));

    await test.step("assert: cart has one gift", async () => {
      expect(cart.gifts).toHaveLength(1);
    });
  });
});
