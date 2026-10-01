import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { FrontendContext } from "@dataset/frontend-context";

import * as allure from "allure-js-commons";

import {
  ChangeCartConfiguredItemDocument,
  ProductConfigurationDocument,
  RemoveCartItemDocument,
} from "@api/graphql/generated/graphql";
import { requireFields } from "@core/required-fields";
import { arrangeCart, cartScope, lineItemFor } from "@dataset/arrange/cart";
import { LAST_OPTION, optionOfEachSection } from "@dataset/builders/product-configuration";
import { expect, test } from "@fixtures";

const CONFIGURABLE_PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai";
const CONFIGURED_SKU = `Configuration-${CONFIGURABLE_PRODUCT_ID}`;

test.beforeEach(async () => {
  await allure.feature("Cart / Configurable Product");
});

test.describe("configurable products in the cart (anonymous)", () => {
  test("add a configured product", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const selection = optionOfEachSection(await getConfiguration(graphqlClient, frontendContext));

    const cart = await test.step("act: add the product with the first option of each section", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: CONFIGURABLE_PRODUCT_ID, quantity: 1 }], {
        configurationSections: selection,
      }));

    await test.step("assert: a configured line item has the selected components", async () => {
      const lineItem = lineItemFor(cart, CONFIGURABLE_PRODUCT_ID);
      expect(cart.itemsCount).toBe(1);
      expect(lineItem.sku).toBe(CONFIGURED_SKU);
      expect(new Set(lineItem.configurationItems?.map((item) => item?.productId))).toEqual(
        selectedProductIds(selection),
      );
      for (const item of lineItem.configurationItems ?? []) {
        expect(item).toMatchObject({ sectionId: expect.any(String), name: expect.any(String) });
      }
    });
  });

  test("change the configuration of a line item", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const configuration = await getConfiguration(graphqlClient, frontendContext);
    const firstSelection = optionOfEachSection(configuration);
    const lastSelection = optionOfEachSection(configuration, LAST_OPTION);
    const cart = await test.step("arrange: cart with the first option of each section", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: CONFIGURABLE_PRODUCT_ID, quantity: 1 }], {
        configurationSections: firstSelection,
      }));
    const lineItem = lineItemFor(cart, CONFIGURABLE_PRODUCT_ID);

    const { changeCartConfiguredItem } = await test.step("act: switch to the last option of each section", () =>
      graphqlClient.execute(ChangeCartConfiguredItemDocument, {
        command: {
          ...cartScope(frontendContext),
          cartId: cart.id,
          lineItemId: lineItem.id,
          configurationSections: lastSelection,
        },
      }));

    await test.step("assert: the same line item has the new components", async () => {
      const changedItem = lineItemFor(changeCartConfiguredItem, CONFIGURABLE_PRODUCT_ID);
      const changedIds = new Set(changedItem.configurationItems?.map((item) => item?.productId));
      expect(changeCartConfiguredItem?.itemsCount).toBe(1);
      expect(changedItem.id).toBe(lineItem.id);
      expect(changedIds).toEqual(selectedProductIds(lastSelection));
      expect(changedIds).not.toEqual(selectedProductIds(firstSelection));
    });
  });

  test("remove a configured line item", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const selection = optionOfEachSection(await getConfiguration(graphqlClient, frontendContext));
    const cart = await test.step("arrange: cart with a configured product", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: CONFIGURABLE_PRODUCT_ID, quantity: 1 }], {
        configurationSections: selection,
      }));

    const { removeCartItem } = await test.step("act: remove the configured line item", () =>
      graphqlClient.execute(RemoveCartItemDocument, {
        command: {
          ...cartScope(frontendContext),
          cartId: cart.id,
          lineItemId: lineItemFor(cart, CONFIGURABLE_PRODUCT_ID).id,
        },
      }));

    await test.step("assert: cart is empty", async () => {
      expect(removeCartItem).toMatchObject({ itemsCount: 0, items: [] });
    });
  });
});

async function getConfiguration(graphqlClient: GraphqlClient, context: FrontendContext) {
  const { productConfiguration } = await test.step(`arrange: configuration of ${CONFIGURABLE_PRODUCT_ID}`, () =>
    graphqlClient.execute(ProductConfigurationDocument, {
      configurableProductId: CONFIGURABLE_PRODUCT_ID,
      ...cartScope(context),
    }));
  const configuration = requireFields(productConfiguration ?? undefined, ["configurationSections"], "Configuration");
  expect(configuration.configurationSections.length).toBeGreaterThan(0);
  return configuration;
}

function selectedProductIds(selection: ReturnType<typeof optionOfEachSection>): Set<string | undefined> {
  return new Set(selection.map(({ option }) => option?.productId));
}
