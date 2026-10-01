import * as allure from "allure-js-commons";

import { CreateConfiguredLineItemDocument, ProductConfigurationDocument } from "@api/graphql/generated/graphql";
import { requireFields } from "@core/required-fields";
import { cartScope } from "@dataset/arrange/cart";
import { optionOfEachSection } from "@dataset/builders/product-configuration";
import { expect, test } from "@fixtures";

const CONFIGURABLE_PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai";

test.beforeEach(async () => {
  await allure.feature("Catalog / Configurable Product");
});

test.describe("configurable product (anonymous)", () => {
  test("configure a product into a line item", async ({ graphqlClient, frontendContext }) => {
    const { productConfiguration } = await test.step("arrange: product configuration", () =>
      graphqlClient.execute(ProductConfigurationDocument, {
        configurableProductId: CONFIGURABLE_PRODUCT_ID,
        ...cartScope(frontendContext),
      }));
    const configuration = requireFields(productConfiguration ?? undefined, ["configurationSections"], "Configuration");
    await test.step("assert: every section offers options", async () => {
      expect(configuration.configurationSections.length).toBeGreaterThan(0);
      for (const section of configuration.configurationSections) {
        expect(section?.options?.length).toBeGreaterThan(0);
      }
    });

    const { createConfiguredLineItem } = await test.step("act: configure the first option of each section", () =>
      graphqlClient.execute(CreateConfiguredLineItemDocument, {
        command: {
          configurableProductId: CONFIGURABLE_PRODUCT_ID,
          configurationSections: optionOfEachSection(configuration),
          storeId: frontendContext.storeId,
          cultureName: frontendContext.cultureName,
          currencyCode: frontendContext.currencyCode,
        },
      }));

    await test.step("assert: one configured item of the product is created", async () => {
      expect(createConfiguredLineItem).toMatchObject({ quantity: 1, product: { id: CONFIGURABLE_PRODUCT_ID } });
    });
  });
});
