import type { APIRequestContext } from "@playwright/test";
import type { Credentials } from "./credentials";
import type { AuthToken } from "./token-auth-client";
import type { TokenManager } from "./token-manager";

import { HttpClient } from "../http/http-client";
import { CookieAuthClient } from "./cookie-auth-client";

export type App = "frontend" | "backend";

export type StorageState = Awaited<ReturnType<APIRequestContext["storageState"]>>;

const EMPTY_STORAGE_STATE: StorageState = { cookies: [], origins: [] };

const STOREFRONT_AUTH_KEY = "auth";
const STOREFRONT_USER_ID_KEY = "user-id";

export interface BrowserSessionsOptions {
  readonly storeId: string;
  readonly frontendBaseUrl: string;
  readonly newBackendContext: () => Promise<APIRequestContext>;
}

export class BrowserSessions {
  readonly #tokenManager: TokenManager;
  readonly #options: BrowserSessionsOptions;
  readonly #backendSessions = new Map<string, StorageState>();

  constructor(tokenManager: TokenManager, options: BrowserSessionsOptions) {
    this.#tokenManager = tokenManager;
    this.#options = options;
  }

  get(app: App, user: Credentials): Promise<StorageState> {
    return app === "frontend" ? this.#frontendSession(user) : this.#backendSession(user);
  }

  anonymous(app: App, anonymousUserId: string): StorageState {
    if (app === "backend") {
      return EMPTY_STORAGE_STATE;
    }
    return storefrontState(this.#options.frontendBaseUrl, [{ name: STOREFRONT_USER_ID_KEY, value: anonymousUserId }]);
  }

  async #frontendSession(user: Credentials): Promise<StorageState> {
    const token = await this.#tokenManager.getToken(user, this.#options.storeId);
    return storefrontState(this.#options.frontendBaseUrl, [
      { name: STOREFRONT_AUTH_KEY, value: storefrontAuthValue(token) },
    ]);
  }

  async #backendSession(user: Credentials): Promise<StorageState> {
    const cached = this.#backendSessions.get(user.username);
    if (cached !== undefined) {
      return cached;
    }
    const context = await this.#options.newBackendContext();
    try {
      await new CookieAuthClient(new HttpClient(context)).signIn(user);
      const session = await context.storageState();
      this.#backendSessions.set(user.username, session);
      return session;
    } finally {
      await context.dispose();
    }
  }
}

function storefrontState(
  frontendBaseUrl: string,
  localStorage: StorageState["origins"][number]["localStorage"],
): StorageState {
  return { cookies: [], origins: [{ origin: new URL(frontendBaseUrl).origin, localStorage }] };
}

function storefrontAuthValue(token: AuthToken): string {
  return JSON.stringify({
    expires_at: new Date(token.expiresAt).toISOString(),
    token_type: token.tokenType,
    access_token: token.accessToken,
    refresh_token: token.refreshToken,
  });
}
