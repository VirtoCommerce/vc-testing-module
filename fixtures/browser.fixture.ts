import type { App } from "@api/auth/browser-sessions";

import { BrowserSessions } from "@api/auth/browser-sessions";

import { openBackendContext, withSignInHint } from "./api.fixture";
import { test as base } from "./customer-account.fixture";

export interface BrowserOptions {
  readonly app: App | undefined;
}

export interface BrowserWorkerFixtures {
  readonly browserSessions: BrowserSessions;
}

export const test = base.extend<BrowserOptions, BrowserWorkerFixtures>({
  app: [undefined, { option: true }],

  browserSessions: [
    async ({ playwright, env, tokenManager }, use) => {
      await use(
        new BrowserSessions(tokenManager, {
          storeId: env.storeId,
          frontendBaseUrl: env.frontendBaseUrl,
          newBackendContext() {
            return openBackendContext(playwright, env);
          },
        }),
      );
    },
    { scope: "worker" },
  ],

  storageState: async ({ app, user, browserCustomerAccount, anonymousUserId, browserSessions }, use) => {
    if (app === undefined) {
      await use(undefined);
      return;
    }
    const credentials = browserCustomerAccount?.credentials ?? user;
    await use(
      credentials === undefined
        ? browserSessions.anonymous(app, anonymousUserId)
        : await withSignInHint(credentials, () => browserSessions.get(app, credentials)),
    );
  },
});
