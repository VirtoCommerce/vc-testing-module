import type { DynamicPropertyData } from "@api/rest/types/platform";

import * as allure from "allure-js-commons";

import { DynamicPropertiesClient } from "@api/rest/clients/dynamic-properties-client";
import { uniqueId } from "@core/unique-id";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const CONTACT_TYPE = "VirtoCommerce.CustomerModule.Core.Model.Contact";
const OBJECT_TYPES = [
  "VirtoCommerce.CartModule.Core.Model.LineItem",
  "VirtoCommerce.CartModule.Core.Model.Payment",
  "VirtoCommerce.CartModule.Core.Model.Shipment",
  "VirtoCommerce.CartModule.Core.Model.ShoppingCart",
  "VirtoCommerce.ContentModule.Core.Model.FrontMatterHeaders",
  "VirtoCommerce.CustomerModule.Core.Model.Contact",
  "VirtoCommerce.CustomerModule.Core.Model.Employee",
  "VirtoCommerce.CustomerModule.Core.Model.Organization",
  "VirtoCommerce.CustomerModule.Core.Model.Vendor",
  "VirtoCommerce.MarketingModule.Core.Model.DynamicContentItem",
  "VirtoCommerce.OrdersModule.Core.Model.CustomerOrder",
  "VirtoCommerce.OrdersModule.Core.Model.LineItem",
  "VirtoCommerce.OrdersModule.Core.Model.PaymentIn",
  "VirtoCommerce.OrdersModule.Core.Model.Shipment",
  "VirtoCommerce.QuoteModule.Core.Model.QuoteRequest",
  "VirtoCommerce.StoreModule.Core.Model.Store",
] as const;
const VALUE_TYPE_CASES = [
  { valueType: "ShortText", isArray: false, isMultilingual: false },
  { valueType: "ShortText", isArray: true, isMultilingual: false },
  { valueType: "ShortText", isArray: false, isMultilingual: true },
  { valueType: "LongText", isArray: false, isMultilingual: false },
  { valueType: "Integer", isArray: false, isMultilingual: false },
  { valueType: "Decimal", isArray: false, isMultilingual: false },
  { valueType: "DateTime", isArray: false, isMultilingual: false },
  { valueType: "Boolean", isArray: false, isMultilingual: false },
  { valueType: "Html", isArray: false, isMultilingual: false },
] as const satisfies readonly DynamicPropertyData[];

test.beforeEach(async () => {
  await allure.feature("Platform / Dynamic Properties");
});

test.describe("dynamic properties (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("list object types that support dynamic properties", async ({ httpClient }) => {
    const dynamicPropertiesClient = new DynamicPropertiesClient(httpClient);

    const objectTypes = await test.step("act: list object types", () => dynamicPropertiesClient.listObjectTypes());

    await test.step("assert: store and contact support dynamic properties", async () => {
      expect(objectTypes).toEqual(expect.arrayContaining(["VirtoCommerce.StoreModule.Core.Model.Store", CONTACT_TYPE]));
    });
  });

  for (const objectType of OBJECT_TYPES) {
    const typeTitle = objectType.replace("VirtoCommerce.", "").replace(".Core.Model.", " ");

    test(`create and find a dynamic property of ${typeTitle}`, async ({ httpClient, cleanupStack }) => {
      const dynamicPropertiesClient = new DynamicPropertiesClient(httpClient);
      const name = uniqueId("test_property");

      const property = await test.step("act: create property", () =>
        dynamicPropertiesClient.create({ objectType, name, valueType: "ShortText" }));
      cleanupStack.push(`delete dynamic property ${property.id}`, () => dynamicPropertiesClient.delete([property.id]));

      await test.step("assert: property is found for the object type", async () => {
        const found = await dynamicPropertiesClient.search({ objectType, keyword: name, take: 10 });
        expect(found).toEqual([expect.objectContaining({ id: property.id, name, objectType })]);
      });
    });
  }

  test("create a dictionary dynamic property", async ({ httpClient, cleanupStack }) => {
    const dynamicPropertiesClient = new DynamicPropertiesClient(httpClient);

    const property = await test.step("act: create dictionary property", () =>
      dynamicPropertiesClient.create({
        objectType: CONTACT_TYPE,
        name: uniqueId("test_dictionary_property"),
        valueType: "ShortText",
        isDictionary: true,
      }));
    cleanupStack.push(`delete dynamic property ${property.id}`, () => dynamicPropertiesClient.delete([property.id]));

    await test.step("assert: property is a dictionary", async () => {
      expect(property.isDictionary).toBe(true);
    });
  });

  for (const { valueType, isArray, isMultilingual } of VALUE_TYPE_CASES) {
    const flags = [isArray ? "array" : "", isMultilingual ? "multilingual" : ""].filter(Boolean).join(", ");

    test(`create a ${valueType} dynamic property${flags ? ` (${flags})` : ""}`, async ({
      httpClient,
      cleanupStack,
    }) => {
      const dynamicPropertiesClient = new DynamicPropertiesClient(httpClient);

      const property = await test.step("act: create property", () =>
        dynamicPropertiesClient.create({
          objectType: CONTACT_TYPE,
          name: uniqueId(`test_${valueType}`),
          valueType,
          isArray,
          isMultilingual,
          isDictionary: false,
        }));
      cleanupStack.push(`delete dynamic property ${property.id}`, () => dynamicPropertiesClient.delete([property.id]));

      await test.step("assert: property keeps its value type and flags", async () => {
        expect(property).toMatchObject({ valueType, isArray, isMultilingual });
      });
    });
  }

  test("search dynamic properties of an object type", async ({ httpClient, cleanupStack }) => {
    const dynamicPropertiesClient = new DynamicPropertiesClient(httpClient);
    const property = await test.step("arrange: contact property", () =>
      dynamicPropertiesClient.create({
        objectType: CONTACT_TYPE,
        name: uniqueId("test_property"),
        valueType: "ShortText",
      }));
    cleanupStack.push(`delete dynamic property ${property.id}`, () => dynamicPropertiesClient.delete([property.id]));

    const found = await test.step("act: search contact properties", () =>
      dynamicPropertiesClient.search({ objectType: CONTACT_TYPE, take: 1000 }));

    await test.step("assert: only contact properties are found", async () => {
      expect(found.map(({ id }) => id)).toContain(property.id);
      expect(new Set(found.map(({ objectType }) => objectType))).toEqual(new Set([CONTACT_TYPE]));
    });
  });
});
