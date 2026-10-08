import * as allure from "allure-js-commons";

import { expect, test, withItems } from "@fixtures";
import { AccountSavedForLaterPage } from "@pages/frontend/pages/account-pages";
import { CartPage } from "@pages/frontend/pages/cart-page";
import { isGraphqlMutation } from "@pages/graphql-traffic";

const PRODUCT_ID = "smartphone-samsung-galaxy-a57-5g";
const ORIGINAL_QUANTITY = 3;
const UPDATED_QUANTITY = 4;

test.beforeEach(async () => {
  await allure.feature("Cart / Line items (E2E)");
});

test.describe("cart line items (customer account)", () => {
  test.use({
    shopperAccount: "customer-account",
    cart: withItems([{ productId: PRODUCT_ID, quantity: ORIGINAL_QUANTITY }]),
  });

  test("change the quantity with the stepper", async ({ page, env }) => {
    test.skip(env.quantityControl !== "stepper", "The frontend renders the add-to-cart button, not the stepper");
    const cartPage = new CartPage(page);
    const { quantityStepper } = cartPage.lineItem(PRODUCT_ID);

    await test.step(`arrange: open the cart with ${PRODUCT_ID} ×${ORIGINAL_QUANTITY}`, async () => {
      await cartPage.navigate();
      await expect(quantityStepper.quantityInput).toHaveValue(String(ORIGINAL_QUANTITY));
    });

    await test.step("act: increment the quantity", () =>
      Promise.all([page.waitForResponse(isGraphqlMutation()), quantityStepper.incrementButton.click()]));

    await test.step(`assert: the cart badge shows ${UPDATED_QUANTITY}`, async () => {
      await expect(cartPage.cartQuantityLabel).toHaveText(String(UPDATED_QUANTITY));
    });
  });

  test("change the quantity with the add-to-cart button input", async ({ page, env }) => {
    test.skip(env.quantityControl !== "button", "The frontend renders the stepper, not the add-to-cart button");
    const cartPage = new CartPage(page);
    const { addToCartButton } = cartPage.lineItem(PRODUCT_ID);

    await test.step(`arrange: open the cart with ${PRODUCT_ID} ×${ORIGINAL_QUANTITY}`, async () => {
      await cartPage.navigate();
      await expect(addToCartButton.quantityInput).toHaveValue(String(ORIGINAL_QUANTITY));
    });

    await test.step(`act: type ${UPDATED_QUANTITY} and leave the input`, async () => {
      await addToCartButton.quantityInput.fill(String(UPDATED_QUANTITY));
      await cartPage.clickOutside();
    });

    await test.step(`assert: the cart badge shows ${UPDATED_QUANTITY}`, async () => {
      await expect(cartPage.cartQuantityLabel).toHaveText(String(UPDATED_QUANTITY));
    });
  });

  test("save a line item for later and remove it from the saved list", async ({ page }) => {
    const cartPage = new CartPage(page);
    const savedForLaterPage = new AccountSavedForLaterPage(page);

    await test.step("act: save the line item for later", async () => {
      await cartPage.navigate();
      await cartPage.lineItem(PRODUCT_ID).saveForLaterButton.click();
    });

    await test.step("assert: the cart is empty", async () => {
      await expect(cartPage.lineItems).toHaveCount(0);
    });

    const savedItem = savedForLaterPage.lineItem(PRODUCT_ID);
    await test.step("assert: the saved-for-later list holds the product", async () => {
      await savedForLaterPage.navigate();
      await expect(savedForLaterPage.lineItems).toHaveCount(1);
      await expect(savedItem.root).toBeVisible();
    });

    await test.step("act: remove the saved item and confirm", async () => {
      await savedItem.removeButton.click();
      await expect(savedForLaterPage.removeItemModal.root).toBeVisible();
      await savedForLaterPage.removeItemModal.confirmButton.click();
    });

    await test.step("assert: the saved item is gone", async () => {
      await expect(savedItem.root).toBeHidden();
    });
  });
});
