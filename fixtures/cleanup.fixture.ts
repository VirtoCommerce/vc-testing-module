import { CleanupStack } from "@core/cleanup-stack";

import { test as base } from "./api.fixture";

export interface CleanupFixtures {
  readonly cleanupStack: CleanupStack;
}

export const test = base.extend<CleanupFixtures>({
  cleanupStack: async ({ httpClient: _httpClientOutlivesCleanup }, use) => {
    const cleanupStack = new CleanupStack();
    await use(cleanupStack);
    await cleanupStack.unwind((description, action) => base.step(`cleanup: ${description}`, action));
  },
});
