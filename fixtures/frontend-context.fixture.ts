import type { FrontendContext } from "@dataset/frontend-context";

import { mergeTests } from "@playwright/test";

import { getFrontendContext } from "@dataset/frontend-context";

import { test as apiTest } from "./api.fixture";
import { test as datasetTest } from "./dataset.fixture";

export interface FrontendContextFixtures {
  readonly frontendContext: FrontendContext;
}

export const test = mergeTests(apiTest, datasetTest).extend<FrontendContextFixtures>({
  frontendContext: async ({ dataset, env, user, anonymousUserId }, use) => {
    await use(getFrontendContext(dataset, env.storeId, user?.username, anonymousUserId));
  },
});
