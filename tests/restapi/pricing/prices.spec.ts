import * as allure from "allure-js-commons";

import { PricingClient } from "@api/rest/clients/pricing-client";
import { SEEDED_CATALOG_ID } from "@dataset/builders/catalog";
import { newPrice, newPricelist } from "@dataset/builders/pricing";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const SEEDED_PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai";
const SECOND_SEEDED_PRODUCT_ID = "laptop-apple-macbook-air-15-midnight-16gb-1tb";

test.beforeEach(async () => {
  await allure.feature("Pricing / Prices");
});

test.describe("prices (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("add a price to a product", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));

    await test.step("act: add price", () =>
      pricingClient.savePrices([
        { productId: SEEDED_PRODUCT_ID, prices: [newPrice(pricelist.id, SEEDED_PRODUCT_ID, 49.99)] },
      ]));

    await test.step("assert: product has the price in the pricelist", async () => {
      expect(
        await pricingClient.searchPrices({ priceListIds: [pricelist.id], productIds: [SEEDED_PRODUCT_ID] }),
      ).toEqual([expect.objectContaining({ pricelistId: pricelist.id, productId: SEEDED_PRODUCT_ID, list: 49.99 })]);
    });
  });

  test("update a price through the product", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));
    await test.step("arrange: price", () =>
      pricingClient.savePrices([
        { productId: SEEDED_PRODUCT_ID, prices: [newPrice(pricelist.id, SEEDED_PRODUCT_ID, 10)] },
      ]));

    await test.step("act: update price through the product", () =>
      pricingClient.saveProductPrices({
        productId: SEEDED_PRODUCT_ID,
        prices: [newPrice(pricelist.id, SEEDED_PRODUCT_ID, 25)],
      }));

    await test.step("assert: pricelist has only the new price", async () => {
      expect(await pricingClient.searchPrices({ priceListIds: [pricelist.id] })).toEqual([
        expect.objectContaining({ productId: SEEDED_PRODUCT_ID, list: 25 }),
      ]);
    });
  });

  test("search prices by pricelist with GET", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));
    await test.step("arrange: price", () =>
      pricingClient.savePrices([
        { productId: SEEDED_PRODUCT_ID, prices: [newPrice(pricelist.id, SEEDED_PRODUCT_ID, 15)] },
      ]));

    const prices = await test.step("act: search prices", () => pricingClient.searchPricesByPricelist(pricelist.id));

    await test.step("assert: pricelist price is found", async () => {
      expect(prices).toEqual([expect.objectContaining({ productId: SEEDED_PRODUCT_ID, list: 15 })]);
    });
  });

  test("search prices by pricelist with POST", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));
    await test.step("arrange: price", () =>
      pricingClient.savePrices([
        { productId: SEEDED_PRODUCT_ID, prices: [newPrice(pricelist.id, SEEDED_PRODUCT_ID, 16)] },
      ]));

    const prices = await test.step("act: search prices", () =>
      pricingClient.searchPrices({ priceListIds: [pricelist.id] }));

    await test.step("assert: pricelist price is found", async () => {
      expect(prices).toEqual([expect.objectContaining({ productId: SEEDED_PRODUCT_ID, list: 16 })]);
    });
  });

  test("delete a price by id", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));
    await test.step("arrange: price", () =>
      pricingClient.savePrices([
        { productId: SEEDED_PRODUCT_ID, prices: [newPrice(pricelist.id, SEEDED_PRODUCT_ID, 5)] },
      ]));
    const prices = await test.step("arrange: located price", () =>
      pricingClient.searchPrices({ priceListIds: [pricelist.id] }));

    await test.step("act: delete price by id", () => pricingClient.deletePrices(prices.map(({ id }) => id)));

    await test.step("assert: pricelist has no prices", async () => {
      expect(await pricingClient.searchPrices({ priceListIds: [pricelist.id] })).toEqual([]);
    });
  });

  test("delete prices by pricelist and product", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));
    await test.step("arrange: price", () =>
      pricingClient.savePrices([
        { productId: SEEDED_PRODUCT_ID, prices: [newPrice(pricelist.id, SEEDED_PRODUCT_ID, 7.5)] },
      ]));

    await test.step("act: delete product prices", () =>
      pricingClient.deleteProductPrices(pricelist.id, [SEEDED_PRODUCT_ID]));

    await test.step("assert: pricelist has no prices", async () => {
      expect(await pricingClient.searchPrices({ priceListIds: [pricelist.id] })).toEqual([]);
    });
  });

  test("add and delete prices in bulk", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));
    const productIds = [SEEDED_PRODUCT_ID, SECOND_SEEDED_PRODUCT_ID];

    await test.step("act: add prices for two products", () =>
      pricingClient.savePrices(
        productIds.map((productId, index) => ({ productId, prices: [newPrice(pricelist.id, productId, index + 1)] })),
      ));
    await test.step("assert: both products are priced", async () => {
      const prices = await pricingClient.searchPrices({ priceListIds: [pricelist.id] });
      expect(prices.map(({ productId }) => productId).sort()).toEqual([...productIds].sort());
    });

    await test.step("act: delete prices for both products", () =>
      pricingClient.deleteProductPrices(pricelist.id, productIds));
    await test.step("assert: pricelist has no prices", async () => {
      expect(await pricingClient.searchPrices({ priceListIds: [pricelist.id] })).toEqual([]);
    });
  });

  test("get the prices widget of a product", async ({ httpClient }) => {
    const pricingClient = new PricingClient(httpClient);

    const prices = await test.step("act: get prices widget", () =>
      pricingClient.getPricesWidget(SEEDED_PRODUCT_ID, SEEDED_CATALOG_ID));

    await test.step("assert: widget lists the seeded product prices", async () => {
      expect(prices.length).toBeGreaterThan(0);
      expect(prices.map(({ productId }) => productId)).toEqual(prices.map(() => SEEDED_PRODUCT_ID));
    });
  });
});
