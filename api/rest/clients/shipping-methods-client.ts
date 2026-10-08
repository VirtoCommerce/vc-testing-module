import type { HttpClient } from "../../http/http-client";
import type { ShippingMethodData, ShippingMethodsSearchCriteria, ShippingMethodsSearchResult } from "../types/shipping";

const SHIPPING_PATH = "/api/shipping";

export class ShippingMethodsClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async search(criteria: ShippingMethodsSearchCriteria): Promise<ShippingMethodData[]> {
    const response = await this.#httpClient.post(`${SHIPPING_PATH}/search`, { json: criteria });
    return response.expectOk().json<ShippingMethodsSearchResult>().results ?? [];
  }

  async update(shippingMethod: ShippingMethodData): Promise<void> {
    (await this.#httpClient.put(SHIPPING_PATH, { json: shippingMethod })).expectOk();
  }
}
