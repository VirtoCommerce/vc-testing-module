import * as allure from "allure-js-commons";

import { expect, test } from "@fixtures";
import { LineItem } from "@pages/frontend/components/line-item";
import { CartPage, CONFIGURED_SKU_PREFIX } from "@pages/frontend/pages/cart-page";
import { ProductPage } from "@pages/frontend/pages/product-page";
import { isGraphqlOperation } from "@pages/graphql-traffic";

const PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai";
const PRODUCT_PATH = "laptops/acer-predator-helios-neo-16-ai";
const CONFIGURED_SKU = `${CONFIGURED_SKU_PREFIX}${PRODUCT_ID}`;
const MEMORY = "Memory";
const STORAGE = "Storage";
const MEMORY_OPTION = "Samsung DDR5-4800 8GB";
const OTHER_MEMORY_OPTION = "Crucial DDR5-4800 16GB";
const STORAGE_OPTION = "Kingston FURY Renegade G5 PCIe 5.0 NVMe M.2 SSD 1024GB";

test.beforeEach(async () => {
  await allure.feature("Catalog / Product configuration (E2E)");
});

test.describe("configurable product (anonymous)", () => {
  test("configure a product and add it to the cart", async ({ page }) => {
    const productPage = new ProductPage(page, PRODUCT_PATH);
    const memory = productPage.configuration.section(MEMORY);
    const storage = productPage.configuration.section(STORAGE);

    await test.step("arrange: open the configurable product", async () => {
      await productPage.navigate();
      await expect(productPage.configuration.root).toBeVisible();
    });

    await test.step(`assert: ${MEMORY} and ${STORAGE} are required sections`, async () => {
      await expect(memory.requiredMark).toHaveCount(1);
      await expect(storage.requiredMark).toHaveCount(1);
    });

    for (const [section, option] of [
      [memory, MEMORY_OPTION],
      [storage, STORAGE_OPTION],
    ] as const) {
      await test.step(`act: select ${option}`, () => section.selectOption(option));
      await test.step(`assert: the section shows ${option} as selected`, async () => {
        await expect(section.selectedOptionLabel).toHaveText(option);
      });
    }

    await test.step("assert: the configuration has a total price", async () => {
      await expect(productPage.totalPrice).toHaveText(/\d/);
    });

    await test.step("act: add the configured product to the cart", () => productPage.addToCartButton.click());

    await test.step("assert: the cart holds one configured line item", async () => {
      await expect(productPage.cartQuantityLabel).toHaveText("1");
      const cartPage = new CartPage(page);
      await cartPage.navigate();
      await expect(cartPage.lineItems).toHaveCount(1);
      await expect(cartPage.lineItem(CONFIGURED_SKU).root).toBeVisible();
    });
  });

  test("two configurations of one product are separate line items", async ({ page }) => {
    const productPage = new ProductPage(page, PRODUCT_PATH);
    const cartPage = new CartPage(page);

    for (const [option, badge] of [
      [MEMORY_OPTION, "1"],
      [OTHER_MEMORY_OPTION, "2"],
    ] as const) {
      await test.step(`arrange: add a configuration with ${option}`, () => addConfiguration(productPage, option));
      await test.step(`assert: the cart badge shows ${badge}`, async () => {
        await expect(productPage.cartQuantityLabel).toHaveText(badge);
      });
    }

    await test.step("act: open the cart and expand both component lists", async () => {
      await cartPage.navigate();
      await expect(cartPage.configuredLineItems(PRODUCT_ID)).toHaveCount(2);
      for (const index of [0, 1]) {
        await new LineItem(cartPage.configuredLineItems(PRODUCT_ID).nth(index)).expandComponents();
      }
    });

    await test.step("assert: each line item carries its own memory option", async () => {
      await expect(cartPage.configuredLineItem(PRODUCT_ID, MEMORY_OPTION).root).toBeVisible();
      await expect(cartPage.configuredLineItem(PRODUCT_ID, OTHER_MEMORY_OPTION).root).toBeVisible();
    });
  });

  test("remove a configured line item", async ({ page }) => {
    const productPage = new ProductPage(page, PRODUCT_PATH);
    const cartPage = new CartPage(page);
    const lineItem = cartPage.lineItem(CONFIGURED_SKU);

    await test.step("arrange: add a configuration and open the cart", async () => {
      await addConfiguration(productPage, MEMORY_OPTION);
      await expect(productPage.cartQuantityLabel).toHaveText("1");
      await cartPage.navigate();
    });

    await test.step("act: remove the configured line item", () => lineItem.removeButton.click());

    await test.step("assert: the cart is empty", async () => {
      await expect(cartPage.lineItems).toHaveCount(0);
    });
  });

  test("edit a configuration from the cart", async ({ page }) => {
    const productPage = new ProductPage(page, PRODUCT_PATH);
    const cartPage = new CartPage(page);
    const lineItem = cartPage.lineItem(CONFIGURED_SKU);

    await test.step(`arrange: add a configuration with ${MEMORY_OPTION} and open the cart`, async () => {
      await addConfiguration(productPage, MEMORY_OPTION);
      await expect(productPage.cartQuantityLabel).toHaveText("1");
      await cartPage.navigate();
      await lineItem.expandComponents();
      await expect(lineItem.root).toContainText(MEMORY_OPTION);
    });

    await test.step("act: edit the configuration from the line item", async () => {
      await lineItem.expandComponents();
      await lineItem.editConfigurationLink.click();
      await expect(productPage.configuration.section(MEMORY).selectedOptionLabel).toHaveText(MEMORY_OPTION);
    });

    await test.step(`act: switch the memory to ${OTHER_MEMORY_OPTION} and update the cart`, async () => {
      const memory = await productPage.configuration.selectOption(MEMORY, OTHER_MEMORY_OPTION);
      await expect(memory.radio).toBeChecked();
      await expect(productPage.configuration.section(MEMORY).selectedOptionLabel).toHaveText(OTHER_MEMORY_OPTION);
      await expect(productPage.updateCartButton).toBeEnabled();
      await Promise.all([
        page.waitForResponse(isGraphqlOperation("ChangeCartConfiguredItem")),
        productPage.updateCartButton.click(),
      ]);
    });

    await test.step("assert: the cart still has one line item with the new memory", async () => {
      await cartPage.navigate();
      await expect(cartPage.configuredLineItems(PRODUCT_ID)).toHaveCount(1);
      await lineItem.expandComponents();
      await expect(lineItem.root).toContainText(OTHER_MEMORY_OPTION);
      await expect(lineItem.root).not.toContainText(MEMORY_OPTION);
    });
  });
});

async function addConfiguration(productPage: ProductPage, memoryOption: string): Promise<void> {
  await productPage.navigate();
  await expect(productPage.configuration.root).toBeVisible();
  await productPage.configuration.selectOption(MEMORY, memoryOption);
  await productPage.addToCartButton.click();
}
