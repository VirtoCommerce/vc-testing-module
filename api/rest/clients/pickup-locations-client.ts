import type { HttpClient } from "../../http/http-client";
import type { PickupLocation, PickupLocationData } from "../types/shipping";

import { requireFields } from "@core/required-fields";

import { PICKUP_LOCATION_FIELDS } from "../types/shipping";

const PICKUP_LOCATIONS_PATH = "/api/shipping/pickup-locations";

export class PickupLocationsClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async create(pickupLocation: PickupLocationData): Promise<PickupLocation> {
    const response = await this.#httpClient.post(PICKUP_LOCATIONS_PATH, { json: pickupLocation });
    return requireFields(
      response.expectOk().json<PickupLocationData>(),
      PICKUP_LOCATION_FIELDS,
      "Created pickup location",
    );
  }

  async update(pickupLocation: PickupLocationData): Promise<void> {
    (await this.#httpClient.put(PICKUP_LOCATIONS_PATH, { json: pickupLocation })).expectOk();
  }

  async delete(storeId: string, id: string): Promise<void> {
    (
      await this.#httpClient.delete(`${PICKUP_LOCATIONS_PATH}/${encodeURIComponent(storeId)}/${encodeURIComponent(id)}`)
    ).expectOk();
  }
}
