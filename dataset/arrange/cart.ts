import type { CartFragment, InputNewCartItemType } from "@api/graphql/generated/graphql";
import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { CleanupStack } from "@core/cleanup-stack";
import type { FrontendContext } from "../frontend-context";

import { AddItemsCartDocument, GetCartDocument, RemoveCartDocument } from "@api/graphql/generated/graphql";
import { requireFields } from "@core/required-fields";
import { uniqueId } from "@core/unique-id";

export interface CartScope {
  readonly storeId: string;
  readonly userId: string;
  readonly currencyCode: string;
  readonly cultureName: string;
}

export interface CartItem {
  readonly productId: string;
  readonly quantity: number;
}

export type ArrangedCart = CartFragment & { readonly id: string };

export function cartScope(context: FrontendContext): CartScope {
  return {
    storeId: context.storeId,
    userId: context.userId,
    currencyCode: context.currencyCode,
    cultureName: context.cultureName,
  };
}

export async function arrangeCart(
  graphqlClient: GraphqlClient,
  cleanupStack: CleanupStack,
  context: FrontendContext,
  items: readonly CartItem[],
  extraItemFields: Partial<InputNewCartItemType> = {},
): Promise<ArrangedCart> {
  const { addItemsCart } = await graphqlClient.execute(AddItemsCartDocument, {
    command: {
      ...cartScope(context),
      cartName: uniqueId("test-cart"),
      cartItems: items.map((item) => ({ ...extraItemFields, ...item })),
    },
  });
  const cart = requireFields(addItemsCart ?? undefined, ["id"], "Arranged cart");
  registerCartRemoval(graphqlClient, cleanupStack, context, cart.id);
  return cart;
}

export async function arrangeDefaultCart(
  graphqlClient: GraphqlClient,
  cleanupStack: CleanupStack,
  context: FrontendContext,
  items: readonly CartItem[],
): Promise<ArrangedCart> {
  const { addItemsCart } = await graphqlClient.execute(AddItemsCartDocument, {
    command: { ...cartScope(context), cartItems: [...items] },
  });
  const cart = requireFields(addItemsCart ?? undefined, ["id"], "Arranged default cart");
  registerCartRemoval(graphqlClient, cleanupStack, context, cart.id);
  return cart;
}

export async function findDefaultCart(
  graphqlClient: GraphqlClient,
  context: FrontendContext,
): Promise<ArrangedCart | undefined> {
  const { cart } = await graphqlClient.execute(GetCartDocument, cartScope(context));
  return cart === null ? undefined : requireCart(cart, "Default cart");
}

export function registerDefaultCartRemoval(
  graphqlClient: GraphqlClient,
  cleanupStack: CleanupStack,
  context: FrontendContext,
): void {
  cleanupStack.push(`remove the default cart of ${context.userName ?? context.userId}`, async () => {
    const cart = await findDefaultCart(graphqlClient, context);
    if (cart !== undefined) {
      await graphqlClient.execute(RemoveCartDocument, { command: { cartId: cart.id, userId: context.userId } });
    }
  });
}

export function registerCartRemoval(
  graphqlClient: GraphqlClient,
  cleanupStack: CleanupStack,
  context: FrontendContext,
  cartId: string,
): void {
  cleanupStack.push(`remove cart ${cartId}`, () =>
    graphqlClient.execute(RemoveCartDocument, { command: { cartId, userId: context.userId } }),
  );
}

interface LineItemIdentity {
  readonly id?: string | null;
  readonly productId?: string | null;
}

export type IdentifiedLineItem<Item extends LineItemIdentity> = Item & {
  readonly id: string;
  readonly productId: string;
};

export function lineItemFor<Item extends LineItemIdentity>(
  cart: { readonly items?: readonly (Item | null)[] | null | undefined } | null | undefined,
  productId: string,
): IdentifiedLineItem<Item> {
  const lineItem = cart?.items?.find((item) => item?.productId === productId) ?? undefined;
  return requireFields(lineItem, ["id", "productId"], `Line item of product "${productId}"`);
}

export function requireCart(cart: CartFragment | null | undefined, label: string): ArrangedCart {
  return requireFields(cart ?? undefined, ["id"], label);
}
