import type {
  PickupLocationFragment,
  ProductPickupAvailabilityType,
  ProductPickupLocationFragment,
} from "@api/graphql/generated/graphql";
import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { ArrangedPickupLocations } from "@dataset/arrange/pickup-location";
import type { PickupLocationDraft } from "@dataset/builders/shipping";
import type { Dataset } from "@dataset/dataset";
import type { FrontendContext } from "@dataset/frontend-context";

import * as allure from "allure-js-commons";

import { PickupLocationsDocument, ProductPickupLocationsDocument } from "@api/graphql/generated/graphql";
import { CatalogClient } from "@api/rest/clients/catalog-client";
import { PickupLocationsClient } from "@api/rest/clients/pickup-locations-client";
import { uniqueId } from "@core/unique-id";
import { arrangePickupLocation, arrangePickupLocations, locationsArrangedIn } from "@dataset/arrange/pickup-location";
import { newCatalog, newCategory, newProduct } from "@dataset/builders/catalog";
import { newPickupLocation } from "@dataset/builders/shipping";
import { findFulfillmentCenter, getProductStock, getStockQuantity } from "@dataset/stock";
import { expect, test } from "@fixtures";

const PAGE_SIZE = 5;
const ALL_LOCATIONS_PAGE_SIZE = 100;
const KEYWORD = "Berlin";
const STOCKED_PRODUCT_ID = "sodimm-crucial-ddr4-2400-8gb";
const OUT_OF_STOCK_PRODUCT_ID = "sodimm-samsung-ddr5-4800-8gb";
const AVAILABILITY_ORDER: readonly (ProductPickupAvailabilityType | null)[] = ["Today", "Transfer", "GlobalTransfer"];
const IN_STOCK = { stocks: [STOCKED_PRODUCT_ID] };
const OUT_OF_STOCK = { lacks: [STOCKED_PRODUCT_ID] };

test.beforeEach(async () => {
  await allure.feature("Catalog / Pickup Locations");
});

test.describe("pickup locations (anonymous)", () => {
  test("page through pickup locations", async ({ graphqlClient, frontendContext }) => {
    const { pickupLocations: page } = await test.step(`act: get the first ${PAGE_SIZE} locations`, () =>
      graphqlClient.execute(PickupLocationsDocument, { storeId: frontendContext.storeId, first: PAGE_SIZE }));
    const { pickupLocations: all } = await test.step("act: get every location", () =>
      graphqlClient.execute(PickupLocationsDocument, {
        storeId: frontendContext.storeId,
        first: ALL_LOCATIONS_PAGE_SIZE,
      }));

    await test.step("assert: the page is full and every location has an address", async () => {
      expect(page?.items).toHaveLength(PAGE_SIZE);
      expect(all?.items?.length).toBeGreaterThan(PAGE_SIZE);
      for (const location of all?.items ?? []) {
        expect(location?.address).toMatchObject({
          city: expect.any(String),
          countryName: expect.any(String),
          line1: expect.any(String),
        });
      }
    });
  });

  test("filter pickup locations by keyword", async ({ graphqlClient, frontendContext }) => {
    const { pickupLocations } = await test.step(`act: search locations for "${KEYWORD}"`, () =>
      graphqlClient.execute(PickupLocationsDocument, { storeId: frontendContext.storeId, keyword: KEYWORD }));

    await test.step(`assert: every location mentions ${KEYWORD}`, async () => {
      const names = (pickupLocations?.items ?? []).map((location) => location?.name ?? "");
      expect(names.length).toBeGreaterThan(0);
      expect(names.filter((name) => !name.includes(KEYWORD))).toEqual([]);
    });
  });
});

test.describe("pickup location administration (anonymous)", () => {
  test("an updated pickup location shows its new name and address", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
    dataset,
  }) => {
    const pickupLocationsClient = new PickupLocationsClient(platformAdminHttpClient);
    const location = await test.step("arrange: pickup location", () =>
      arrangePickupLocation(
        pickupLocationsClient,
        cleanupStack,
        newStorePickupLocation(frontendContext, dataset, "Oldtown"),
      ));
    const newAddress = { city: "Newtown", line1: "2 Updated Street", regionId: "CA", regionName: "California" };
    const changes = {
      name: `${location.name} Updated`,
      description: "Updated by an automated test",
      address: { ...location.address, ...newAddress },
    };

    await test.step("act: rename the location and move it to Newtown", () =>
      pickupLocationsClient.update({ ...location, ...changes }));

    await test.step("assert: the frontend sees the new name, description and address", async () => {
      await expect
        .poll(() => storePickupLocation(graphqlClient, frontendContext, location.id))
        .toMatchObject({ name: changes.name, description: changes.description, address: newAddress });
    });
  });

  test("a deactivated pickup location is hidden", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
    dataset,
  }) => {
    const pickupLocationsClient = new PickupLocationsClient(platformAdminHttpClient);
    const location = await test.step("arrange: active pickup location", () =>
      arrangePickupLocation(
        pickupLocationsClient,
        cleanupStack,
        newStorePickupLocation(frontendContext, dataset, "Closingtown"),
      ));
    await test.step("arrange: the frontend lists the location", async () => {
      await expect.poll(() => storePickupLocation(graphqlClient, frontendContext, location.id)).toBeDefined();
    });

    await test.step("act: deactivate the location", () =>
      pickupLocationsClient.update({ ...location, isActive: false }));

    await test.step("assert: the frontend no longer lists the location", async () => {
      await expect.poll(() => storePickupLocation(graphqlClient, frontendContext, location.id)).toBeUndefined();
    });
  });
});

