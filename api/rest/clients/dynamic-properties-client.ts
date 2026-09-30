import type { HttpClient } from "../../http/http-client";
import type {
  DynamicProperty,
  DynamicPropertyData,
  DynamicPropertySearchCriteria,
  DynamicPropertySearchResult,
} from "../types/platform";

import { requireFields } from "@core/required-fields";

import { DYNAMIC_PROPERTY_FIELDS } from "../types/platform";

const DYNAMIC_PATH = "/api/platform/dynamic";
const PROPERTIES_PATH = `${DYNAMIC_PATH}/properties`;

export class DynamicPropertiesClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async listObjectTypes(): Promise<string[]> {
    return (await this.#httpClient.get(`${DYNAMIC_PATH}/types`)).expectOk().json<string[]>();
  }

  async create(property: DynamicPropertyData): Promise<DynamicProperty> {
    const response = await this.#httpClient.post(PROPERTIES_PATH, { json: property });
    return requireFields(response.expectOk().json<DynamicPropertyData>(), DYNAMIC_PROPERTY_FIELDS, "Created property");
  }

  async search(criteria: DynamicPropertySearchCriteria): Promise<DynamicProperty[]> {
    const response = await this.#httpClient.post(`${PROPERTIES_PATH}/search`, { json: criteria });
    const { results } = response.expectOk().json<DynamicPropertySearchResult>();
    return (results ?? []).map((property) => requireFields(property, DYNAMIC_PROPERTY_FIELDS, "Found property"));
  }

  async delete(ids: readonly string[]): Promise<void> {
    (await this.#httpClient.delete(PROPERTIES_PATH, { query: { propertyIds: ids } })).expectOk();
  }
}
