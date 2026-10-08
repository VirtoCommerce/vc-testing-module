import type { HttpClient } from "../../http/http-client";
import type {
  ChangeLogSearchResult,
  CustomerOrder,
  CustomerOrderChangesSearchCriteria,
  CustomerOrderData,
  CustomerOrderSearchCriteria,
  CustomerOrderSearchResult,
  OperationLog,
  OrderShipment,
  OrderShipmentData,
  PaymentIn,
  PaymentInData,
} from "../types/orders";

import { requireFields } from "@core/required-fields";

import { CUSTOMER_ORDER_FIELDS, ORDER_DOCUMENT_FIELDS } from "../types/orders";

export const CUSTOMER_ORDERS_PATH = "/api/order/customerOrders";

export class OrdersClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async get(id: string): Promise<CustomerOrder> {
    return requireFields(await this.find(id), CUSTOMER_ORDER_FIELDS, `Order "${id}"`);
  }

  async find(id: string): Promise<CustomerOrder | undefined> {
    return this.#fetch(`${CUSTOMER_ORDERS_PATH}/${encodeURIComponent(id)}`, `Order "${id}"`);
  }

  async getByNumber(number: string): Promise<CustomerOrder> {
    const order = await this.#fetch(`${CUSTOMER_ORDERS_PATH}/number/${encodeURIComponent(number)}`, `Order ${number}`);
    return requireFields(order, CUSTOMER_ORDER_FIELDS, `Order ${number}`);
  }

  async create(order: CustomerOrderData): Promise<CustomerOrder> {
    const response = await this.#httpClient.post(CUSTOMER_ORDERS_PATH, { json: order });
    return requireFields(response.expectOk().json<CustomerOrderData>(), CUSTOMER_ORDER_FIELDS, "Created order");
  }

  async update(order: CustomerOrderData): Promise<void> {
    (await this.#httpClient.put(CUSTOMER_ORDERS_PATH, { json: order })).expectOk();
  }

  async recalculate(order: CustomerOrderData): Promise<CustomerOrder> {
    const response = await this.#httpClient.put(`${CUSTOMER_ORDERS_PATH}/recalculate`, { json: order });
    return requireFields(response.expectOk().json<CustomerOrderData>(), CUSTOMER_ORDER_FIELDS, "Recalculated order");
  }

  async search(criteria: CustomerOrderSearchCriteria): Promise<CustomerOrder[]> {
    const response = await this.#httpClient.post(`${CUSTOMER_ORDERS_PATH}/search`, { json: criteria });
    const { results } = response.expectOk().json<CustomerOrderSearchResult>();
    return (results ?? []).map((order) => requireFields(order, CUSTOMER_ORDER_FIELDS, "Found order"));
  }

  async isIndexedSearchEnabled(): Promise<boolean> {
    const response = await this.#httpClient.get(`${CUSTOMER_ORDERS_PATH}/indexed/searchEnabled`);
    return response.expectOk().json<{ result: boolean }>().result;
  }

  async newPayment(orderId: string): Promise<PaymentIn> {
    const response = await this.#httpClient.get(`${CUSTOMER_ORDERS_PATH}/${encodeURIComponent(orderId)}/payments/new`);
    return requireFields(
      response.expectOk().json<PaymentInData>(),
      ORDER_DOCUMENT_FIELDS,
      `New payment of "${orderId}"`,
    );
  }

  async newShipment(orderId: string): Promise<OrderShipment> {
    const path = `${CUSTOMER_ORDERS_PATH}/${encodeURIComponent(orderId)}/shipments/new`;
    const response = await this.#httpClient.get(path);
    return requireFields(
      response.expectOk().json<OrderShipmentData>(),
      ORDER_DOCUMENT_FIELDS,
      `New shipment of "${orderId}"`,
    );
  }

  async searchChanges(criteria: CustomerOrderChangesSearchCriteria): Promise<ChangeLogSearchResult> {
    const response = await this.#httpClient.post(`${CUSTOMER_ORDERS_PATH}/searchChanges`, { json: criteria });
    return response.expectOk().json<ChangeLogSearchResult>();
  }

  async getChanges(orderId: string): Promise<OperationLog[]> {
    const response = await this.#httpClient.get(`${CUSTOMER_ORDERS_PATH}/${encodeURIComponent(orderId)}/changes`);
    return response.expectOk().json<OperationLog[]>();
  }

  async delete(id: string): Promise<void> {
    (await this.#httpClient.delete(CUSTOMER_ORDERS_PATH, { query: { ids: id } })).expectOk();
  }

  async #fetch(path: string, label: string): Promise<CustomerOrder | undefined> {
    const response = await this.#httpClient.get(path);
    if (response.status === 404) {
      return undefined;
    }
    return requireFields(response.expectOk().json<CustomerOrderData>(), CUSTOMER_ORDER_FIELDS, label);
  }
}
