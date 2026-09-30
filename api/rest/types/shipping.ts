import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommerceShippingModuleCoreModelPickupLocationAddress as PickupLocationAddress,
  VirtoCommerceShippingModuleCoreModelPickupLocation as PickupLocationData,
} from "../generated/rest-api";

export type { PickupLocationAddress, PickupLocationData };

export const PICKUP_LOCATION_FIELDS = ["id", "storeId", "name"] as const;

export type PickupLocation = WithRequired<PickupLocationData, (typeof PICKUP_LOCATION_FIELDS)[number]>;
