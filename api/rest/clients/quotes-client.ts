import type { HttpClient } from "../../http/http-client";

const QUOTE_REQUESTS_PATH = "/api/quote/requests";

export class QuotesClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async delete(ids: readonly string[]): Promise<void> {
    (await this.#httpClient.delete(QUOTE_REQUESTS_PATH, { query: { ids } })).expectOk();
  }
}
