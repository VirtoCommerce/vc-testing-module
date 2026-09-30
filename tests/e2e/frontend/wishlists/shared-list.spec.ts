import type { CleanupStack } from "@core/cleanup-stack";
import type { ArrangedShoppingList } from "@dataset/arrange/shopping-list";
import type { SignedInCustomerAccount } from "@fixtures";

import * as allure from "allure-js-commons";

import { ChangeShoppingListDocument } from "@api/graphql/generated/graphql";
import { requireFields } from "@core/required-fields";
import { cartScope } from "@dataset/arrange/cart";
import { addShoppingListItems, arrangeShoppingList } from "@dataset/arrange/shopping-list";
import { expect, test } from "@fixtures";
import { SharedListPage } from "@pages/frontend/pages/account-pages";

const PRODUCT_IDS = ["smartphone-apple-iphone-17-256gb-black", "smartphone-apple-iphone-17-256gb-mist-blue"];
const PUBLIC_SCOPE = "AnyoneAnonymous";
const PRIVATE_SCOPE = "Private";
const UNKNOWN_SHARING_KEY = "non-existent-sharing-key-000000";

test.beforeEach(async () => {
  await allure.feature("Wishlists / Shared list (E2E)");
});

test.describe("shared wishlist (anonymous visitor)", () => {
  test("a list shared with anyone is readable without signing in", async ({ page, customerAccount, cleanupStack }) => {
    const { list, sharingKey } = await test.step("arrange: a list with two products shared with anyone", () =>
      arrangeSharedList(customerAccount, cleanupStack, PRODUCT_IDS));
    const sharedPage = new SharedListPage(page, sharingKey);

    await test.step("act: open the share link", () => sharedPage.navigate());

    await test.step("assert: the list renders read-only with both products", async () => {
      await expect(sharedPage.listTitle).toHaveText(list.name);
      await expect(sharedPage.lineItems).toHaveCount(PRODUCT_IDS.length);
      await expect(sharedPage.addToCartControls).toHaveCount(0);
    });
  });

  test("a list made private again is not reachable by its old share link", async ({
    page,
    customerAccount,
    cleanupStack,
  }) => {
    const { list, sharingKey } = await test.step("arrange: a shared list with one product", () =>
      arrangeSharedList(customerAccount, cleanupStack, PRODUCT_IDS.slice(0, 1)));
    await test.step("arrange: make the list private again", () =>
      customerAccount.graphqlClient.execute(ChangeShoppingListDocument, {
        command: { listId: list.id, scope: PRIVATE_SCOPE },
      }));
    const sharedPage = new SharedListPage(page, sharingKey);

    await test.step("act: open the old share link", () => sharedPage.navigate());

    await test.step("assert: the not-found page is shown without the list", async () => {
      await expect(sharedPage.notFound).toBeVisible();
      await expect(sharedPage.listTitle).toHaveCount(0);
      await expect(sharedPage.lineItems).toHaveCount(0);
    });
  });

  test("an unknown share link shows the not-found page", async ({ page }) => {
    const sharedPage = new SharedListPage(page, UNKNOWN_SHARING_KEY);

    await test.step("act: open a share link with an unknown key", () => sharedPage.navigate());

    await test.step("assert: the not-found page is shown without list content", async () => {
      await expect(sharedPage.notFound).toBeVisible();
      await expect(sharedPage.lineItems).toHaveCount(0);
    });
  });
});

async function arrangeSharedList(
  account: SignedInCustomerAccount,
  cleanupStack: CleanupStack,
  productIds: readonly string[],
): Promise<{ readonly list: ArrangedShoppingList; readonly sharingKey: string }> {
  const created = await arrangeShoppingList(account.graphqlClient, cleanupStack, cartScope(account.context));
  const { changeWishlist } = await account.graphqlClient.execute(ChangeShoppingListDocument, {
    command: { listId: created.id, scope: PUBLIC_SCOPE },
  });
  const sharing = requireFields(changeWishlist?.sharingSetting ?? undefined, ["id"], `Sharing of ${created.name}`);
  const list = await addShoppingListItems(
    account.graphqlClient,
    created.id,
    productIds.map((productId) => ({ productId, quantity: 1 })),
  );
  return { list, sharingKey: sharing.id };
}
