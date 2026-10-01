import type { WithRequired } from "@core/required-fields";
import type { VirtoCommerceInventoryModuleCoreModelInventoryInfo as InventoryInfoData } from "../generated/rest-api";

export type { InventoryInfoData };

export const INVENTORY_INFO_FIELDS = ["productId", "fulfillmentCenterId", "inStockQuantity"] as const;

export type InventoryInfo = WithRequired<InventoryInfoData, (typeof INVENTORY_INFO_FIELDS)[number]>;
