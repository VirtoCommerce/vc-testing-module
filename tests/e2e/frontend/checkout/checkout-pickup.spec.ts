import type { HttpClient } from "@api/http/http-client";
import type { CleanupStack } from "@core/cleanup-stack";
import type { ArrangedCart } from "@dataset/arrange/cart";
import type { ArrangedPickupLocations } from "@dataset/arrange/pickup-location";
import type { Dataset } from "@dataset/dataset";
import type { Shopper } from "@fixtures";
import type { PickupLocationCardFilter } from "@pages/frontend/components/pickup-locations-modal";

import * as allure from "allure-js-commons";

import { CartPickupLocationsDocument } from "@api/graphql/generated/graphql";
import { PickupLocationsClient } from "@api/rest/clients/pickup-locations-client";
import { requireFields } from "@core/required-fields";
import { arrangePickupLocations, locationsArrangedIn } from "@dataset/arrange/pickup-location";
import { findFulfillmentCenter } from "@dataset/stock";
import { expect, test, withItems } from "@fixtures";
import { CheckoutFlow } from "@pages/frontend/checkout-flow";
import { PickupLocationsModal } from "@pages/frontend/components/pickup-locations-modal";

import { PRODUCT_ID, QUANTITY } from "./checkout-support";

const LOCATION = {
  countryName: "United States of America",
  regionId: "DC",
  regionName: "District of Columbia",
  city: "Washington",
} as const;
const NO_MATCH_KEYWORD = "NonExistentLocation12345";
const FILTERS: readonly { readonly title: string; readonly card: PickupLocationCardFilter }[] = [
  { title: "country", card: { country: LOCATION.countryName } },
  { title: "country and region", card: { country: LOCATION.countryName, region: LOCATION.regionId } },
  {
    title: "country, region and city",
    card: { country: LOCATION.countryName, region: LOCATION.regionId, city: LOCATION.city },
  },
];

test.beforeEach(async () => {
  await allure.feature("Checkout / Pickup locations (E2E)");
});

test.describe("checkout pickup locations (anonymous)", () => {
  test.use({ cart: withItems([{ productId: PRODUCT_ID, quantity: QUANTITY }]) });

  for (const { title, card } of FILTERS) {
    test(`filter pickup locations by ${title}`, async ({
      page,
      env,
      shopper,
      cart,
      platformAdminHttpClient,
      cleanupStack,
      dataset,
    }) => {
      const arranged = await arrangeWashingtonLocation(platformAdminHttpClient, cleanupStack, shopper, cart, dataset);
      const modal = await openPickupLocations(new CheckoutFlow(page, env.checkoutMode), new PickupLocationsModal(page));

      await test.step(`act: filter by ${title}`, async () => {
        await modal.filters.apply(modal.filters.country, LOCATION.countryName);
        if (card.region !== undefined) {
          await modal.filters.apply(modal.filters.region, LOCATION.regionName);
        }
        if (card.city !== undefined) {
          await modal.filters.apply(modal.filters.city, LOCATION.city);
        }
      });

      await test.step(`assert: the arranged ${LOCATION.city} location matches the filter`, async () => {
        await expect(modal.cardsWhere({ ...card, name: arrangedName(arranged) })).toHaveCount(1);
      });
    });
  }

  test("search pickup locations by keyword", async ({
    page,
    env,
    shopper,
    cart,
    platformAdminHttpClient,
    cleanupStack,
    dataset,
  }) => {
    const arranged = await arrangeWashingtonLocation(platformAdminHttpClient, cleanupStack, shopper, cart, dataset);
    const modal = await openPickupLocations(new CheckoutFlow(page, env.checkoutMode), new PickupLocationsModal(page));

    await test.step(`act: search for "${arranged.namePrefix}"`, () => modal.filters.search(arranged.namePrefix));

    await test.step("assert: only the arranged location is listed", async () => {
      await expect(modal.cards).toHaveCount(1);
      await expect(modal.cardsWhere({ name: arrangedName(arranged), city: LOCATION.city })).toHaveCount(1);
    });
  });

  test("a keyword without matches lists no pickup locations", async ({ page, env }) => {
    const modal = await openPickupLocations(new CheckoutFlow(page, env.checkoutMode), new PickupLocationsModal(page));

    await test.step(`act: search for "${NO_MATCH_KEYWORD}"`, () => modal.filters.search(NO_MATCH_KEYWORD));

    await test.step("assert: no pickup location is listed", async () => {
      await expect(modal.cards).toHaveCount(0);
    });
  });
});

async function arrangeWashingtonLocation(
  platformAdminHttpClient: HttpClient,
  cleanupStack: CleanupStack,
  shopper: Shopper,
  cart: ArrangedCart | undefined,
  dataset: Dataset,
): Promise<ArrangedPickupLocations> {
  const { id: cartId } = requireFields(cart, ["id"], "Prefilled cart");
  const arranged = await test.step(`arrange: pickup location in ${LOCATION.city}, ${LOCATION.regionId}`, () =>
    arrangePickupLocations(new PickupLocationsClient(platformAdminHttpClient), cleanupStack, shopper.context.storeId, [
      {
        city: LOCATION.city,
        fulfillmentCenterId: findFulfillmentCenter(dataset, { stocks: [PRODUCT_ID] }),
        transferFulfillmentCenterIds: [],
        address: { countryName: LOCATION.countryName, regionId: LOCATION.regionId, regionName: LOCATION.regionName },
      },
    ]));
  await test.step("arrange: wait until the cart can be picked up there", async () => {
    await expect
      .poll(async () => {
        const { cartPickupLocations } = await shopper.graphqlClient.execute(CartPickupLocationsDocument, {
          cartId,
          storeId: shopper.context.storeId,
          cultureName: shopper.context.cultureName,
          first: 100,
        });
        return locationsArrangedIn(cartPickupLocations?.items ?? [], arranged).length;
      })
      .toBe(1);
  });
  return arranged;
}

async function openPickupLocations(flow: CheckoutFlow, modal: PickupLocationsModal): Promise<PickupLocationsModal> {
  await test.step(`arrange: open the pickup locations on the ${flow.mode} checkout`, async () => {
    await flow.start();
    await flow.shippingDetails.pickupSwitcher.click();
    await flow.shippingDetails.pickupLocationButton.click();
    await expect(modal.root).toBeVisible();
  });
  return modal;
}

function arrangedName(arranged: ArrangedPickupLocations): string {
  return `${arranged.namePrefix} ${LOCATION.city}`;
}
