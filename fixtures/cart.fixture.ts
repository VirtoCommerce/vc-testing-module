import type { TestFixture } from "@playwright/test";
import type { ArrangedCart, CartItem } from "@dataset/arrange/cart";
import type { CleanupFixtures } from "./cleanup.fixture";
import type { ShopperFixtures } from "./shopper.fixture";

import { expect } from "@playwright/test";

import { arrangeDefaultCart, findDefaultCart } from "@dataset/arrange/cart";

import { test as base } from "./shopper.fixture";

export interface CartFixtures {
  readonly cart: ArrangedCart | undefined;
}

type CartFixtureArgs = ShopperFixtures & CleanupFixtures;

export const test = base.extend<CartFixtures>({
  cart: [
    async ({}, use) => {
      await use(undefined);
    },
    { auto: true },
  ],
});

export function withItems(items: readonly CartItem[]): TestFixture<ArrangedCart | undefined, CartFixtureArgs> {
  return async ({ shopper, cleanupStack }, use) => {
    const cart = await arrangeDefaultCart(shopper.graphqlClient, cleanupStack, shopper.context, items);
    await expect
      .poll(async () => (await findDefaultCart(shopper.graphqlClient, shopper.context))?.itemsCount, {
        message: `the default cart of ${shopper.context.userName ?? "the anonymous shopper"} is readable`,
      })
      .toBe(cart.itemsCount);
    await use(cart);
  };
}
