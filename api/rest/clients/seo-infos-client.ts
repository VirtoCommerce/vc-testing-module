import type { HttpClient } from "../../http/http-client";
import type { SeoInfo } from "../types/core";

const SEO_INFOS_PATH = "/api/seoinfos";

export class SeoInfosClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async findDuplicates(objectType: string, objectId: string): Promise<SeoInfo[]> {
    const response = await this.#httpClient.get(`${SEO_INFOS_PATH}/duplicates`, { query: { objectType, objectId } });
    return response.expectOk().json<SeoInfo[]>();
  }
}
