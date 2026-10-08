import type { HttpClient } from "../../http/http-client";
import type { Store, StoreData, StoreSearchCriteria, StoreSearchResult } from "../types/store";

import { requireFields } from "@core/required-fields";

import { STORE_FIELDS } from "../types/store";

export const STORES_PATH = "/api/stores";

export class StoresClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async get(id: string): Promise<Store> {
    return requireFields(await this.#fetch(id), STORE_FIELDS, `Store "${id}"`);
  }

  async find(id: string): Promise<Store | undefined> {
    const store = await this.#fetch(id);
    return store === undefined ? undefined : requireFields(store, STORE_FIELDS, `Store "${id}"`);
  }

  async create(store: StoreData): Promise<Store> {
    const response = await this.#httpClient.post(STORES_PATH, { json: store });
    return requireFields(response.expectOk().json<StoreData>(), STORE_FIELDS, "Created store");
  }

  async update(store: StoreData): Promise<void> {
    (await this.#httpClient.put(STORES_PATH, { json: store })).expectOk();
  }

  async search(criteria: StoreSearchCriteria): Promise<Store[]> {
    const response = await this.#httpClient.post(`${STORES_PATH}/search`, { json: criteria });
    const { results } = response.expectOk().json<StoreSearchResult>();
    return (results ?? []).map((store) => requireFields(store, STORE_FIELDS, "Found store"));
  }

  async listAllowed(userId: string): Promise<Store[]> {
    const response = await this.#httpClient.get(`${STORES_PATH}/allowed/${encodeURIComponent(userId)}`);
    return response
      .expectOk()
      .json<StoreData[]>()
      .map((store) => requireFields(store, STORE_FIELDS, "Allowed store"));
  }

  async delete(id: string): Promise<void> {
    (await this.#httpClient.delete(STORES_PATH, { query: { ids: id } })).expectOk();
  }

  async #fetch(id: string): Promise<StoreData | undefined> {
    const response = (await this.#httpClient.get(`${STORES_PATH}/${encodeURIComponent(id)}`)).expectOk();
    return response.json<StoreData | null>() ?? undefined;
  }
}
