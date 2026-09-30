import type { APIRequestContext, PlaywrightWorkerArgs } from "@playwright/test";
import type { Credentials } from "@api/auth/credentials";
import type { Env } from "@core/env";

import { TokenAuthClient } from "@api/auth/token-auth-client";
import { TokenManager } from "@api/auth/token-manager";
import { GraphqlClient } from "@api/graphql/graphql-client";
import { HttpClient } from "@api/http/http-client";
import { HttpError } from "@api/http/http-error";

import { test as base } from "./env.fixture";

export interface ApiOptions {
  readonly user: Credentials | undefined;
}

export interface ApiWorkerFixtures {
  readonly tokenManager: TokenManager;
}

export interface ApiFixtures {
  readonly anonymousUserId: string;
  readonly httpClient: HttpClient;
  readonly anonymousHttpClient: HttpClient;
  readonly platformAdminHttpClient: HttpClient;
  readonly graphqlClient: GraphqlClient;
}

export const test = base.extend<ApiOptions & ApiFixtures, ApiWorkerFixtures>({
  user: [undefined, { option: true }],

  anonymousUserId: async ({}, use) => {
    await use(crypto.randomUUID());
  },

  tokenManager: [
    async ({ playwright, env }, use) => {
      const context = await openBackendContext(playwright, env);
      const tokenManager = new TokenManager(new TokenAuthClient(new HttpClient(context)));
      try {
        await use(tokenManager);
        await tokenManager.signOutAll();
      } finally {
        await context.dispose();
      }
    },
    { scope: "worker" },
  ],

  httpClient: async ({ user, playwright, env, tokenManager }, use) => {
    const context = await openBackendContext(playwright, env);
    try {
      const anonymous = new HttpClient(context);
      await use(
        user === undefined
          ? anonymous
          : await withSignInHint(user, () => tokenManager.authorize(anonymous, user, env.storeId)),
      );
    } finally {
      await context.dispose();
    }
  },

  anonymousHttpClient: async ({ playwright, env }, use) => {
    const context = await openBackendContext(playwright, env);
    try {
      await use(new HttpClient(context));
    } finally {
      await context.dispose();
    }
  },

  platformAdminHttpClient: async ({ anonymousHttpClient, env, tokenManager }, use) => {
    await use(
      await withSignInHint(env.admin, () => tokenManager.authorize(anonymousHttpClient, env.admin, env.storeId)),
    );
  },

  graphqlClient: async ({ httpClient }, use) => {
    await use(new GraphqlClient(httpClient));
  },
});

export function openBackendContext(
  playwright: PlaywrightWorkerArgs["playwright"],
  env: Env,
): Promise<APIRequestContext> {
  return playwright.request.newContext({
    baseURL: env.backendBaseUrl,
    timeout: env.requestTimeoutMs,
    ignoreHTTPSErrors: !env.verifySsl,
  });
}

export function openFrontendContext(
  playwright: PlaywrightWorkerArgs["playwright"],
  env: Env,
): Promise<APIRequestContext> {
  return playwright.request.newContext({
    baseURL: env.frontendBaseUrl,
    timeout: env.requestTimeoutMs,
    ignoreHTTPSErrors: !env.verifySsl,
  });
}

export async function withSignInHint<T>(user: Credentials, signIn: () => Promise<T>): Promise<T> {
  try {
    return await signIn();
  } catch (error) {
    if (error instanceof HttpError && error.status >= 400 && error.status < 500) {
      const hint = "check the credentials, or seed the dataset with `npm run seed`";
      throw new Error(`Cannot sign in as ${user.username}: ${hint}`, { cause: error });
    }
    throw error;
  }
}