test.describe("product pickup locations (anonymous)", () => {
  test("page product pickup locations with first", async ({ graphqlClient, frontendContext }) => {
    const { productPickupLocations: page } = await test.step(`act: get the first ${PAGE_SIZE} locations`, () =>
      graphqlClient.execute(ProductPickupLocationsDocument, {
        productId: STOCKED_PRODUCT_ID,
        storeId: frontendContext.storeId,
        cultureName: frontendContext.cultureName,
        first: PAGE_SIZE,
      }));
    const all = await test.step("act: get every location", () =>
      productPickupLocations(graphqlClient, frontendContext, STOCKED_PRODUCT_ID));

    await test.step(`assert: the page holds exactly ${PAGE_SIZE} of more locations`, async () => {
      expect(all.length).toBeGreaterThan(PAGE_SIZE);
      expect(page?.items).toHaveLength(PAGE_SIZE);
    });
  });

  test("product pickup locations include every availability type", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
    dataset,
  }) => {
    const arranged = await test.step("arrange: same-day, transfer and global-transfer locations", () =>
      arrangePickupLocations(
        new PickupLocationsClient(platformAdminHttpClient),
        cleanupStack,
        frontendContext.storeId,
        [
          {
            city: "Sameday",
            fulfillmentCenterId: findFulfillmentCenter(dataset, IN_STOCK),
            transferFulfillmentCenterIds: [],
          },
          {
            city: "Transferville",
            fulfillmentCenterId: findFulfillmentCenter(dataset, OUT_OF_STOCK),
            transferFulfillmentCenterIds: [findFulfillmentCenter(dataset, IN_STOCK)],
          },
          {
            city: "Globalton",
            fulfillmentCenterId: findFulfillmentCenter(dataset, OUT_OF_STOCK),
            transferFulfillmentCenterIds: [findFulfillmentCenter(dataset, OUT_OF_STOCK, 1)],
          },
        ],
      ));

    const locations = await test.step(`act: get pickup locations of ${STOCKED_PRODUCT_ID}`, () =>
      waitForArrangedLocations(graphqlClient, frontendContext, STOCKED_PRODUCT_ID, arranged));

    await test.step("assert: each location has the availability its fulfillment centers allow", async () => {
      expect(availabilityByCity(locations)).toEqual({
        Sameday: "Today",
        Transferville: "Transfer",
        Globalton: "GlobalTransfer",
      });
    });
  });

  test("same-day pickup locations report the stock of their fulfillment center", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
    dataset,
  }) => {
    const centerId = findFulfillmentCenter(dataset, IN_STOCK);
    const arranged = await test.step(`arrange: location served by ${centerId}`, () =>
      arrangePickupLocations(
        new PickupLocationsClient(platformAdminHttpClient),
        cleanupStack,
        frontendContext.storeId,
        [{ city: "Sameday", fulfillmentCenterId: centerId, transferFulfillmentCenterIds: [] }],
      ));

    const locations = await test.step(`act: get pickup locations of ${STOCKED_PRODUCT_ID}`, () =>
      waitForArrangedLocations(graphqlClient, frontendContext, STOCKED_PRODUCT_ID, arranged));

    await test.step(`assert: the location is same-day with the stock of ${centerId}`, async () => {
      expect(locations).toEqual([
        expect.objectContaining({
          availabilityType: "Today",
          availableQuantity: getStockQuantity(dataset, STOCKED_PRODUCT_ID, centerId),
        }),
      ]);
    });
  });

  test("transfer pickup locations in several cities report the stock of their transfer centers", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
    dataset,
  }) => {
    const firstCenterId = findFulfillmentCenter(dataset, IN_STOCK, 0);
    const secondCenterId = findFulfillmentCenter(dataset, IN_STOCK, 1);
    const arranged = await test.step("arrange: two transfer locations served by different centers", () =>
      arrangePickupLocations(
        new PickupLocationsClient(platformAdminHttpClient),
        cleanupStack,
        frontendContext.storeId,
        [
          { city: "Denver", fulfillmentCenterId: null, transferFulfillmentCenterIds: [firstCenterId] },
          { city: "Austin", fulfillmentCenterId: null, transferFulfillmentCenterIds: [secondCenterId] },
        ],
      ));

    const locations = await test.step(`act: get pickup locations of ${STOCKED_PRODUCT_ID}`, () =>
      waitForArrangedLocations(graphqlClient, frontendContext, STOCKED_PRODUCT_ID, arranged));

    await test.step("assert: each city is a transfer with the stock of its own center", async () => {
      expect(quantityByCity(locations, "Transfer")).toEqual({
        Denver: getStockQuantity(dataset, STOCKED_PRODUCT_ID, firstCenterId),
        Austin: getStockQuantity(dataset, STOCKED_PRODUCT_ID, secondCenterId),
      });
    });
  });

  test("a product without inventory tracking is available same-day everywhere without a quantity", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
  }) => {
    const catalogClient = new CatalogClient(platformAdminHttpClient);
    const product = await test.step("arrange: product that does not track inventory", async () => {
      const catalog = await catalogClient.saveCatalog(newCatalog());
      cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
      const category = await catalogClient.saveCategory(newCategory(catalog.id));
      return catalogClient.saveProduct({ ...newProduct(catalog.id, category.id), trackInventory: false });
    });

    const locations = await test.step(`act: get pickup locations of ${product.code}`, () =>
      productPickupLocations(graphqlClient, frontendContext, product.id));

    await test.step("assert: every location is same-day and reports no quantity", async () => {
      expect(locations.length).toBeGreaterThan(0);
      expect(locations.filter((location) => location.availabilityType !== "Today")).toEqual([]);
      expect(locations.filter((location) => location.availableQuantity !== null)).toEqual([]);
    });
  });

  test("a product at transfer centers has transfer locations in Berlin and Billund", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
    dataset,
  }) => {
    const transferCenterIds = [
      findFulfillmentCenter(dataset, IN_STOCK, 0),
      findFulfillmentCenter(dataset, IN_STOCK, 1),
    ];
    const arranged = await test.step("arrange: Berlin and Billund locations without a same-day center", () =>
      arrangePickupLocations(
        new PickupLocationsClient(platformAdminHttpClient),
        cleanupStack,
        frontendContext.storeId,
        ["Berlin", "Billund"].map((city) => ({
          city,
          fulfillmentCenterId: null,
          transferFulfillmentCenterIds: transferCenterIds,
        })),
      ));

    const locations = await test.step(`act: get pickup locations of ${STOCKED_PRODUCT_ID}`, () =>
      waitForArrangedLocations(graphqlClient, frontendContext, STOCKED_PRODUCT_ID, arranged));

    await test.step("assert: both cities are transfer locations", async () => {
      expect(availabilityByCity(locations)).toEqual({ Berlin: "Transfer", Billund: "Transfer" });
    });
  });

  test("a pickup location with several transfer centers reports their combined stock", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
    dataset,
  }) => {
    const transferCenterIds = [0, 1, 2].map((index) => findFulfillmentCenter(dataset, IN_STOCK, index));
    const arranged = await test.step(`arrange: location with transfer centers ${transferCenterIds.join(", ")}`, () =>
      arrangePickupLocations(
        new PickupLocationsClient(platformAdminHttpClient),
        cleanupStack,
        frontendContext.storeId,
        [
          {
            city: "Hubcity",
            fulfillmentCenterId: findFulfillmentCenter(dataset, OUT_OF_STOCK),
            transferFulfillmentCenterIds: transferCenterIds,
          },
        ],
      ));

    const locations = await test.step(`act: get pickup locations of ${STOCKED_PRODUCT_ID}`, () =>
      waitForArrangedLocations(graphqlClient, frontendContext, STOCKED_PRODUCT_ID, arranged));

    await test.step("assert: the transfer quantity is the sum over the transfer centers", async () => {
      const combinedStock = transferCenterIds
        .map((centerId) => getStockQuantity(dataset, STOCKED_PRODUCT_ID, centerId))
        .reduce((sum, quantity) => sum + quantity, 0);
      expect(quantityByCity(locations, "Transfer")).toEqual({ Hubcity: combinedStock });
    });
  });

  test("product pickup locations list same-day first and only global transfers lack a quantity", async ({
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
            city: "Sameday",
            fulfillmentCenterId: findFulfillmentCenter(dataset, IN_STOCK),
            transferFulfillmentCenterIds: [],
          },
          {
            city: "Transferville",
            fulfillmentCenterId: null,
            transferFulfillmentCenterIds: [findFulfillmentCenter(dataset, IN_STOCK, 1)],
          },
        ],
      ));
    await test.step("arrange: wait until the locations are searchable", () =>
      waitForArrangedLocations(graphqlClient, frontendContext, STOCKED_PRODUCT_ID, arranged));

    const locations = await test.step(`act: get every pickup location of ${STOCKED_PRODUCT_ID}`, () =>
      productPickupLocations(graphqlClient, frontendContext, STOCKED_PRODUCT_ID));

    await test.step("assert: same-day, transfer, then global transfer", async () => {
      expect(availabilityRanks(locations)).toEqual(availabilityRanks(locations).toSorted((a, b) => a - b));
    });
    await test.step("assert: same-day and transfer locations have a quantity, global transfers do not", async () => {
      for (const location of locations) {
        expect(location.availableQuantity === null, `${location.name} (${location.availabilityType})`).toBe(
          location.availabilityType === "GlobalTransfer",
        );
      }
    });
  });

  test("a product out of stock everywhere is only available via global transfer", async ({
    graphqlClient,
    frontendContext,
    dataset,
  }) => {
    await test.step(`arrange: ${OUT_OF_STOCK_PRODUCT_ID} has no stock in the dataset`, async () => {
      expect(getProductStock(dataset, OUT_OF_STOCK_PRODUCT_ID)).toEqual([]);
    });

    const locations = await test.step(`act: get pickup locations of ${OUT_OF_STOCK_PRODUCT_ID}`, () =>
      productPickupLocations(graphqlClient, frontendContext, OUT_OF_STOCK_PRODUCT_ID));

    await test.step("assert: every location is a global transfer without a quantity", async () => {
      expect(locations.length).toBeGreaterThan(0);
      expect(locations.filter((location) => location.availabilityType !== "GlobalTransfer")).toEqual([]);
      expect(locations.filter((location) => location.availableQuantity !== null)).toEqual([]);
    });
  });
});

