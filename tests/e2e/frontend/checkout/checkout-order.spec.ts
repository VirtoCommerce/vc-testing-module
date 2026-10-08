import * as allure from "allure-js-commons";

import { OrdersClient } from "@api/rest/clients/orders-client";
import { TEST_ADDRESS } from "@dataset/builders/address";
import { expect, test, withItems } from "@fixtures";
import { CheckoutFlow } from "@pages/frontend/checkout-flow";
import { EditAddressModal } from "@pages/frontend/components/edit-address-modal";

import { FIXED_RATE_GROUND, MANUAL_PAYMENT_METHOD, PRODUCT_ID, QUANTITY } from "./checkout-support";

const ORDER_NUMBER_ATTRIBUTE = "data-order-number";

test.beforeEach(async () => {
  await allure.feature("Checkout / Order creation (E2E)");
});

test.describe("checkout payment and order (anonymous)", () => {
  test.use({ cart: withItems([{ productId: PRODUCT_ID, quantity: QUANTITY }]) });

  test("select the manual payment method", async ({ page, env }) => {
    const flow = new CheckoutFlow(page, env.checkoutMode);

    await test.step(`arrange: reach the payment details on the ${env.checkoutMode} checkout`, () =>
      shipToTestAddress(flow, new EditAddressModal(page)));

    await test.step(`act: select ${MANUAL_PAYMENT_METHOD}`, () =>
      flow.paymentDetails.selectPaymentMethod(MANUAL_PAYMENT_METHOD));

    await test.step(`assert: ${MANUAL_PAYMENT_METHOD} is selected`, async () => {
      await expect(flow.paymentDetails.selectedPaymentMethod(MANUAL_PAYMENT_METHOD)).toBeVisible();
    });
  });

  test("place an order", async ({ page, env, platformAdminHttpClient, cleanupStack }) => {
    const flow = new CheckoutFlow(page, env.checkoutMode);

    await test.step(`arrange: ship and pay on the ${env.checkoutMode} checkout`, async () => {
      await shipToTestAddress(flow, new EditAddressModal(page));
      await flow.paymentDetails.selectPaymentMethod(MANUAL_PAYMENT_METHOD);
      await expect(flow.paymentDetails.selectedPaymentMethod(MANUAL_PAYMENT_METHOD)).toBeVisible();
    });

    await test.step("act: place the order", () => flow.placeOrder());

    await test.step("assert: the completed page shows the new order number", async () => {
      await expect(flow.completedPage.createdOrderNumberLabel).toHaveAttribute(ORDER_NUMBER_ATTRIBUTE, /\S/);
    });
    const orderNumber = await flow.completedPage.createdOrderNumberLabel.getAttribute(ORDER_NUMBER_ATTRIBUTE);
    if (orderNumber !== null) {
      const ordersClient = new OrdersClient(platformAdminHttpClient);
      cleanupStack.push(`delete order ${orderNumber}`, async () => {
        await ordersClient.delete((await ordersClient.getByNumber(orderNumber)).id);
      });
    }
  });
});

async function shipToTestAddress(flow: CheckoutFlow, editAddressModal: EditAddressModal): Promise<void> {
  await flow.start();
  await flow.shippingDetails.shippingSwitcher.click();
  await flow.shippingDetails.shippingAddressButton.click();
  await editAddressModal.addressForm.fill(TEST_ADDRESS);
  await editAddressModal.submitButton.click();
  await expect(flow.shippingDetails.shippingAddressLabel).toContainText(TEST_ADDRESS.line1);
  await flow.shippingDetails.selectShippingMethod(FIXED_RATE_GROUND);
  await expect(flow.shippingDetails.selectedShippingMethod(FIXED_RATE_GROUND)).toBeVisible();
  await flow.continueToPayment();
}
