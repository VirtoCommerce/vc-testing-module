import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommercePlatformCoreChangeLogChangeLogSearchResult as ChangeLogSearchResult,
  VirtoCommerceOrdersModuleCoreModelSearchCustomerOrderHistorySearchCriteria as CustomerOrderChangesSearchCriteria,
  VirtoCommerceOrdersModuleCoreModelCustomerOrder as CustomerOrderData,
  VirtoCommerceOrdersModuleCoreModelSearchCustomerOrderSearchCriteria as CustomerOrderSearchCriteria,
  VirtoCommerceOrdersModuleCoreModelSearchCustomerOrderSearchResult as CustomerOrderSearchResult,
  VirtoCommercePlatformCoreChangeLogOperationLog as OperationLog,
  OrderLineItem as OrderLineItemData,
  OrderShipment as OrderShipmentData,
  VirtoCommerceOrdersModuleCoreModelPaymentIn as PaymentInData,
} from "../generated/rest-api";

export type {
  ChangeLogSearchResult,
  CustomerOrderChangesSearchCriteria,
  CustomerOrderData,
  CustomerOrderSearchCriteria,
  CustomerOrderSearchResult,
  OperationLog,
  OrderLineItemData,
  OrderShipmentData,
  PaymentInData,
};

export const CUSTOMER_ORDER_FIELDS = ["id", "number", "status", "storeId", "customerId", "items"] as const;
export const ORDER_DOCUMENT_FIELDS = ["number"] as const;

export type CustomerOrder = WithRequired<CustomerOrderData, (typeof CUSTOMER_ORDER_FIELDS)[number]>;
export type PaymentIn = WithRequired<PaymentInData, (typeof ORDER_DOCUMENT_FIELDS)[number]>;
export type OrderShipment = WithRequired<OrderShipmentData, (typeof ORDER_DOCUMENT_FIELDS)[number]>;
