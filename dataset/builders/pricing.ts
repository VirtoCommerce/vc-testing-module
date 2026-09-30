import type { PriceData, PricelistAssignmentData, PricelistData } from "@api/rest/types/pricing";

import { uniqueId } from "@core/unique-id";

import { SEEDED_CATALOG_ID } from "./catalog";

export const PRICELIST_CURRENCY = "USD";

export function newPricelist(name = uniqueId("test-pricelist")): PricelistData {
  return { name, currency: PRICELIST_CURRENCY };
}

export function newPrice(pricelistId: string, productId: string, list: number): PriceData {
  return { pricelistId, productId, list, minQuantity: 1, currency: PRICELIST_CURRENCY };
}

export function newPricelistAssignment(
  pricelistId: string,
  name = uniqueId("test-assignment"),
): PricelistAssignmentData {
  return { pricelistId, catalogId: SEEDED_CATALOG_ID, name };
}
