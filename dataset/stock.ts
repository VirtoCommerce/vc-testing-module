import type { InventoryInfo, InventoryInfoData } from "@api/rest/types/inventory";
import type { Dataset } from "./dataset";

import { INVENTORY_INFO_FIELDS } from "@api/rest/types/inventory";
import { requireFields } from "@core/required-fields";

export interface StockCondition {
  readonly stocks?: readonly string[];
  readonly lacks?: readonly string[];
}

export function getProductStock(dataset: Dataset, productId: string): InventoryInfo[] {
  return dataset.productInventories
    .filter((item) => item["productId"] === productId)
    .map((item) =>
      requireFields(item as InventoryInfoData, INVENTORY_INFO_FIELDS, `Dataset inventory of "${productId}"`),
    )
    .filter((inventory) => inventory.inStockQuantity > 0);
}

export function getStockQuantity(dataset: Dataset, productId: string, fulfillmentCenterId: string): number {
  const inventory = getProductStock(dataset, productId).find(
    (item) => item.fulfillmentCenterId === fulfillmentCenterId,
  );
  return requireFields(inventory, ["inStockQuantity"], `Stock of "${productId}" at "${fulfillmentCenterId}"`)
    .inStockQuantity;
}

export function findFulfillmentCenter(dataset: Dataset, condition: StockCondition, index = 0): string {
  const matching = getFulfillmentCenterIds(dataset).filter(
    (centerId) =>
      (condition.stocks ?? []).every((productId) => isStockedAt(dataset, productId, centerId)) &&
      (condition.lacks ?? []).every((productId) => !isStockedAt(dataset, productId, centerId)),
  );
  const centerId = matching[index];
  if (centerId === undefined) {
    throw new Error(
      `Dataset has ${matching.length} fulfillment center(s) matching ${JSON.stringify(condition)}, need #${index + 1}`,
    );
  }
  return centerId;
}

function getFulfillmentCenterIds(dataset: Dataset): string[] {
  return dataset.fulfillmentCenters.map(
    (item) => requireFields(item as { id?: string | null }, ["id"], "Dataset fulfillment center").id,
  );
}

function isStockedAt(dataset: Dataset, productId: string, fulfillmentCenterId: string): boolean {
  return getProductStock(dataset, productId).some((item) => item.fulfillmentCenterId === fulfillmentCenterId);
}
