import * as allure from "allure-js-commons";

import { expect, test, withItems } from "@fixtures";
import { CartPage } from "@pages/frontend/pages/cart-page";
import { isGraphqlOperation } from "@pages/graphql-traffic";

const PRODUCT_ID = "smartphone-samsung-galaxy-a57-5g";
const QUANTITY = 3;

test.beforeEach(async () => {
  await allure.feature("Cart / Lifecycle (E2E)");
});

test.describe("cart lifecycle (anonymous)", () => {
  test.use({ cart: withItems([{ productId: PRODUCT_ID, quantity: QUANTITY }]) });

  test("clear every item from the cart", async ({ page }) => {
    const cartPage = new CartPage(page);

    await test.step("arrange: open the cart with the prefilled line item", async () => {
      await cartPage.navigate();
      await expect(cartPage.lineItems).toHaveCount(1);
      await expect(cartPage.clearCartButton).toBeEnabled();
    });

    await test.step("act: confirm clear cart in the modal", async () => {
      await cartPage.clearCartButton.click();
      await expect(cartPage.clearCartModal.confirmButton).toBeEnabled();
      await Promise.all([
        page.waitForResponse(isGraphqlOperation("ClearCart")),
        cartPage.clearCartModal.confirmButton.click(),
      ]);
    });

    await test.step("assert: the modal closes and no line items remain", async () => {
      await expect(cartPage.clearCartModal.root).toBeHidden();
      await expect(cartPage.lineItems).toHaveCount(0);
    });
  });

  test("remove a line item from the cart", async ({ page }) => {
    const cartPage = new CartPage(page);
    const lineItem = cartPage.lineItem(PRODUCT_ID);

    await test.step(`arrange: open the cart with ${PRODUCT_ID}`, async () => {
      await cartPage.navigate();
      await expect(lineItem.removeButton).toBeVisible();
    });

    await test.step("act: remove the line item", () => lineItem.removeButton.click());

    await test.step("assert: the line item is gone", async () => {
      await expect(lineItem.root).toBeHidden();
    });
  });
});
