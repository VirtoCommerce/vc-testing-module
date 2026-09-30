import * as allure from "allure-js-commons";

import { expect, test } from "@fixtures";
import { CategoryPage } from "@pages/frontend/pages/category-page";
import { ProductPage } from "@pages/frontend/pages/product-page";
import { isGraphqlMutation } from "@pages/graphql-traffic";

const SMARTPHONES = "smartphones";
const LAPTOPS = "laptops";
const PRODUCT_SKU = "smartphone-samsung-galaxy-a57-5g";
const CONFIGURABLE_SKU = "laptop-acer-predator-helios-neo-16-ai";
const CONFIGURABLE_SLUG = "acer-predator-helios-neo-16-ai";
const VARIATIONS_PARENT_SKU = "smartphone-google-pixel-10-frost";
const VARIATION_SKUS = ["smartphone-google-pixel-10-indigo", "smartphone-google-pixel-10-lemongrass"] as const;
const PRICE_RANGE = { from: "1000", to: "2000" } as const;
const PRICE_FACETS = ["filter-price-[1000 TO 1300)", "filter-price-[1300 TO 1500)", "filter-price-[1500 TO 2000)"];
const PRODUCTS_IN_PRICE_RANGE = "4";
const NARROW_VIEWPORT = { width: 800, height: 600 };

test.beforeEach(async () => {
  await allure.feature("Catalog / Category (E2E)");
});

