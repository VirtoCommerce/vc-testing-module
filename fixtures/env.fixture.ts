import type { Env } from "@core/env";

import { test as base } from "@playwright/test";

import { getEnv } from "@core/env";

export interface EnvFixtures {
  readonly env: Env;
}

export const test = base.extend<Record<never, never>, EnvFixtures>({
  env: [
    async ({}, use) => {
      await use(getEnv());
    },
    { scope: "worker" },
  ],
});
