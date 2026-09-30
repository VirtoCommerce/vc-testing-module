import type { PickupLocationsClient } from "@api/rest/clients/pickup-locations-client";
import type { PickupLocation } from "@api/rest/types/shipping";
import type { CleanupStack } from "@core/cleanup-stack";
import type { PickupLocationDraft, PickupLocationSources } from "../builders/shipping";

import { uniqueId } from "@core/unique-id";

import { newPickupLocation } from "../builders/shipping";

export async function arrangePickupLocation(
  pickupLocationsClient: PickupLocationsClient,
  cleanupStack: CleanupStack,
  draft: PickupLocationDraft,
): Promise<PickupLocation> {
  cleanupStack.push(`delete pickup location ${draft.name}`, () =>
    pickupLocationsClient.delete(draft.storeId, draft.id),
  );
  return pickupLocationsClient.create(draft);
}

export interface ArrangedPickupLocations {
  readonly namePrefix: string;
  readonly locations: readonly PickupLocation[];
}

export async function arrangePickupLocations(
  pickupLocationsClient: PickupLocationsClient,
  cleanupStack: CleanupStack,
  storeId: string,
  sources: readonly PickupLocationSources[],
): Promise<ArrangedPickupLocations> {
  const namePrefix = uniqueId("test-pickup");
  const locations: PickupLocation[] = [];
  for (const source of sources) {
    locations.push(
      await arrangePickupLocation(pickupLocationsClient, cleanupStack, newPickupLocation(storeId, namePrefix, source)),
    );
  }
  return { namePrefix, locations };
}

export function locationsArrangedIn<Location extends { readonly name: string }>(
  locations: readonly (Location | null)[],
  arranged: ArrangedPickupLocations,
): Location[] {
  return locations.filter((location): location is Location => location?.name.startsWith(arranged.namePrefix) ?? false);
}
