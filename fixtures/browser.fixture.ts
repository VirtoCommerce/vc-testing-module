import type { App } from "@api/auth/browser-sessions";

import { BrowserSessions } from "@api/auth/browser-sessions";
import { TokenAuthClient } from "@api/auth/token-auth-client";
import { TokenManager } from "@api/auth/token-manager";
import { HttpClient } from "@api/http/http-client";

import { openBackendContext, openFrontendContext, withSignInHint } from "./api.fixture";
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
    async ({ playwright, env }, use) => {
      const frontendRequestContext = await openFrontendContext(playwright, env);
      const frontendTokenManager = new TokenManager(new TokenAuthClient(new HttpClient(frontendRequestContext)));
      try {
        await use(
          new BrowserSessions(frontendTokenManager, {
            storeId: env.storeId,
            frontendBaseUrl: env.frontendBaseUrl,
            newBackendContext() {
              return openBackendContext(playwright, env);
            },
          }),
        );
        await frontendTokenManager.signOutAll();
      } finally {
        await frontendRequestContext.dispose();
      }
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
