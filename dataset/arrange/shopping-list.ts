import type { ShoppingListFragment } from "@api/graphql/generated/graphql";
import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { CleanupStack } from "@core/cleanup-stack";
import type { CartItem, CartScope } from "./cart";

import {
  AddItemsToShoppingListDocument,
  CreateShoppingListDocument,
  DeleteShoppingListDocument,
  GetShoppingListsDocument,
} from "@api/graphql/generated/graphql";
import { requireFields } from "@core/required-fields";
import { uniqueId } from "@core/unique-id";

export type ArrangedShoppingList = ShoppingListFragment & { readonly id: string };

export async function arrangeShoppingList(
  graphqlClient: GraphqlClient,
  cleanupStack: CleanupStack,
  scope: CartScope,
  listName = uniqueId("test-shopping-list"),
): Promise<ArrangedShoppingList> {
  const { createWishlist } = await graphqlClient.execute(CreateShoppingListDocument, {
    command: { ...scope, listName, description: `Created by an automated test: ${listName}` },
  });
  const list = requireShoppingList(createWishlist, `Shopping list ${listName}`);
  cleanupStack.push(`delete shopping list ${listName}`, () =>
    graphqlClient.execute(DeleteShoppingListDocument, { command: { listId: list.id } }),
  );
  return list;
}

export async function addShoppingListItems(
  graphqlClient: GraphqlClient,
  listId: string,
  items: readonly CartItem[],
): Promise<ArrangedShoppingList> {
  const { addWishlistItems } = await graphqlClient.execute(AddItemsToShoppingListDocument, {
    command: { listId, listItems: [...items] },
  });
  return requireShoppingList(addWishlistItems, `Shopping list ${listId}`);
}

export function registerShoppingListsRemoval(
  graphqlClient: GraphqlClient,
  cleanupStack: CleanupStack,
  scope: CartScope,
): void {
  cleanupStack.push(`delete every shopping list of ${scope.userId}`, async () => {
    const { wishlists } = await graphqlClient.execute(GetShoppingListsDocument, scope);
    for (const list of wishlists?.items ?? []) {
      if (list !== null) {
        await graphqlClient.execute(DeleteShoppingListDocument, { command: { listId: list.id } });
      }
    }
  });
}

export function requireShoppingList(
  list: ShoppingListFragment | null | undefined,
  label: string,
): ArrangedShoppingList {
  return requireFields(list ?? undefined, ["id"], label);
}
