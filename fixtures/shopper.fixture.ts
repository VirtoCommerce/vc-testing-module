import type { Credentials } from "@api/auth/credentials";
import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { FrontendContext } from "@dataset/frontend-context";

import { mergeTests } from "@playwright/test";

import { registerDefaultCartRemoval } from "@dataset/arrange/cart";

import { test as browserTest } from "./browser.fixture";
import { test as frontendContextTest } from "./frontend-context.fixture";

export interface Shopper {
  readonly credentials: Credentials | undefined;
  readonly graphqlClient: GraphqlClient;
  readonly context: FrontendContext;
}

export interface ShopperFixtures {
  readonly shopper: Shopper;
}

export const test = mergeTests(browserTest, frontendContextTest).extend<ShopperFixtures>({
  shopper: async ({ browserCustomerAccount, user, graphqlClient, frontendContext, cleanupStack }, use) => {
    const shopper =
      browserCustomerAccount === undefined
        ? { credentials: user, graphqlClient, context: frontendContext }
        : {
            credentials: browserCustomerAccount.credentials,
            graphqlClient: browserCustomerAccount.graphqlClient,
            context: browserCustomerAccount.context,
          };
    registerDefaultCartRemoval(shopper.graphqlClient, cleanupStack, shopper.context);
    await use(shopper);
  },
});
