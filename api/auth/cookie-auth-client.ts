import type { HttpClient } from "../http/http-client";
import type { LoginRequestData, SignInResultData } from "../rest/types/security";
import type { Credentials } from "./credentials";

const LOGIN_PATH = "/api/platform/security/login";

export class CookieAuthClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async signIn({ username, password }: Credentials): Promise<void> {
    const request: LoginRequestData = { userName: username, password };
    const response = await this.#httpClient.post(LOGIN_PATH, { json: request });
    const result = response.expectOk().json<SignInResultData>();
    if (!result.succeeded) {
      throw new Error(`Platform sign-in as ${username} failed: ${JSON.stringify(result)}`);
    }
  }
}
