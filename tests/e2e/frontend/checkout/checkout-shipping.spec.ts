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
  FIXED_RATE_AIR,
  FIXED_RATE_GROUND,
  PRODUCT_ID,
  QUANTITY,
  SAVED_ADDRESS,
} from "./checkout-support";

const SHIPPING_COSTS = [
  { code: FIXED_RATE_GROUND, cost: "15" },
  { code: FIXED_RATE_AIR, cost: "25" },
] as const;

test.beforeEach(async () => {
  await allure.feature("Checkout / Shipping (E2E)");
});

test.describe("checkout shipping (anonymous)", () => {
  test.use({ cart: withItems([{ productId: PRODUCT_ID, quantity: QUANTITY }]) });

  test("switch between shipping and pickup", async ({ page, env }) => {
    const flow = new CheckoutFlow(page, env.checkoutMode);
    const { shippingDetails } = flow;

    await test.step(`arrange: open the ${env.checkoutMode} checkout`, () => flow.start());
    await test.step("assert: both delivery options are offered", async () => {
      await expect(shippingDetails.shippingSwitcher).toBeVisible();
      await expect(shippingDetails.pickupSwitcher).toBeVisible();
    });

    await test.step("act: choose shipping", () => shippingDetails.shippingSwitcher.click());
    await test.step("assert: the shipping address section is shown", async () => {
      await expect(shippingDetails.shippingAddressSection).toBeVisible();
    });

    await test.step("act: choose pickup", () => shippingDetails.pickupSwitcher.click());
    await test.step("assert: the pickup location section is shown", async () => {
      await expect(shippingDetails.pickupLocationSection).toBeVisible();
    });
  });

  test("switch between FixedRate Ground and Air", async ({ page, env }) => {
    const flow = new CheckoutFlow(page, env.checkoutMode);

    await test.step(`arrange: open the ${env.checkoutMode} checkout with shipping`, async () => {
      await flow.start();
      await flow.shippingDetails.shippingSwitcher.click();
      await expect(flow.shippingDetails.shippingMethodSelector).toBeVisible();
    });

    for (const { code, cost } of SHIPPING_COSTS) {
      await test.step(`act: select ${code}`, () => flow.shippingDetails.selectShippingMethod(code));
      await test.step(`assert: ${code} is selected and shipping costs ${cost}`, async () => {
        await expect(flow.shippingDetails.selectedShippingMethod(code)).toBeVisible();
        await expect(flow.shippingCostLabel).toContainText(cost);
      });
    }
  });

  test("add a new shipping address", async ({ page, env }) => {
    const flow = new CheckoutFlow(page, env.checkoutMode);
    const editAddressModal = new EditAddressModal(page);

    await test.step(`arrange: open the ${env.checkoutMode} checkout with shipping`, async () => {
      await flow.start();
      await flow.shippingDetails.shippingSwitcher.click();
    });

    await test.step("act: fill and submit a new address", async () => {
      await flow.shippingDetails.shippingAddressButton.click();
      await editAddressModal.addressForm.fill(TEST_ADDRESS);
      await editAddressModal.submitButton.click();
    });

    await test.step("assert: the new address is the shipping address", async () => {
      await expect(editAddressModal.root).toBeHidden();
      await expect(flow.shippingDetails.shippingAddressLabel).toContainText(TEST_ADDRESS.line1);
    });
  });
});

test.describe("checkout shipping (customer account with a saved address)", () => {
  test.use({
    shopperAccount: "customer-account",
    cart: withItems([{ productId: PRODUCT_ID, quantity: QUANTITY }]),
  });

  test("pick a saved shipping address", async ({ page, env, customerAccount }) => {
    await arrangeSavedOrganizationAddress(customerAccount);
    const flow = new CheckoutFlow(page, env.checkoutMode);
    const selectAddressModal = new SelectAddressModal(page);

    await test.step(`arrange: open the ${env.checkoutMode} checkout with shipping`, async () => {
      await flow.start();
      await flow.shippingDetails.shippingSwitcher.click();
      await flow.shippingDetails.shippingAddressButton.click();
    });

    await test.step(`act: pick ${SAVED_ADDRESS.line1} and confirm`, async () => {
      await selectAddressModal.address(SAVED_ADDRESS.line1).click();
      await selectAddressModal.okButton.click();
    });

    await test.step("assert: the saved address is the shipping address", async () => {
      await expect(selectAddressModal.root).toBeHidden();
      await expect(flow.shippingDetails.shippingAddressLabel).toContainText(SAVED_ADDRESS.line1);
    });
  });

  for (const { title, filter } of ADDRESS_FILTERS) {
    test(`filter saved shipping addresses by ${title}`, async ({ page, env, customerAccount }) => {
      await arrangeSavedOrganizationAddress(customerAccount);
      const flow = new CheckoutFlow(page, env.checkoutMode);
      const selectAddressModal = new SelectAddressModal(page);

      await test.step(`arrange: open the saved addresses on the ${env.checkoutMode} checkout`, async () => {
        await flow.start();
        await flow.shippingDetails.shippingSwitcher.click();
        await flow.shippingDetails.shippingAddressButton.click();
        await expect(selectAddressModal.root).toBeVisible();
      });

      await applyAddressFilter(selectAddressModal.filters, filter);

      await test.step(`assert: ${SAVED_ADDRESS.line1} matches the filter`, async () => {
        await expect(selectAddressModal.address(SAVED_ADDRESS.line1)).toBeVisible();
      });
    });
  }
});
