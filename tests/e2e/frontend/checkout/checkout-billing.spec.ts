import * as allure from "allure-js-commons";

import { TEST_ADDRESS } from "@dataset/builders/address";
import { expect, test, withItems } from "@fixtures";
import { CheckoutFlow } from "@pages/frontend/checkout-flow";
import { EditAddressModal } from "@pages/frontend/components/edit-address-modal";
import { SelectAddressModal } from "@pages/frontend/components/select-address-modal";

import {
  ADDRESS_FILTERS,
  applyAddressFilter,
  arrangeSavedOrganizationAddress,
  FIXED_RATE_GROUND,
  PRODUCT_ID,
  QUANTITY,
  SAVED_ADDRESS,
} from "./checkout-support";

test.beforeEach(async () => {
  await allure.feature("Checkout / Billing address (E2E)");
});

test.describe("checkout billing (anonymous)", () => {
  test.use({ cart: withItems([{ productId: PRODUCT_ID, quantity: QUANTITY }]) });

  test("the billing address mirrors the shipping address", async ({ page, env }) => {
    const flow = new CheckoutFlow(page, env.checkoutMode);
    const editAddressModal = new EditAddressModal(page);

    await test.step(`arrange: ship to a new address on the ${env.checkoutMode} checkout`, async () => {
      await flow.start();
      await flow.shippingDetails.shippingSwitcher.click();
      await flow.shippingDetails.shippingAddressButton.click();
      await editAddressModal.addressForm.fill(TEST_ADDRESS);
      await editAddressModal.submitButton.click();
      await expect(flow.shippingDetails.shippingAddressLabel).toContainText(TEST_ADDRESS.line1);
      await flow.shippingDetails.selectShippingMethod(FIXED_RATE_GROUND);
    });

    await test.step("act: continue to the payment details", () => flow.continueToPayment());

    await test.step("assert: billing is the same as shipping", async () => {
      await expect(flow.paymentDetails.billingEqualsShippingCheckbox).toBeVisible();
      await expect(flow.paymentDetails.selectedAddressLabel).toContainText(TEST_ADDRESS.line1);
    });
  });
});

test.describe("checkout billing (customer account with a saved address)", () => {
  test.use({
    shopperAccount: "customer-account",
    cart: withItems([{ productId: PRODUCT_ID, quantity: QUANTITY }]),
  });

  for (const { title, filter } of ADDRESS_FILTERS) {
    test(`filter saved billing addresses by ${title}`, async ({ page, env, customerAccount }) => {
      await arrangeSavedOrganizationAddress(customerAccount);
      const flow = new CheckoutFlow(page, env.checkoutMode);
      const selectAddressModal = new SelectAddressModal(page);

      await test.step(`arrange: ship to ${SAVED_ADDRESS.line1} on the ${env.checkoutMode} checkout`, async () => {
        await flow.start();
        await flow.shippingDetails.shippingSwitcher.click();
        await flow.shippingDetails.shippingAddressButton.click();
        await selectAddressModal.address(SAVED_ADDRESS.line1).click();
        await selectAddressModal.okButton.click();
        await expect(selectAddressModal.root).toBeHidden();
        await flow.shippingDetails.selectShippingMethod(FIXED_RATE_GROUND);
        await flow.continueToPayment();
      });

      await test.step("arrange: open a separate billing address selection", async () => {
        await flow.paymentDetails.useSeparateBillingAddress();
        await flow.paymentDetails.selectAddressButton.click();
        await expect(selectAddressModal.root).toBeVisible();
      });

      await applyAddressFilter(selectAddressModal.filters, filter);

      await test.step(`assert: ${SAVED_ADDRESS.line1} matches the filter`, async () => {
        await expect(selectAddressModal.address(SAVED_ADDRESS.line1)).toBeVisible();
      });
    });
  }
});
