import type { SignedInCustomerAccount } from "@fixtures";

import * as allure from "allure-js-commons";

import { GetShoppingListsDocument } from "@api/graphql/generated/graphql";
import { uniqueId } from "@core/unique-id";
import { cartScope } from "@dataset/arrange/cart";
import { registerShoppingListsRemoval } from "@dataset/arrange/shopping-list";
import { expect, test } from "@fixtures";
import { AccountListsPage } from "@pages/frontend/pages/account-pages";
import { isGraphqlMutation } from "@pages/graphql-traffic";

const SCOPES = [
  { scope: "Private", label: "Private" },
  { scope: "AnyoneAnonymous", label: "Anyone (readonly)" },
  { scope: "Organization", label: "Organization" },
] as const;

test.beforeEach(async () => {
  await allure.feature("Wishlists / Lists (E2E)");
});

test.describe("wishlist management (customer account)", () => {
  test.use({ shopperAccount: "customer-account" });

  for (const { scope, label } of SCOPES) {
    test(`create a wishlist shared with ${label}`, async ({ page, customerAccount, cleanupStack }) => {
      registerShoppingListsRemoval(customerAccount.graphqlClient, cleanupStack, cartScope(customerAccount.context));
      const listsPage = new AccountListsPage(page);
      const name = uniqueId("list");

      await test.step("arrange: open the create-list modal", async () => {
        await listsPage.navigate();
        await listsPage.createListButton.click();
        await expect(listsPage.settingsModal.root).toBeVisible();
      });

      await test.step(`act: create ${name} shared with ${label}`, async () => {
        await listsPage.settingsModal.nameInput.fill(name);
        await listsPage.settingsModal.descriptionInput.fill(`${scope} list created by an automated test`);
        await listsPage.settingsModal.selectScope(label);
        await Promise.all([
          page.waitForResponse(isGraphqlMutation("wishlist")),
          listsPage.settingsModal.saveButton.click(),
        ]);
      });

      await test.step(`assert: ${name} is listed with the ${scope} scope`, async () => {
        await expect(listsPage.card(name).root).toBeVisible();
        await expect.poll(() => listScopes(customerAccount)).toContainEqual({ name, scope });
      });
    });
  }

  test("rename, rescope and delete a wishlist", async ({ page, customerAccount, cleanupStack }) => {
    registerShoppingListsRemoval(customerAccount.graphqlClient, cleanupStack, cartScope(customerAccount.context));
    const listsPage = new AccountListsPage(page);
    const name = uniqueId("list");
    const renamed = `${name}-edited`;

    await test.step(`arrange: create the private list ${name}`, async () => {
      await listsPage.navigate();
      await listsPage.createListButton.click();
      await listsPage.settingsModal.nameInput.fill(name);
      await Promise.all([
        page.waitForResponse(isGraphqlMutation("wishlist")),
        listsPage.settingsModal.saveButton.click(),
      ]);
      await expect(listsPage.card(name).root).toBeVisible();
    });

    await test.step(`act: rename it to ${renamed} and share it with the organization`, async () => {
      const card = listsPage.card(name);
      await card.menuButton.click();
      await card.editMenuItem.click();
      await listsPage.settingsModal.nameInput.fill(renamed);
      await listsPage.settingsModal.descriptionInput.fill("Edited by an automated test");
      await listsPage.settingsModal.selectScope("Organization");
      await Promise.all([
        page.waitForResponse(isGraphqlMutation("wishlist")),
        listsPage.settingsModal.saveButton.click(),
      ]);
    });

    await test.step("assert: the list has the new name and scope", async () => {
      await expect(listsPage.card(renamed).root).toBeVisible();
      await expect.poll(() => listScopes(customerAccount)).toContainEqual({ name: renamed, scope: "Organization" });
    });

    await test.step("act: delete the list", async () => {
      const card = listsPage.card(renamed);
      await card.menuButton.click();
      await card.removeMenuItem.click();
      await Promise.all([
        page.waitForResponse(isGraphqlMutation("wishlist")),
        listsPage.deleteModal.confirmButton.click(),
      ]);
    });

    await test.step("assert: the list is gone", async () => {
      await expect(listsPage.card(renamed).root).toBeHidden();
      await expect
        .poll(async () => (await listScopes(customerAccount)).map((list) => list.name))
        .not.toContain(renamed);
    });
  });
});

async function listScopes(
  account: SignedInCustomerAccount,
): Promise<{ readonly name: string; readonly scope: string | null | undefined }[]> {
  const { wishlists } = await account.graphqlClient.execute(GetShoppingListsDocument, cartScope(account.context));
  return (wishlists?.items ?? []).flatMap((list) =>
    list === null ? [] : [{ name: list.name, scope: list.sharingSetting?.scope }],
  );
}
