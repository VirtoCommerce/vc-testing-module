import type { HttpClient, HttpHeaders } from "../http/http-client";
import type { HttpResponse } from "../http/http-response";
import type { Credentials } from "./credentials";

import { setTimeout as sleep } from "node:timers/promises";

import { number, object, string } from "zod";

const TOKEN_PATH = "/connect/token";
const REVOKE_PATH = "/revoke/token";
const OFFLINE_ACCESS_SCOPE = "offline_access";
const MAX_ATTEMPTS = 3;
const RETRY_BASE_DELAY_MS = 200;

const TokenResponseSchema = object({
  access_token: string().min(1),
  token_type: string().min(1),
  expires_in: number().int().positive(),
  refresh_token: string().min(1).optional(),
});

export interface AuthToken {
  readonly accessToken: string;
  readonly tokenType: string;
  readonly expiresAt: number;
  readonly refreshToken: string | undefined;
}

export class TokenAuthClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  requestToken(credentials: Credentials, storeId: string): Promise<AuthToken> {
    return this.#tokenRequest({
      grant_type: "password",
      username: credentials.username,
      password: credentials.password,
      storeId,
      scope: OFFLINE_ACCESS_SCOPE,
    });
  }

  refreshToken(refreshToken: string): Promise<AuthToken> {
    return this.#tokenRequest({ grant_type: "refresh_token", refresh_token: refreshToken });
  }

  async revokeToken(token: AuthToken): Promise<void> {
    const response = await this.#httpClient.withHeaders(authHeader(token)).post(REVOKE_PATH);
    response.expectOk();
  }

  async #tokenRequest(form: Readonly<Record<string, string>>): Promise<AuthToken> {
    const requestedAt = Date.now();
    const response = await this.#postWithRetry(form);
    const body = response.expectOk().parse(TokenResponseSchema);
    return {
      accessToken: body.access_token,
      tokenType: body.token_type,
      expiresAt: requestedAt + body.expires_in * 1000,
      refreshToken: body.refresh_token,
    };
  }

  async #postWithRetry(form: Readonly<Record<string, string>>): Promise<HttpResponse> {
    for (let attempt = 1; ; attempt++) {
      const response = await this.#httpClient.post(TOKEN_PATH, { form });
      if (response.status < 500 || attempt === MAX_ATTEMPTS) {
        return response;
      }
      await sleep(RETRY_BASE_DELAY_MS * attempt + Math.random() * RETRY_BASE_DELAY_MS);
    }
  }
}

export function authHeader(token: AuthToken): HttpHeaders {
  return { Authorization: `${token.tokenType} ${token.accessToken}` };
}
