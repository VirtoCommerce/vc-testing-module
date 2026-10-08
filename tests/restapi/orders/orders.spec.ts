import type { CustomerOrder } from "@api/rest/types/orders";
import type { CleanupStack } from "@core/cleanup-stack";
import type { CustomerOrderDraft } from "@dataset/builders/order";
import type { Dataset } from "@dataset/dataset";

import * as allure from "allure-js-commons";

import { CUSTOMER_ORDERS_PATH, OrdersClient } from "@api/rest/clients/orders-client";
import { MAX_ORDER_NUMBER_LENGTH, newLineItem, newOrder } from "@dataset/builders/order";
import { getCredentials, getProduct, getUser } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const SEEDED_PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai";
const LINE_ITEM_PRICE = 100;
const CHANGE_LOG_TIMEOUT_MS = 30_000;

test.beforeEach(async () => {
  await allure.feature("Orders");
});

test.describe("customer orders (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create an order", async ({ httpClient, cleanupStack, dataset, env }) => {
    const ordersClient = new OrdersClient(httpClient);
    const draft = newOrder(env.storeId, getUser(dataset, USERNAME));
    cleanupStack.push(`delete order ${draft.number}`, () => ordersClient.delete(draft.id));

    const order = await test.step("act: create order", () => ordersClient.create(draft));

    await test.step("assert: order is new in the seeded store", async () => {
      expect(order).toMatchObject({ id: draft.id, number: draft.number, status: "New", storeId: env.storeId });
    });
  });

  test("get an order by id", async ({ httpClient, cleanupStack, dataset, env }) => {
    const ordersClient = new OrdersClient(httpClient);
    const order = await test.step("arrange: order", () =>
      arrangeOrder(ordersClient, cleanupStack, newOrder(env.storeId, getUser(dataset, USERNAME))));

    const reloaded = await test.step("act: get order", () => ordersClient.get(order.id));

    await test.step("assert: fields match the created order", async () => {
      expect(reloaded).toMatchObject({ id: order.id, number: order.number, storeId: order.storeId });
    });
  });

  test("get an order by number", async ({ httpClient, cleanupStack, dataset, env }) => {
    const ordersClient = new OrdersClient(httpClient);
    const order = await test.step("arrange: order", () =>
      arrangeOrder(ordersClient, cleanupStack, newOrder(env.storeId, getUser(dataset, USERNAME))));

    const reloaded = await test.step("act: get order by number", () => ordersClient.getByNumber(order.number));

    await test.step("assert: the same order is returned", async () => {
      expect(reloaded).toMatchObject({ id: order.id, number: order.number });
    });
  });

  test("get a missing order", async ({ httpClient }) => {
    const ordersClient = new OrdersClient(httpClient);

    const order = await test.step("act: get order by a missing id", () => ordersClient.find(crypto.randomUUID()));

    await test.step("assert: order is not found", async () => {
      expect(order).toBeUndefined();
    });
  });

  test("list orders", async ({ httpClient, cleanupStack, dataset, env }) => {
    const ordersClient = new OrdersClient(httpClient);
    await test.step("arrange: order", () =>
      arrangeOrder(ordersClient, cleanupStack, newOrder(env.storeId, getUser(dataset, USERNAME))));

    const orders = await test.step("act: list orders", () => ordersClient.search({ take: 5 }));

    await test.step("assert: orders are listed", async () => {
      expect(orders.length).toBeGreaterThan(0);
    });
  });

  test("search orders by number", async ({ httpClient, cleanupStack, dataset, env }) => {
    const ordersClient = new OrdersClient(httpClient);
    const order = await test.step("arrange: order", () =>
      arrangeOrder(ordersClient, cleanupStack, newOrder(env.storeId, getUser(dataset, USERNAME))));

    const found = await test.step("act: search by order number", () =>
      ordersClient.search({ keyword: order.number, take: 5 }));

    await test.step("assert: order is in the results", async () => {
      expect(found.map(({ id }) => id)).toContain(order.id);
    });
  });

  test("check whether indexed order search is enabled", async ({ httpClient }) => {
    const ordersClient = new OrdersClient(httpClient);

    const enabled = await test.step("act: check indexed search", () => ordersClient.isIndexedSearchEnabled());

    await test.step("assert: flag is a boolean", async () => {
      expect(typeof enabled).toBe("boolean");
    });
  });

  test("generate a new payment for an order", async ({ httpClient, cleanupStack, dataset, env }) => {
    const ordersClient = new OrdersClient(httpClient);
    const order = await test.step("arrange: order with a line item", () =>
      arrangeOrder(ordersClient, cleanupStack, orderWithLineItem(dataset, env.storeId)));

    const payment = await test.step("act: generate payment", () => ordersClient.newPayment(order.id));

    await test.step("assert: payment is numbered and belongs to the order customer", async () => {
      expect(payment).toMatchObject({ customerId: order.customerId, number: expect.any(String) });
    });
  });

  test("generate a new shipment for an order", async ({ httpClient, cleanupStack, dataset, env }) => {
    const ordersClient = new OrdersClient(httpClient);
    const order = await test.step("arrange: order with a line item", () =>
      arrangeOrder(ordersClient, cleanupStack, orderWithLineItem(dataset, env.storeId)));

    const shipment = await test.step("act: generate shipment", () => ordersClient.newShipment(order.id));

    await test.step("assert: shipment is numbered", async () => {
      expect(shipment.number).toEqual(expect.any(String));
    });
  });

  test("change the status of an order", async ({ httpClient, cleanupStack, dataset, env }) => {
    const ordersClient = new OrdersClient(httpClient);
    const order = await test.step("arrange: order", () =>
      arrangeOrder(ordersClient, cleanupStack, newOrder(env.storeId, getUser(dataset, USERNAME))));

    await test.step("act: set status to Processing", () => ordersClient.update({ ...order, status: "Processing" }));

    await test.step("assert: order is processing", async () => {
      expect((await ordersClient.get(order.id)).status).toBe("Processing");
    });
  });

  test("recalculate order totals after a quantity change", async ({ httpClient, cleanupStack, dataset, env }) => {
    const ordersClient = new OrdersClient(httpClient);
    const order = await test.step("arrange: order with a line item", () =>
      arrangeOrder(ordersClient, cleanupStack, orderWithLineItem(dataset, env.storeId)));

    const recalculated = await test.step("act: recalculate with quantity 2", () =>
      ordersClient.recalculate(withFirstItemQuantity(order, 2)));

    await test.step("assert: total is price times quantity", async () => {
      expect(recalculated.items[0]).toMatchObject({ quantity: 2, price: LINE_ITEM_PRICE });
      expect(recalculated.total).toBe(LINE_ITEM_PRICE * 2);
    });
  });

  test("attach a payment and a shipment to an order", async ({ httpClient, cleanupStack, dataset, env }) => {
    const ordersClient = new OrdersClient(httpClient);
    const order = await test.step("arrange: order with a line item", () =>
      arrangeOrder(ordersClient, cleanupStack, orderWithLineItem(dataset, env.storeId)));
    const payment = await test.step("arrange: new payment", () => ordersClient.newPayment(order.id));
    const shipment = await test.step("arrange: new shipment", () => ordersClient.newShipment(order.id));
    const recalculated = await test.step("arrange: recalculated order", () =>
      ordersClient.recalculate({ ...withFirstItemQuantity(order, 2), inPayments: [payment], shipments: [shipment] }));

    await test.step("act: save order", () => ordersClient.update(recalculated));

    await test.step("assert: order keeps the payment, shipment and quantity", async () => {
      const saved = await ordersClient.getByNumber(order.number);
      expect(saved.items[0]?.quantity).toBe(2);
      expect(saved.inPayments?.map(({ number }) => number)).toEqual([payment.number]);
      expect(saved.shipments?.map(({ number }) => number)).toEqual([shipment.number]);
    });
  });

  test("record order changes after an update", async ({ httpClient, cleanupStack, dataset, env }) => {
    const ordersClient = new OrdersClient(httpClient);
    const order = await test.step("arrange: order with a line item", () =>
      arrangeOrder(ordersClient, cleanupStack, orderWithLineItem(dataset, env.storeId)));
    const initial = await test.step("arrange: initial change count", () =>
      ordersClient.searchChanges({ orderId: order.id, take: 10 }));
    const payment = await test.step("arrange: new payment", () => ordersClient.newPayment(order.id));
    const shipment = await test.step("arrange: new shipment", () => ordersClient.newShipment(order.id));

    await test.step("act: save order with a payment, a shipment and a new quantity", async () =>
      ordersClient.update(
        await ordersClient.recalculate({
          ...withFirstItemQuantity(order, 2),
          inPayments: [payment],
          shipments: [shipment],
        }),
      ));

    await test.step("assert: change count grows", async () => {
      await expect
        .poll(async () => (await ordersClient.searchChanges({ orderId: order.id, take: 10 })).totalCount, {
          timeout: CHANGE_LOG_TIMEOUT_MS,
        })
        .toBeGreaterThan(initial.totalCount ?? 0);
    });
  });

  test("delete an order", async ({ httpClient, cleanupStack, dataset, env }) => {
    const ordersClient = new OrdersClient(httpClient);
    const order = await test.step("arrange: order", () =>
      arrangeOrder(ordersClient, cleanupStack, newOrder(env.storeId, getUser(dataset, USERNAME))));

    await test.step("act: delete order", () => ordersClient.delete(order.id));

    await test.step("assert: order is not found", async () => {
      expect(await ordersClient.find(order.id)).toBeUndefined();
      expect((await ordersClient.search({ keyword: order.number })).map(({ id }) => id)).not.toContain(order.id);
    });
  });

  test("reject an order number that is too long", async ({ httpClient, cleanupStack, dataset, env }) => {
    const ordersClient = new OrdersClient(httpClient);
    const draft = { ...newOrder(env.storeId, getUser(dataset, USERNAME)), number: "X".repeat(65) };
    cleanupStack.push(`delete order ${draft.id}`, () => ordersClient.delete(draft.id));

    const response = await test.step("act: create order with a 65-character number", () =>
      httpClient.post(CUSTOMER_ORDERS_PATH, { json: draft }));

    await test.step("assert: order number length is rejected", async () => {
      expect(response.status).toBe(400);
      expect(response.text).toContain(`must be ${MAX_ORDER_NUMBER_LENGTH} characters or fewer`);
    });
  });
});

async function arrangeOrder(
  ordersClient: OrdersClient,
  cleanupStack: CleanupStack,
  draft: CustomerOrderDraft,
): Promise<CustomerOrder> {
  cleanupStack.push(`delete order ${draft.number}`, () => ordersClient.delete(draft.id));
  return ordersClient.create(draft);
}

function orderWithLineItem(dataset: Dataset, storeId: string): CustomerOrderDraft {
  const product = getProduct(dataset, SEEDED_PRODUCT_ID);
  return newOrder(storeId, getUser(dataset, USERNAME), [newLineItem(product, LINE_ITEM_PRICE)]);
}

function withFirstItemQuantity(order: CustomerOrder, quantity: number): CustomerOrder {
  return { ...order, items: order.items.map((item, index) => (index === 0 ? { ...item, quantity } : item)) };
}
