import type { CatalogProduct } from "@api/rest/types/catalog";
import type { CustomerOrderData, OrderLineItemData } from "@api/rest/types/orders";
import type { WithRequired } from "@core/required-fields";
import type { DatasetUser } from "../dataset";

export const ORDER_CURRENCY = "USD";
export const MAX_ORDER_NUMBER_LENGTH = 64;

export type CustomerOrderDraft = WithRequired<CustomerOrderData, "id" | "number" | "items">;

export function newOrder(storeId: string, customer: DatasetUser, items: OrderLineItemData[] = []): CustomerOrderDraft {
  const id = crypto.randomUUID();
  return {
    id,
    number: `TEST-${id.slice(0, 8).toUpperCase()}`,
    storeId,
    customerId: customer.id,
    customerName: customer.userName,
    currency: ORDER_CURRENCY,
    status: "New",
    items,
  };
}

export function newLineItem(product: CatalogProduct, price: number, quantity = 1): OrderLineItemData {
  return {
    id: crypto.randomUUID(),
    productId: product.id,
    sku: product.code,
    name: product.name,
    catalogId: product.catalogId,
    productType: "Physical",
    currency: ORDER_CURRENCY,
    price,
    quantity,
  };
}
