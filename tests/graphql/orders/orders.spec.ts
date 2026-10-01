import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { Dataset } from "@dataset/dataset";

import * as allure from "allure-js-commons";

import { OrderDocument, OrganizationOrdersDocument } from "@api/graphql/generated/graphql";
import { requireFields } from "@core/required-fields";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const MAINTAINER_USERNAME = "acme_store_maintainer_1@acme.com";
const ADMINISTRATOR_USERNAME = "acme_store_administrator@acme.com";
const ORDER_NUMBER = "CO251029-00038";
const STATUSES = ["New", "Completed", "Pending", "Payment required", "ReadyForPickup"] as const;
const ORDERS_PAGE_SIZE = 100;
const DATE_WINDOW_MS = 7 * 24 * 60 * 60 * 1000;

test.beforeEach(async () => {
  await allure.feature("Orders");
});

test.describe("orders (seeded maintainer)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, MAINTAINER_USERNAME)) });

  test("get an order by number", async ({ graphqlClient, frontendContext }) => {
    const { order } = await test.step(`act: get order ${ORDER_NUMBER}`, () =>
      graphqlClient.execute(OrderDocument, { number: ORDER_NUMBER, cultureName: frontendContext.cultureName }));

    await test.step("assert: the order is returned", async () => {
      expect(order?.number).toBe(ORDER_NUMBER);
    });
  });

  for (const status of STATUSES) {
    test(`filter organization orders by status ${status}`, async ({ graphqlClient, frontendContext, dataset }) => {
      const orders = await test.step(`act: filter by status ${status}`, () =>
        organizationOrders(graphqlClient, {
          organizationId: frontendContext.organizationId,
          filter: `status:"${status}"`,
        }));

      await test.step(`assert: only ${status} orders, including every seeded one`, async () => {
        expect(orders.filter((order) => order.status !== status).map(({ number }) => number)).toEqual([]);
        expect(orders.length).toBeGreaterThanOrEqual(seededOrderCount(dataset, frontendContext.organizationId, status));
        expect(orders.length).toBeGreaterThan(0);
      });
    });
  }

  test("filter organization orders by created date", async ({ graphqlClient, frontendContext }) => {
    const orders = await test.step("arrange: every organization order", () =>
      organizationOrders(graphqlClient, { organizationId: frontendContext.organizationId }));
    const anchor = Date.parse(requireFields(orders[0], ["createdDate"], "Newest organization order").createdDate);
    const from = new Date(anchor - DATE_WINDOW_MS);
    const to = new Date(anchor + DATE_WINDOW_MS);

    const inRange = await test.step(`act: filter by created date ${from.toISOString()} to ${to.toISOString()}`, () =>
      organizationOrders(graphqlClient, {
        organizationId: frontendContext.organizationId,
        filter: `createddate:["${from.toISOString()}" TO "${to.toISOString()}"]`,
      }));

    await test.step("assert: every order was created inside the range", async () => {
      expect(inRange.length).toBeGreaterThan(0);
      const outside = inRange.filter((order) => {
        const created = Date.parse(order.createdDate);
        return created < from.getTime() || created > to.getTime();
      });
      expect(outside.map(({ number }) => number)).toEqual([]);
    });
  });
});

test.describe("orders (seeded store administrator)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, ADMINISTRATOR_USERNAME)) });

  test("search organization orders by number", async ({ graphqlClient }) => {
    const orders = await test.step(`act: filter by number ${ORDER_NUMBER}`, () =>
      organizationOrders(graphqlClient, { filter: `number:${ORDER_NUMBER}` }));

    await test.step("assert: exactly that order is found", async () => {
      expect(orders.map(({ number }) => number)).toEqual([ORDER_NUMBER]);
    });
  });

  for (const direction of ["asc", "desc"] as const) {
    test(`sort organization orders by created date ${direction}`, async ({ graphqlClient }) => {
      const orders = await test.step(`act: sort by createdDate:${direction}`, () =>
        organizationOrders(graphqlClient, { sort: `createdDate:${direction}` }));

      await test.step(`assert: orders are in ${direction} date order`, async () => {
        const dates = orders.map(({ createdDate }) => Date.parse(createdDate));
        expect(dates.length).toBeGreaterThan(1);
        expect(dates).toEqual(sorted(dates, direction));
      });
    });

    test(`sort organization orders by total ${direction}`, async ({ graphqlClient }) => {
      const orders = await test.step(`act: sort by total:${direction}`, () =>
        organizationOrders(graphqlClient, { sort: `total:${direction}` }));

      await test.step(`assert: orders are in ${direction} total order`, async () => {
        const totals = orders.map(({ total }) => total.amount);
        expect(totals.length).toBeGreaterThan(1);
        expect(totals).toEqual(sorted(totals, direction));
      });
    });
  }
});

async function organizationOrders(
  graphqlClient: GraphqlClient,
  variables: { organizationId?: string | undefined; filter?: string; sort?: string },
) {
  const { organizationOrders: page } = await graphqlClient.execute(OrganizationOrdersDocument, {
    ...variables,
    first: ORDERS_PAGE_SIZE,
  });
  return (page?.items ?? []).flatMap((order) => (order === null ? [] : [order]));
}

function seededOrderCount(dataset: Dataset, organizationId: string | undefined, status: string): number {
  return dataset.orders.filter((order) => order["organizationId"] === organizationId && order["status"] === status)
    .length;
}

function sorted(values: readonly number[], direction: "asc" | "desc"): number[] {
  return [...values].sort((left, right) => (direction === "asc" ? left - right : right - left));
}