test.describe("category page (anonymous)", () => {
  test("switch between grid and list views", async ({ page }) => {
    const categoryPage = new CategoryPage(page, SMARTPHONES);
    await test.step(`arrange: open ${SMARTPHONES}`, () => categoryPage.navigate());

    await test.step("act: switch to grid view", () => categoryPage.viewSwitcher.gridViewTab.click());
    await test.step("assert: products are shown as a grid", async () => {
      await expect(categoryPage.gridView).toBeVisible();
    });

    await test.step("act: switch to list view", () => categoryPage.viewSwitcher.listViewTab.click());
    await test.step("assert: products are shown as a list", async () => {
      await expect(categoryPage.listView).toBeVisible();
    });
  });

  test("filter products by price with the slider", async ({ page, env }) => {
    test.skip(env.rangeFilterType !== "slider", "The frontend renders price checkboxes, not the slider");
    const categoryPage = new CategoryPage(page, SMARTPHONES);
    const { priceFilter } = categoryPage;

    await test.step(`arrange: open ${SMARTPHONES} and expand the price filter`, async () => {
      await categoryPage.navigate();
      await priceFilter.header.click();
      await expect(priceFilter.content).toBeVisible();
    });

    await test.step(`act: set the range ${PRICE_RANGE.from}–${PRICE_RANGE.to}`, async () => {
      await priceFilter.startInput.fill(PRICE_RANGE.from);
      await priceFilter.endInput.fill(PRICE_RANGE.to);
      await categoryPage.clickOutside();
    });

    await test.step(`assert: ${PRODUCTS_IN_PRICE_RANGE} products are in range`, async () => {
      await expect(categoryPage.productsCountLabel).toHaveText(PRODUCTS_IN_PRICE_RANGE);
    });
  });

  test("filter products by price with the checkboxes", async ({ page, env }) => {
    test.skip(env.rangeFilterType !== "default", "The frontend renders the price slider, not checkboxes");
    const categoryPage = new CategoryPage(page, SMARTPHONES);
    const { priceFilter } = categoryPage;

    await test.step(`arrange: open ${SMARTPHONES} and expand the price filter`, async () => {
      await categoryPage.navigate();
      await priceFilter.header.click();
      await expect(priceFilter.content).toBeVisible();
    });

    await test.step(`act: tick the facets covering ${PRICE_RANGE.from}–${PRICE_RANGE.to}`, async () => {
      for (const facet of PRICE_FACETS) {
        await priceFilter.facet(facet).click();
      }
    });

    await test.step(`assert: ${PRODUCTS_IN_PRICE_RANGE} products are in range`, async () => {
      await expect(categoryPage.productsCountLabel).toHaveText(PRODUCTS_IN_PRICE_RANGE);
    });
  });

  test("the stepper stays visible in a narrow viewport", async ({ page, env }) => {
    test.skip(env.quantityControl !== "stepper", "The frontend renders the add-to-cart button, not the stepper");
    const categoryPage = new CategoryPage(page, SMARTPHONES);

    const card = await test.step(`arrange: find ${PRODUCT_SKU}`, async () => {
      await categoryPage.navigate();
      return categoryPage.scrollToProduct(PRODUCT_SKU);
    });
    await expect(card.quantityStepper.root).toBeVisible();

    await test.step("act: narrow the viewport", () => page.setViewportSize(NARROW_VIEWPORT));

    await test.step("assert: the stepper is still visible", async () => {
      await expect(card.quantityStepper.root).toBeVisible();
    });
  });

  test("the add-to-cart button collapses to an icon in a narrow viewport", async ({ page, env }) => {
    test.skip(env.quantityControl !== "button", "The frontend renders the stepper, not the add-to-cart button");
    const categoryPage = new CategoryPage(page, SMARTPHONES);

    const card = await test.step(`arrange: find ${PRODUCT_SKU}`, async () => {
      await categoryPage.navigate();
      return categoryPage.scrollToProduct(PRODUCT_SKU);
    });
    await expect(card.addToCartButton.textButton).toBeVisible();

    await test.step("act: narrow the viewport", () => page.setViewportSize(NARROW_VIEWPORT));

    await test.step("assert: the icon button is shown", async () => {
      await expect(card.addToCartButton.iconButton).toBeVisible();
    });
  });

  test("change the cart from a product card with the stepper", async ({ page, env }) => {
    test.skip(env.quantityControl !== "stepper", "The frontend renders the add-to-cart button, not the stepper");
    const categoryPage = new CategoryPage(page, SMARTPHONES);

    const { quantityStepper } = await test.step(`arrange: find ${PRODUCT_SKU}`, async () => {
      await categoryPage.navigate();
      return categoryPage.scrollToProduct(PRODUCT_SKU);
    });

    for (const [button, expected] of [
      [quantityStepper.incrementButton, "1"],
      [quantityStepper.incrementButton, "2"],
      [quantityStepper.decrementButton, "1"],
    ] as const) {
      await test.step(`act and assert: the cart badge shows ${expected}`, async () => {
        await Promise.all([page.waitForResponse(isGraphqlMutation()), button.click()]);
        await expect(categoryPage.cartQuantityLabel).toHaveText(expected);
      });
    }
  });

  test("change the cart from a product card with the add-to-cart button", async ({ page, env }) => {
    test.skip(env.quantityControl !== "button", "The frontend renders the stepper, not the add-to-cart button");
    const categoryPage = new CategoryPage(page, SMARTPHONES);

    const { addToCartButton } = await test.step(`arrange: find ${PRODUCT_SKU}`, async () => {
      await categoryPage.navigate();
      return categoryPage.scrollToProduct(PRODUCT_SKU);
    });

    for (const quantity of ["1", "2"]) {
      await test.step(`act and assert: adding ${quantity} makes the cart badge show ${quantity}`, async () => {
        await addToCartButton.quantityInput.fill(quantity);
        await addToCartButton.textButton.click();
        await expect(categoryPage.cartQuantityLabel).toHaveText(quantity);
      });
    }
  });

  test("change the cart from product variations with steppers", async ({ page, env }) => {
    test.skip(env.quantityControl !== "stepper", "The frontend renders the add-to-cart button, not the stepper");
    const categoryPage = new CategoryPage(page, SMARTPHONES);

    const card = await test.step(`arrange: open the variations of ${VARIATIONS_PARENT_SKU}`, async () => {
      await categoryPage.navigate();
      await categoryPage.viewSwitcher.listViewTab.click();
      const parent = await categoryPage.scrollToProduct(VARIATIONS_PARENT_SKU);
      await parent.variationsButton.click();
      return parent;
    });
    const [firstSku, secondSku] = VARIATION_SKUS;

    for (const [sku, button, expected] of [
      [firstSku, "increment", "1"],
      [firstSku, "increment", "2"],
      [secondSku, "increment", "3"],
      [secondSku, "increment", "4"],
      [firstSku, "decrement", "3"],
      [secondSku, "decrement", "2"],
    ] as const) {
      await test.step(`act and assert: ${button} ${sku} makes the cart badge show ${expected}`, async () => {
        const { quantityStepper } = card.variation(sku);
        const control = button === "increment" ? quantityStepper.incrementButton : quantityStepper.decrementButton;
        await Promise.all([page.waitForResponse(isGraphqlMutation()), control.click()]);
        await expect(categoryPage.cartQuantityLabel).toHaveText(expected);
      });
    }
  });

  test("change the cart from product variations with add-to-cart buttons", async ({ page, env }) => {
    test.skip(env.quantityControl !== "button", "The frontend renders the stepper, not the add-to-cart button");
    const categoryPage = new CategoryPage(page, SMARTPHONES);

    const card = await test.step(`arrange: open the variations of ${VARIATIONS_PARENT_SKU}`, async () => {
      await categoryPage.navigate();
      await categoryPage.viewSwitcher.listViewTab.click();
      const parent = await categoryPage.scrollToProduct(VARIATIONS_PARENT_SKU);
      await parent.variationsButton.click();
      return parent;
    });

    let expectedTotal = 0;
    for (const sku of VARIATION_SKUS) {
      const { addToCartButton } = card.variation(sku);
      for (const quantity of [1, 2]) {
        expectedTotal += 1;
        await test.step(`act and assert: setting ${sku} to ${quantity} makes the badge show ${expectedTotal}`, async () => {
          await addToCartButton.quantityInput.fill(String(quantity));
          await addToCartButton.iconButton.click();
          await expect(categoryPage.cartQuantityLabel).toHaveText(String(expectedTotal));
        });
      }
    }
  });

  test("a configurable product card links to its configuration page", async ({ page }) => {
    const categoryPage = new CategoryPage(page, LAPTOPS);

    const card = await test.step(`arrange: find ${CONFIGURABLE_SKU}`, async () => {
      await categoryPage.navigate();
      return categoryPage.scrollToProduct(CONFIGURABLE_SKU);
    });

    await test.step("assert: the card offers a customize link to the product", async () => {
      await expect(card.configurationsButton).toBeVisible();
      await expect(card.configurationsButton).toHaveAttribute("href", new RegExp(CONFIGURABLE_SLUG));
    });

    const productTab = await test.step("act: follow the customize link", () => card.openConfigurations());

    await test.step("assert: the product page opens with its configuration", async () => {
      const productPage = new ProductPage(productTab, CONFIGURABLE_SLUG);
      await expect(productTab).toHaveURL(new RegExp(CONFIGURABLE_SLUG));
      await expect(productPage.configuration.root).toBeVisible();
    });
  });
});
