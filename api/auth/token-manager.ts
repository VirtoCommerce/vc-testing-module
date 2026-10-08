import type { HttpClient } from "../http/http-client";
import type { Credentials } from "./credentials";
import type { AuthToken, TokenAuthClient } from "./token-auth-client";

import { HttpError } from "../http/http-error";
import { authHeader } from "./token-auth-client";

const EXPIRY_MARGIN_MS = 60_000;

interface ManagedSession {
  readonly storeId: string;
  readonly credentials: Credentials;
  readonly token: AuthToken;
}

export class TokenManager {
  readonly #tokenAuthClient: TokenAuthClient;
  readonly #sessions = new Map<string, ManagedSession>();

  constructor(tokenAuthClient: TokenAuthClient) {
    this.#tokenAuthClient = tokenAuthClient;
  }

  async authorize(httpClient: HttpClient, credentials: Credentials, storeId: string): Promise<HttpClient> {
    await this.getToken(credentials, storeId);
    return httpClient.withHeaders(async () => authHeader(await this.getToken(credentials, storeId)));
  }

  async getToken(credentials: Credentials, storeId: string): Promise<AuthToken> {
    const session = this.#sessions.get(sessionKey(storeId, credentials.username));
    if (session === undefined || session.credentials.password !== credentials.password) {
      return this.#signIn(credentials, storeId);
    }
    return this.#refresh(session);
  }

  async signOut(username: string, storeId: string): Promise<void> {
    const key = sessionKey(storeId, username);
    const session = this.#sessions.get(key);
    if (session === undefined) {
      return;
    }
    this.#sessions.delete(key);
    const token = await this.#revocableToken(session);
    if (token !== undefined) {
      await this.#tokenAuthClient.revokeToken(token);
    }
  }

  async signOutAll(): Promise<void> {
    await Promise.all(
      [...this.#sessions.values()].map((session) => this.signOut(session.credentials.username, session.storeId)),
    );
  }

  async #refresh(session: ManagedSession): Promise<AuthToken> {
    if (session.token.expiresAt - EXPIRY_MARGIN_MS > Date.now()) {
      return session.token;
    }
    if (session.token.refreshToken !== undefined) {
      const refreshed = await this.#tokenAuthClient.refreshToken(session.token.refreshToken).catch(rejectedRefresh);
      if (refreshed !== undefined) {
        this.#sessions.set(sessionKey(session.storeId, session.credentials.username), { ...session, token: refreshed });
        return refreshed;
      }
    }
    return this.#signIn(session.credentials, session.storeId);
  }

  async #revocableToken(session: ManagedSession): Promise<AuthToken | undefined> {
    if (session.token.expiresAt - EXPIRY_MARGIN_MS > Date.now()) {
      return session.token;
    }
    if (session.token.refreshToken === undefined) {
      return undefined;
    }
    return this.#tokenAuthClient.refreshToken(session.token.refreshToken).catch(rejectedRefresh);
  }

  async #signIn(credentials: Credentials, storeId: string): Promise<AuthToken> {
    const token = await this.#tokenAuthClient.requestToken(credentials, storeId);
    this.#sessions.set(sessionKey(storeId, credentials.username), { storeId, credentials, token });
    return token;
  }
}

function sessionKey(storeId: string, username: string): string {
  return JSON.stringify([storeId, username]);
}

function rejectedRefresh(error: unknown): undefined {
  if (error instanceof HttpError && error.status >= 400 && error.status < 500) {
    return undefined;
  }
  throw error;
}
