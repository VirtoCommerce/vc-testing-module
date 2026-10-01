import type { ProductPickupLocationFragment } from "@api/graphql/generated/graphql";
import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { ArrangedPickupLocations } from "@dataset/arrange/pickup-location";
import type { FrontendContext } from "@dataset/frontend-context";

import * as allure from "allure-js-commons";

import { CartPickupLocationsDocument } from "@api/graphql/generated/graphql";
import { PickupLocationsClient } from "@api/rest/clients/pickup-locations-client";
import { arrangeCart } from "@dataset/arrange/cart";
import { arrangePickupLocations, locationsArrangedIn } from "@dataset/arrange/pickup-location";
import { findFulfillmentCenter } from "@dataset/stock";
import { expect, test } from "@fixtures";

const MEMORY_PRODUCT_ID = "sodimm-crucial-ddr4-2400-8gb";
const PHONE_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black";
const ALL_LOCATIONS_PAGE_SIZE = 100;

test.beforeEach(async () => {
  await allure.feature("Cart / Pickup Locations");
});

test.describe("cart pickup locations (anonymous)", () => {
  test("cart pickup locations of a product missing at the same-day center are transfers", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
    dataset,
  }) => {
    const arranged = await test.step("arrange: locations whose same-day center lacks the product", () =>
      arrangePickupLocations(
        new PickupLocationsClient(platformAdminHttpClient),
        cleanupStack,
        frontendContext.storeId,
        [
          {
            city: "Transferville",
            fulfillmentCenterId: findFulfillmentCenter(dataset, { lacks: [MEMORY_PRODUCT_ID] }),
            transferFulfillmentCenterIds: [findFulfillmentCenter(dataset, { stocks: [MEMORY_PRODUCT_ID] })],
          },
          {
            city: "Globalton",
            fulfillmentCenterId: findFulfillmentCenter(dataset, { lacks: [MEMORY_PRODUCT_ID] }),
            transferFulfillmentCenterIds: [findFulfillmentCenter(dataset, { lacks: [MEMORY_PRODUCT_ID] }, 1)],
          },
        ],
      ));
    const cart = await test.step(`arrange: cart with ${MEMORY_PRODUCT_ID}`, () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: MEMORY_PRODUCT_ID, quantity: 1 }]));

    const locations = await test.step("act: get the cart pickup locations", () =>
      waitForArrangedLocations(graphqlClient, frontendContext, cart.id, arranged));

    await test.step("assert: the locations are transfer and global transfer", async () => {
      expect(availabilityByCity(locations)).toEqual({ Transferville: "Transfer", Globalton: "GlobalTransfer" });
    });
  });

  test("cart pickup locations of an in-stock product list same-day locations first", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
    dataset,
  }) => {
    const arranged = await test.step("arrange: same-day and transfer locations", () =>
      arrangePickupLocations(
        new PickupLocationsClient(platformAdminHttpClient),
        cleanupStack,
        frontendContext.storeId,
        [
          {
            city: "Transferville",
            fulfillmentCenterId: null,
            transferFulfillmentCenterIds: [findFulfillmentCenter(dataset, { stocks: [MEMORY_PRODUCT_ID] })],
          },
          {
            city: "Sameday",
            fulfillmentCenterId: findFulfillmentCenter(dataset, { stocks: [MEMORY_PRODUCT_ID] }),
            transferFulfillmentCenterIds: [],
          },
        ],
      ));
    const cart = await test.step(`arrange: cart with ${MEMORY_PRODUCT_ID}`, () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: MEMORY_PRODUCT_ID, quantity: 1 }]));
    await test.step("arrange: wait until the locations are searchable", () =>
      waitForArrangedLocations(graphqlClient, frontendContext, cart.id, arranged));

    const locations = await test.step("act: get every cart pickup location", () =>
      cartPickupLocations(graphqlClient, frontendContext, cart.id));

    await test.step("assert: the arranged same-day location is same-day", async () => {
      expect(availabilityByCity(locationsArrangedIn(locations, arranged))).toMatchObject({ Sameday: "Today" });
    });
    await test.step("assert: no same-day location follows another availability type", async () => {
      const firstOtherIndex = locations.findIndex((location) => location.availabilityType !== "Today");
      expect(firstOtherIndex).toBeGreaterThan(0);
      expect(locations.slice(firstOtherIndex).filter((location) => location.availabilityType === "Today")).toEqual([]);
    });
  });

  test("cart pickup locations of mixed products are same-day only where every product is stocked", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
    dataset,
  }) => {
    const memoryOnlyCenterId = findFulfillmentCenter(dataset, {
      stocks: [MEMORY_PRODUCT_ID],
      lacks: [PHONE_PRODUCT_ID],
    });
    const arranged = await test.step("arrange: locations stocking both, one, or one plus a transfer of the other", () =>
      arrangePickupLocations(
        new PickupLocationsClient(platformAdminHttpClient),
        cleanupStack,
        frontendContext.storeId,
        [
          {
            city: "Bothstock",
            fulfillmentCenterId: findFulfillmentCenter(dataset, { stocks: [MEMORY_PRODUCT_ID, PHONE_PRODUCT_ID] }),
            transferFulfillmentCenterIds: [],
          },
          {
            city: "Halfstock",
            fulfillmentCenterId: memoryOnlyCenterId,
            transferFulfillmentCenterIds: [],
          },
          {
            city: "Halftransfer",
            fulfillmentCenterId: memoryOnlyCenterId,
            transferFulfillmentCenterIds: [
              findFulfillmentCenter(dataset, { stocks: [PHONE_PRODUCT_ID], lacks: [MEMORY_PRODUCT_ID] }),
            ],
          },
        ],
      ));
    const cart = await test.step(`arrange: cart with ${MEMORY_PRODUCT_ID} and ${PHONE_PRODUCT_ID}`, () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [
        { productId: MEMORY_PRODUCT_ID, quantity: 1 },
        { productId: PHONE_PRODUCT_ID, quantity: 1 },
      ]));

    const locations = await test.step("act: get the cart pickup locations", () =>
      waitForArrangedLocations(graphqlClient, frontendContext, cart.id, arranged));

    await test.step("assert: a location missing a product is never same-day", async () => {
      expect(availabilityByCity(locations)).toEqual({
        Bothstock: "Today",
        Halfstock: "GlobalTransfer",
        Halftransfer: "Transfer",
      });
    });
  });

  test("cart pickup locations of a multi-region product include same-day and transfer", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
    dataset,
  }) => {
    const arranged = await test.step("arrange: locations served by two regions stocking the product", () =>
      arrangePickupLocations(
        new PickupLocationsClient(platformAdminHttpClient),
        cleanupStack,
        frontendContext.storeId,
        [
          {
            city: "Sameday",
            fulfillmentCenterId: findFulfillmentCenter(dataset, { stocks: [MEMORY_PRODUCT_ID] }, 0),
            transferFulfillmentCenterIds: [],
          },
          {
            city: "Transferville",
            fulfillmentCenterId: findFulfillmentCenter(dataset, { lacks: [MEMORY_PRODUCT_ID] }),
            transferFulfillmentCenterIds: [findFulfillmentCenter(dataset, { stocks: [MEMORY_PRODUCT_ID] }, 1)],
          },
        ],
      ));
    const cart = await test.step(`arrange: cart with ${MEMORY_PRODUCT_ID}`, () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: MEMORY_PRODUCT_ID, quantity: 1 }]));

    const locations = await test.step("act: get the cart pickup locations", () =>
      waitForArrangedLocations(graphqlClient, frontendContext, cart.id, arranged));

    await test.step("assert: one region is same-day and the other is a transfer", async () => {
      expect(availabilityByCity(locations)).toEqual({ Sameday: "Today", Transferville: "Transfer" });
    });
  });
});

async function cartPickupLocations(
  graphqlClient: GraphqlClient,
  context: FrontendContext,
  cartId: string,
): Promise<ProductPickupLocationFragment[]> {
  const { cartPickupLocations: connection } = await graphqlClient.execute(CartPickupLocationsDocument, {
    cartId,
    storeId: context.storeId,
    cultureName: context.cultureName,
    first: ALL_LOCATIONS_PAGE_SIZE,
  });
  return (connection?.items ?? []).filter((location): location is ProductPickupLocationFragment => location !== null);
}

async function waitForArrangedLocations(
  graphqlClient: GraphqlClient,
  context: FrontendContext,
  cartId: string,
  arranged: ArrangedPickupLocations,
): Promise<ProductPickupLocationFragment[]> {
  let found: ProductPickupLocationFragment[] = [];
  await expect
    .poll(async () => {
      found = locationsArrangedIn(await cartPickupLocations(graphqlClient, context, cartId), arranged);
      return found.length;
    })
    .toBe(arranged.locations.length);
  return found;
}

function availabilityByCity(locations: readonly ProductPickupLocationFragment[]): Record<string, string | null> {
  return Object.fromEntries(locations.map((location) => [location.address?.city, location.availabilityType]));
}