async function productPickupLocations(
  graphqlClient: GraphqlClient,
  context: FrontendContext,
  productId: string,
): Promise<ProductPickupLocationFragment[]> {
  const { productPickupLocations: connection } = await graphqlClient.execute(ProductPickupLocationsDocument, {
    productId,
    storeId: context.storeId,
    cultureName: context.cultureName,
    first: ALL_LOCATIONS_PAGE_SIZE,
  });
  return (connection?.items ?? []).filter((location): location is ProductPickupLocationFragment => location !== null);
}

function newStorePickupLocation(context: FrontendContext, dataset: Dataset, city: string): PickupLocationDraft {
  return newPickupLocation(context.storeId, uniqueId("test-pickup"), {
    city,
    fulfillmentCenterId: findFulfillmentCenter(dataset, IN_STOCK),
    transferFulfillmentCenterIds: [],
  });
}

async function storePickupLocation(
  graphqlClient: GraphqlClient,
  context: FrontendContext,
  id: string,
): Promise<PickupLocationFragment | undefined> {
  const { pickupLocations } = await graphqlClient.execute(PickupLocationsDocument, {
    storeId: context.storeId,
    first: ALL_LOCATIONS_PAGE_SIZE,
  });
  return pickupLocations?.items?.find((location) => location?.id === id) ?? undefined;
}

async function waitForArrangedLocations(
  graphqlClient: GraphqlClient,
  context: FrontendContext,
  productId: string,
  arranged: ArrangedPickupLocations,
): Promise<ProductPickupLocationFragment[]> {
  let found: ProductPickupLocationFragment[] = [];
  await expect
    .poll(async () => {
      found = locationsArrangedIn(await productPickupLocations(graphqlClient, context, productId), arranged);
      return found.length;
    })
    .toBe(arranged.locations.length);
  return found;
}

function availabilityByCity(locations: readonly ProductPickupLocationFragment[]): Record<string, string | null> {
  return Object.fromEntries(locations.map((location) => [location.address?.city, location.availabilityType]));
}

function quantityByCity(
  locations: readonly ProductPickupLocationFragment[],
  availabilityType: ProductPickupLocationFragment["availabilityType"],
): Record<string, number | null> {
  return Object.fromEntries(
    locations
      .filter((location) => location.availabilityType === availabilityType)
      .map((location) => [location.address?.city, location.availableQuantity]),
  );
}

function availabilityRanks(locations: readonly ProductPickupLocationFragment[]): number[] {
  return locations.map((location) => AVAILABILITY_ORDER.indexOf(location.availabilityType));
}
