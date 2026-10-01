import type { Page } from "@playwright/test";
import type { SignedInCustomerAccount } from "@fixtures";

import * as allure from "allure-js-commons";

import { GetShoppingListDocument } from "@api/graphql/generated/graphql";
import { cartScope } from "@dataset/arrange/cart";
import { addShoppingListItems, arrangeShoppingList } from "@dataset/arrange/shopping-list";
import { expect, test } from "@fixtures";
import { AddToWishlistsModal } from "@pages/frontend/components/wishlist";
import { AccountListDetailsPage } from "@pages/frontend/pages/account-pages";
import { CartPage } from "@pages/frontend/pages/cart-page";
import { CategoryPage } from "@pages/frontend/pages/category-page";
import { ProductPage } from "@pages/frontend/pages/product-page";
import { isGraphqlMutation } from "@pages/graphql-traffic";

const SMARTPHONES = "smartphones";
const PRODUCT_SKU = "smartphone-samsung-galaxy-a57-5g";
const VARIATIONS_PARENT_SKU = "smartphone-google-pixel-10-frost";
const VARIATION_SKU = "smartphone-google-pixel-10-indigo";

interface AddToListSource {
  readonly title: string;
  readonly sku: string;
  open(page: Page): Promise<void>;
}

const FROM_CATEGORY_GRID: AddToListSource = {
  title: "the category grid",
  sku: PRODUCT_SKU,
  async open(page) {
    const categoryPage = new CategoryPage(page, SMARTPHONES);
    await categoryPage.navigate();
    await (await categoryPage.scrollToProduct(PRODUCT_SKU)).addToListButton.click();
  },
};

const ADD_TO_LIST_SOURCES: readonly AddToListSource[] = [
  FROM_CATEGORY_GRID,
  {
    title: "the category list",
    sku: VARIATIONS_PARENT_SKU,
    async open(page) {
      const categoryPage = new CategoryPage(page, SMARTPHONES);
      await categoryPage.navigate();
      await categoryPage.viewSwitcher.listViewTab.click();
      await (await categoryPage.scrollToProduct(VARIATIONS_PARENT_SKU)).addToListButton.click();
    },
  },
  {
    title: "the product page",
    sku: VARIATION_SKU,
    async open(page) {
      const productPage = new ProductPage(page, `product/${VARIATION_SKU}`);
      await productPage.navigate();
      await productPage.addToListButton.click();
    },
  },
];

test.beforeEach(async () => {
  await allure.feature("Wishlists / Items (E2E)");
});

test.describe("wishlist items (customer account)", () => {
  test.use({ shopperAccount: "customer-account" });

  for (const source of ADD_TO_LIST_SOURCES) {
    test(`add a product to a wishlist from ${source.title}`, async ({ page, customerAccount, cleanupStack }) => {
      const list = await test.step("arrange: an empty wishlist", () =>
        arrangeShoppingList(customerAccount.graphqlClient, cleanupStack, cartScope(customerAccount.context)));
      const modal = new AddToWishlistsModal(page);

      await test.step(`arrange: open the add-to-list modal from ${source.title}`, async () => {
        await source.open(page);
        await expect(modal.root).toBeVisible();
      });

      await test.step(`act: tick ${list.name} and save`, async () => {
        await modal.listCheckbox(list.id).click();
        await Promise.all([page.waitForResponse(isGraphqlMutation("wishlist")), modal.saveButton.click()]);
      });

      await test.step(`assert: the wishlist holds ${source.sku}`, async () => {
        await expect(modal.root).toBeHidden();
        await expect.poll(() => listSkus(customerAccount, list.id)).toContain(source.sku);
      });
    });
  }

  test("remove a product from a wishlist via the add-to-list modal", async ({
    page,
    customerAccount,
    cleanupStack,
  }) => {
    const list = await test.step(`arrange: a wishlist with ${PRODUCT_SKU}`, async () => {
      const created = await arrangeShoppingList(
        customerAccount.graphqlClient,
        cleanupStack,
        cartScope(customerAccount.context),
      );
      return addShoppingListItems(customerAccount.graphqlClient, created.id, [{ productId: PRODUCT_SKU, quantity: 1 }]);
    });
    const modal = new AddToWishlistsModal(page);

    await test.step("arrange: open the add-to-list modal from the category grid", async () => {
      await FROM_CATEGORY_GRID.open(page);
      await expect(modal.root).toBeVisible();
    });

    await test.step(`act: untick ${list.name} and save`, async () => {
      await modal.listWithProductCheckbox(list.id).click();
      await Promise.all([page.waitForResponse(isGraphqlMutation("wishlist")), modal.saveButton.click()]);
    });

    await test.step(`assert: the wishlist no longer holds ${PRODUCT_SKU}`, async () => {
      await expect(modal.root).toBeHidden();
      await expect.poll(() => listSkus(customerAccount, list.id)).not.toContain(PRODUCT_SKU);
    });
  });

  test("add every wishlist product to the cart", async ({ page, customerAccount, cleanupStack }) => {
    const skus = [PRODUCT_SKU, VARIATION_SKU];
    const list = await test.step("arrange: a wishlist with two products", async () => {
      const created = await arrangeShoppingList(
        customerAccount.graphqlClient,
        cleanupStack,
        cartScope(customerAccount.context),
      );
      return addShoppingListItems(
        customerAccount.graphqlClient,
        created.id,
        skus.map((productId) => ({ productId, quantity: 1 })),
      );
    });
    const detailsPage = new AccountListDetailsPage(page, list.id);

    await test.step("arrange: open the wishlist details", async () => {
      await detailsPage.navigate();
      await expect(detailsPage.lineItems).toHaveCount(skus.length);
    });

    await test.step("act: add all products to the cart", () =>
      Promise.all([page.waitForResponse(isGraphqlMutation("cart")), detailsPage.addAllToCartButton.click()]));

    await test.step("assert: the cart holds both products", async () => {
      await expect(detailsPage.cartQuantityLabel).toHaveText(String(skus.length));
      const cartPage = new CartPage(page);
      await cartPage.navigate();
      await expect(cartPage.lineItems).toHaveCount(skus.length);
      for (const sku of skus) {
        await expect(cartPage.lineItem(sku).root).toBeVisible();
      }
    });
  });
});

async function listSkus(account: SignedInCustomerAccount, listId: string): Promise<(string | null)[]> {
  const { wishlist } = await account.graphqlClient.execute(GetShoppingListDocument, {
    listId,
    cultureName: account.context.cultureName,
  });
  return wishlist?.items?.map((item) => item?.sku ?? null) ?? [];
}
