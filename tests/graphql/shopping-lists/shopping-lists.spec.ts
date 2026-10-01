import * as allure from "allure-js-commons";

import {
  ChangeShoppingListDocument,
  GetShoppingListDocument,
  GetShoppingListsDocument,
  RemoveItemsFromShoppingListDocument,
  UpdateShoppingListItemsDocument,
} from "@api/graphql/generated/graphql";
import { uniqueId } from "@core/unique-id";
import { cartScope, lineItemFor } from "@dataset/arrange/cart";
import { addShoppingListItems, arrangeShoppingList } from "@dataset/arrange/shopping-list";
import { expect, test } from "@fixtures";

const PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black";
const ORGANIZATION_SCOPE = "Organization";

test.beforeEach(async () => {
  await allure.feature("Shopping Lists");
});

test.describe("shopping lists (customer account)", () => {
  test("create and read a shopping list", async ({ customerAccount, cleanupStack }) => {
    const listName = uniqueId("test-shopping-list");

    const list = await test.step(`act: create shopping list ${listName}`, () =>
      arrangeShoppingList(customerAccount.graphqlClient, cleanupStack, cartScope(customerAccount.context), listName));

    await test.step("assert: the list is empty and readable", async () => {
      expect(list).toMatchObject({ name: listName, storeId: customerAccount.context.storeId, items: [] });
      const { wishlist } = await customerAccount.graphqlClient.execute(GetShoppingListDocument, {
        listId: list.id,
        cultureName: customerAccount.context.cultureName,
      });
      expect(wishlist).toMatchObject({ id: list.id, name: listName });
    });
  });

  test("list the shopping lists of the user", async ({ customerAccount, cleanupStack }) => {
    const scope = cartScope(customerAccount.context);
    const created = await test.step("arrange: two shopping lists", async () => [
      await arrangeShoppingList(customerAccount.graphqlClient, cleanupStack, scope),
      await arrangeShoppingList(customerAccount.graphqlClient, cleanupStack, scope),
    ]);

    const { wishlists } = await test.step("act: list the shopping lists", () =>
      customerAccount.graphqlClient.execute(GetShoppingListsDocument, scope));

    await test.step("assert: both lists are listed", async () => {
      expect(wishlists?.items?.map((list) => list?.id)).toEqual(expect.arrayContaining(created.map((list) => list.id)));
    });
  });

  test("rename, describe and share a shopping list", async ({ customerAccount, cleanupStack }) => {
    const list = await test.step("arrange: shopping list", () =>
      arrangeShoppingList(customerAccount.graphqlClient, cleanupStack, cartScope(customerAccount.context)));
    const changes = { listName: `${list.name}-renamed`, description: "Updated description", scope: ORGANIZATION_SCOPE };

    const { changeWishlist } = await test.step("act: change name, description and scope", () =>
      customerAccount.graphqlClient.execute(ChangeShoppingListDocument, { command: { listId: list.id, ...changes } }));

    await test.step("assert: the list has the new name, description and organization scope", async () => {
      expect(changeWishlist).toMatchObject({
        name: changes.listName,
        description: changes.description,
        sharingSetting: { scope: ORGANIZATION_SCOPE },
      });
    });
  });

  test("add an item to a shopping list", async ({ customerAccount, cleanupStack }) => {
    const list = await test.step("arrange: shopping list", () =>
      arrangeShoppingList(customerAccount.graphqlClient, cleanupStack, cartScope(customerAccount.context)));

    const withItem = await test.step("act: add a product ×3", () =>
      addShoppingListItems(customerAccount.graphqlClient, list.id, [{ productId: PRODUCT_ID, quantity: 3 }]));

    await test.step("assert: the list has the product ×3", async () => {
      expect(lineItemFor(withItem, PRODUCT_ID).quantity).toBe(3);
    });
  });

  test("change the quantity of a shopping list item", async ({ customerAccount, cleanupStack }) => {
    const list = await test.step("arrange: shopping list with a product ×1", async () => {
      const created = await arrangeShoppingList(
        customerAccount.graphqlClient,
        cleanupStack,
        cartScope(customerAccount.context),
      );
      return addShoppingListItems(customerAccount.graphqlClient, created.id, [{ productId: PRODUCT_ID, quantity: 1 }]);
    });
    const item = lineItemFor(list, PRODUCT_ID);

    const { updateWishListItems } = await test.step("act: change the quantity to 3", () =>
      customerAccount.graphqlClient.execute(UpdateShoppingListItemsDocument, {
        command: { listId: list.id, items: [{ lineItemId: item.id, quantity: 3 }] },
      }));

    await test.step("assert: the same item has quantity 3", async () => {
      expect(lineItemFor(updateWishListItems, PRODUCT_ID)).toMatchObject({ id: item.id, quantity: 3 });
    });
  });

  test("remove an item from a shopping list", async ({ customerAccount, cleanupStack }) => {
    const list = await test.step("arrange: shopping list with a product", async () => {
      const created = await arrangeShoppingList(
        customerAccount.graphqlClient,
        cleanupStack,
        cartScope(customerAccount.context),
      );
      return addShoppingListItems(customerAccount.graphqlClient, created.id, [{ productId: PRODUCT_ID, quantity: 1 }]);
    });

    const { removeWishlistItems } = await test.step("act: remove the item", () =>
      customerAccount.graphqlClient.execute(RemoveItemsFromShoppingListDocument, {
        command: { listId: list.id, lineItemIds: [lineItemFor(list, PRODUCT_ID).id] },
      }));

    await test.step("assert: the list is empty", async () => {
      expect(removeWishlistItems).toMatchObject({ itemsCount: 0, items: [] });
    });
  });
});
