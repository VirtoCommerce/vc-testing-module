import type { PickupLocationAddress, PickupLocationData } from "@api/rest/types/shipping";
import type { WithRequired } from "@core/required-fields";

import { uniqueId } from "@core/unique-id";

export type PickupLocationDraft = WithRequired<PickupLocationData, "id" | "storeId" | "name">;

export interface PickupLocationSources {
  readonly city: string;
  readonly fulfillmentCenterId: string | null;
  readonly transferFulfillmentCenterIds: readonly string[];
  readonly address?: Partial<PickupLocationAddress>;
}

export function newPickupLocation(
  storeId: string,
  namePrefix: string,
  sources: PickupLocationSources,
): PickupLocationDraft {
  const id = uniqueId("test-pickup-location");
  return {
    id,
    storeId,
    name: `${namePrefix} ${sources.city}`,
    isActive: true,
    fulfillmentCenterId: sources.fulfillmentCenterId,
    transferFulfillmentCenterIds: [...sources.transferFulfillmentCenterIds],
    deliveryDays: 2,
    storageDays: 7,
    address: {
      city: sources.city,
      countryCode: "USA",
      countryName: "United States",
      line1: `1 ${sources.city} Test Street`,
      postalCode: "10001",
      ...sources.address,
    },
  };
}
