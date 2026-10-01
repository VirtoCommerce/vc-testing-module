import type { CatalogProduct, Category } from "@api/rest/types/catalog";
import type { TaggedEntity } from "@api/rest/types/personalization";
import type { CleanupStack } from "@core/cleanup-stack";

import * as allure from "allure-js-commons";

import { CatalogClient } from "@api/rest/clients/catalog-client";
import { PersonalizationClient } from "@api/rest/clients/personalization-client";
import { SettingsClient } from "@api/rest/clients/settings-client";
import { uniqueId } from "@core/unique-id";
import { newCatalog, newCategory, newProduct } from "@dataset/builders/catalog";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const MEMBER_GROUPS_SETTING = "Customer.MemberGroups";
const INHERITANCE_POLICY_SETTING = "CatalogPersonalization.TagsInheritancePolicy";

test.beforeEach(async () => {
  await allure.feature("Catalog / Personalization");
});

test.describe("catalog personalization (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test.describe("tags", () => {
    test("get member groups", async ({ httpClient }) => {
      const settingsClient = new SettingsClient(httpClient);

      const groups = await test.step("act: get member groups", () => settingsClient.getValues(MEMBER_GROUPS_SETTING));

      await test.step("assert: member groups are a list of names", async () => {
        expect(Array.isArray(groups)).toBe(true);
        for (const group of groups) {
          expect(group).toEqual(expect.any(String));
        }
      });
    });

    test("add a tag to the member groups", async ({ httpClient, cleanupStack }) => {
      const settingsClient = new SettingsClient(httpClient);
      const original = await test.step("arrange: current member groups", () =>
        settingsClient.get(MEMBER_GROUPS_SETTING));
      cleanupStack.push(`restore setting ${MEMBER_GROUPS_SETTING}`, () => settingsClient.save([original]));
      const tag = uniqueId("test-tag");

      await test.step("act: add tag", () =>
        settingsClient.save([{ ...original, allowedValues: [...(original.allowedValues ?? []), tag] }]));

      await test.step("assert: tag is a member group", async () => {
        expect(await settingsClient.getValues(MEMBER_GROUPS_SETTING)).toContain(tag);
      });
    });

    test("assign a tag to a product", async ({ httpClient, cleanupStack }) => {
      const catalogClient = new CatalogClient(httpClient);
      const personalizationClient = new PersonalizationClient(httpClient);
      const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
      cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
      const { product } = await test.step("arrange: product", () =>
        createCategoryWithProduct(catalogClient, catalog.id));
      const tag = uniqueId("test-tag");

      await test.step("act: tag product", () => personalizationClient.setTags(productEntity(product), [tag]));

      await test.step("assert: product has the tag", async () => {
        expect((await personalizationClient.getTaggedItem(product.id)).tags).toEqual([tag]);
      });
    });

    test("assign a tag to a category", async ({ httpClient, cleanupStack }) => {
      const catalogClient = new CatalogClient(httpClient);
      const personalizationClient = new PersonalizationClient(httpClient);
      const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
      cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
      const category = await test.step("arrange: category", () => catalogClient.saveCategory(newCategory(catalog.id)));
      const tag = uniqueId("test-tag");

      await test.step("act: tag category", () => personalizationClient.setTags(categoryEntity(category), [tag]));

      await test.step("assert: category has the tag", async () => {
        expect((await personalizationClient.getTaggedItem(category.id)).tags).toEqual([tag]);
      });
    });

    test("unassign a tag from a product", async ({ httpClient, cleanupStack }) => {
      const catalogClient = new CatalogClient(httpClient);
      const personalizationClient = new PersonalizationClient(httpClient);
      const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
      cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
      const { product } = await test.step("arrange: product", () =>
        createCategoryWithProduct(catalogClient, catalog.id));
      await test.step("arrange: tagged product", () =>
        personalizationClient.setTags(productEntity(product), [uniqueId("test-tag")]));

      await test.step("act: clear tags", () => personalizationClient.setTags(productEntity(product), []));

      await test.step("assert: product has no tags", async () => {
        expect((await personalizationClient.getTaggedItem(product.id)).tags).toEqual([]);
      });
    });

    test("search tagged items by entity id", async ({ httpClient, cleanupStack }) => {
      const catalogClient = new CatalogClient(httpClient);
      const personalizationClient = new PersonalizationClient(httpClient);
      const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
      cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
      const { product } = await test.step("arrange: product", () =>
        createCategoryWithProduct(catalogClient, catalog.id));
      const tag = uniqueId("test-tag");
      await test.step("arrange: tagged product", () => personalizationClient.setTags(productEntity(product), [tag]));

      const found = await test.step("act: search by product id", () =>
        personalizationClient.search({ entityIds: [product.id] }));

      await test.step("assert: product's tagged item is found", async () => {
        expect(found).toEqual([expect.objectContaining({ entityId: product.id, tags: [tag] })]);
      });
    });

    test("count product tags", async ({ httpClient, cleanupStack }) => {
      const catalogClient = new CatalogClient(httpClient);
      const personalizationClient = new PersonalizationClient(httpClient);
      const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
      cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
      const { product } = await test.step("arrange: product", () =>
        createCategoryWithProduct(catalogClient, catalog.id));
      const tags = [uniqueId("test-tag"), uniqueId("test-tag")];
      await test.step("arrange: tagged product", () => personalizationClient.setTags(productEntity(product), tags));

      const count = await test.step("act: count tags", () => personalizationClient.countTags(product.id));

      await test.step("assert: count matches the assigned tags", async () => {
        expect(count).toBe(tags.length);
      });
    });
  });

  test.describe("tag inheritance", () => {
    test.describe.configure({ mode: "default" });

    test("category tag is inherited down the tree", async ({ httpClient, cleanupStack }) => {
      const catalogClient = new CatalogClient(httpClient);
      const personalizationClient = new PersonalizationClient(httpClient);
      const settingsClient = new SettingsClient(httpClient);
      await test.step("arrange: DownTree inheritance policy", () =>
        arrangeInheritancePolicy(settingsClient, cleanupStack, "DownTree"));
      const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
      cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
      const { category, product } = await test.step("arrange: product in a category", () =>
        createCategoryWithProduct(catalogClient, catalog.id));
      const tag = uniqueId("test-tag");

      await test.step("act: tag category", () => personalizationClient.setTags(categoryEntity(category), [tag]));

      await test.step("assert: product inherits the tag", async () => {
        expect((await personalizationClient.getTaggedItem(product.id)).inheritedTags).toContain(tag);
      });
    });

    test("product tag is inherited up the tree", async ({ httpClient, cleanupStack }) => {
      const catalogClient = new CatalogClient(httpClient);
      const personalizationClient = new PersonalizationClient(httpClient);
      const settingsClient = new SettingsClient(httpClient);
      await test.step("arrange: UpTree inheritance policy", () =>
        arrangeInheritancePolicy(settingsClient, cleanupStack, "UpTree"));
      const catalog = await test.step("arrange: catalog", () => catalogClient.saveCatalog(newCatalog()));
      cleanupStack.push(`delete catalog ${catalog.id}`, () => catalogClient.deleteCatalog(catalog.id));
      const { category, product } = await test.step("arrange: product in a category", () =>
        createCategoryWithProduct(catalogClient, catalog.id));
      const tag = uniqueId("test-tag");

      await test.step("act: tag product", () => personalizationClient.setTags(productEntity(product), [tag]));

      await test.step("assert: category inherits the tag", async () => {
        expect((await personalizationClient.getTaggedItem(category.id)).inheritedTags).toContain(tag);
      });
    });

    test("synchronize outlines", async ({ httpClient, cleanupStack }) => {
      const personalizationClient = new PersonalizationClient(httpClient);
      const settingsClient = new SettingsClient(httpClient);
      await test.step("arrange: UpTree inheritance policy", () =>
        arrangeInheritancePolicy(settingsClient, cleanupStack, "UpTree"));

      const notification = await test.step("act: start outlines synchronization", () =>
        personalizationClient.synchronizeOutlines());

      await test.step("assert: synchronization job is started", async () => {
        expect(notification).toMatchObject({ errorCount: 0, jobId: expect.any(String) });
      });
    });
  });
});

async function createCategoryWithProduct(
  catalogClient: CatalogClient,
  catalogId: string,
): Promise<{ category: Category; product: CatalogProduct }> {
  const category = await catalogClient.saveCategory(newCategory(catalogId));
  const product = await catalogClient.saveProduct(newProduct(catalogId, category.id));
  return { category, product };
}

async function arrangeInheritancePolicy(
  settingsClient: SettingsClient,
  cleanupStack: CleanupStack,
  policy: string,
): Promise<void> {
  const original = await settingsClient.get(INHERITANCE_POLICY_SETTING);
  cleanupStack.push(`restore setting ${INHERITANCE_POLICY_SETTING}`, () => settingsClient.save([original]));
  await settingsClient.save([{ ...original, value: policy }]);
}

function productEntity(product: CatalogProduct): TaggedEntity {
  return { entityId: product.id, entityType: "Product", label: product.name };
}

function categoryEntity(category: Category): TaggedEntity {
  return { entityId: category.id, entityType: "Category", label: category.name };
}
