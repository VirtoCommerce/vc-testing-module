import type { Page } from "@playwright/test";
import type { SignedInCustomerAccount } from "@fixtures";

import * as allure from "allure-js-commons";

import { arrangeDefaultCart, registerDefaultCartRemoval } from "@dataset/arrange/cart";
import { expect, test, withItems } from "@fixtures";
import { CartPage, CONFIGURED_SKU_PREFIX } from "@pages/frontend/pages/cart-page";
import { ProductPage } from "@pages/frontend/pages/product-page";
import { SignInPage } from "@pages/frontend/pages/simple-pages";

const PRODUCT_ID = "smartphone-samsung-galaxy-a57-5g";
const QUANTITY = 3;
const REGULAR_QUANTITY = 2;
const CONFIGURABLE_PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai";
const CONFIGURABLE_PRODUCT_PATH = "laptops/acer-predator-helios-neo-16-ai";
const MEMORY = "Memory";
const MEMORY_OPTION = "Samsung DDR5-4800 8GB";

test.beforeEach(async () => {
  await allure.feature("Cart / Merge (E2E)");
});

test.describe("cart merge (anonymous cart, then sign-in)", () => {
  test.describe("with a prefilled anonymous cart", () => {
    test.use({ cart: withItems([{ productId: PRODUCT_ID, quantity: QUANTITY }]) });

    test("the anonymous cart merges into the signed-in cart", async ({ page, env, customerAccount, cleanupStack }) => {
      registerDefaultCartRemoval(customerAccount.graphqlClient, cleanupStack, customerAccount.context);
      const cartPage = new CartPage(page);
      const lineItem = cartPage.lineItem(PRODUCT_ID);

      await test.step("arrange: the anonymous cart shows the product", async () => {
        await cartPage.navigate();
        await expect(lineItem.root).toBeVisible();
      });

      await test.step(`act: sign in as ${customerAccount.credentials.username}`, () => signIn(page, customerAccount));

      await test.step(`assert: the signed-in cart holds the product ×${QUANTITY}`, async () => {
        await cartPage.navigate();
        const quantityInput =
          env.quantityControl === "stepper"
            ? lineItem.quantityStepper.quantityInput
            : lineItem.addToCartButton.quantityInput;
        await expect(quantityInput).toHaveValue(String(QUANTITY));
      });
    });
  });

  test("an anonymous configured product merges into a signed-in cart with a regular product", async ({
    page,
    customerAccount,
    cleanupStack,
  }) => {
    await test.step(`arrange: the customer's cart holds ${PRODUCT_ID} ×${REGULAR_QUANTITY}`, () =>
      arrangeDefaultCart(customerAccount.graphqlClient, cleanupStack, customerAccount.context, [
        { productId: PRODUCT_ID, quantity: REGULAR_QUANTITY },
      ]));
    registerDefaultCartRemoval(customerAccount.graphqlClient, cleanupStack, customerAccount.context);
    const productPage = new ProductPage(page, CONFIGURABLE_PRODUCT_PATH);

    await test.step("arrange: add a configured product as the anonymous shopper", async () => {
      await productPage.navigate();
      await productPage.configuration.selectOption(MEMORY, MEMORY_OPTION);
      await productPage.addToCartButton.click();
      await expect(productPage.cartQuantityLabel).toHaveText("1");
    });

    await test.step(`act: sign in as ${customerAccount.credentials.username}`, () => signIn(page, customerAccount));

    await test.step("assert: the cart holds the regular and the configured product", async () => {
      const cartPage = new CartPage(page);
      await cartPage.navigate();
      await expect(cartPage.lineItems).toHaveCount(2);
      await expect(cartPage.lineItem(PRODUCT_ID).root).toBeVisible();
      await expect(cartPage.lineItem(`${CONFIGURED_SKU_PREFIX}${CONFIGURABLE_PRODUCT_ID}`).root).toBeVisible();
    });
  });
});

async function signIn(page: Page, account: SignedInCustomerAccount): Promise<void> {
  await new SignInPage(page).signIn(account.credentials.username, account.credentials.password);
  await page.waitForURL((url) => !url.pathname.startsWith("/sign-in"));
}
