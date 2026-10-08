import type {
  DynamicContentResource,
  SearchableDynamicContentResource,
} from "@api/rest/clients/dynamic-content-client";
import type { NamedEntityData } from "@api/rest/types/marketing";

import * as allure from "allure-js-commons";

import { DynamicContentClient } from "@api/rest/clients/dynamic-content-client";
import { uniqueId } from "@core/unique-id";
import { ageConditionTree, newInactivePublication } from "@dataset/builders/marketing";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const READ_AFTER_WRITE_TIMEOUT_MS = 5_000;

interface ContentResourceCase {
  readonly title: string;
  readonly prefix: string;
  readonly select: (client: DynamicContentClient) => DynamicContentResource<NamedEntityData>;
  readonly selectSearchable?: (
    client: DynamicContentClient,
  ) => SearchableDynamicContentResource<NamedEntityData, { keyword?: string | null }>;
}

const CONTENT_RESOURCES: readonly ContentResourceCase[] = [
  { title: "content folder", prefix: "test-content-folder", select: (client) => client.folders },
  {
    title: "content item",
    prefix: "test-content-item",
    select: (client) => client.items,
    selectSearchable: (client) => client.items,
  },
  {
    title: "content place",
    prefix: "test-content-place",
    select: (client) => client.places,
    selectSearchable: (client) => client.places,
  },
  {
    title: "content publication",
    prefix: "test-content-publication",
    select: (client) => client.publications,
    selectSearchable: (client) => client.publications,
  },
];

test.beforeEach(async () => {
  await allure.feature("Marketing / Dynamic Content");
});

test.describe("dynamic content (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  for (const { title, prefix, select, selectSearchable } of CONTENT_RESOURCES) {
    test(`create a ${title}`, async ({ httpClient, cleanupStack }) => {
      const resource = select(new DynamicContentClient(httpClient));
      const name = uniqueId(prefix);

      const entity = await test.step(`act: create ${title}`, () => resource.create({ name }));
      cleanupStack.push(`delete ${title} ${entity.id}`, () => resource.delete([entity.id]));

      await test.step(`assert: ${title} has the name`, async () => {
        expect(entity.name).toBe(name);
      });
    });

    test(`get a ${title} by id`, async ({ httpClient, cleanupStack }) => {
      const resource = select(new DynamicContentClient(httpClient));
      const entity = await test.step(`arrange: ${title}`, () => resource.create({ name: uniqueId(prefix) }));
      cleanupStack.push(`delete ${title} ${entity.id}`, () => resource.delete([entity.id]));

      const reloaded = await test.step(`act: get ${title}`, () => resource.get(entity.id));

      await test.step(`assert: fields match the created ${title}`, async () => {
        expect(reloaded).toMatchObject({ id: entity.id, name: entity.name });
      });
    });

    test(`rename a ${title}`, async ({ httpClient, cleanupStack }) => {
      const resource = select(new DynamicContentClient(httpClient));
      const entity = await test.step(`arrange: ${title}`, () => resource.create({ name: uniqueId(prefix) }));
      cleanupStack.push(`delete ${title} ${entity.id}`, () => resource.delete([entity.id]));
      const newName = `${entity.name}-renamed`;

      await test.step(`act: rename ${title}`, () => resource.update({ ...entity, name: newName }));

      await test.step(`assert: ${title} has the new name`, async () => {
        await expect
          .poll(async () => (await resource.get(entity.id)).name, { timeout: READ_AFTER_WRITE_TIMEOUT_MS })
          .toBe(newName);
      });
    });

    test(`delete a ${title}`, async ({ httpClient, cleanupStack }) => {
      const resource = select(new DynamicContentClient(httpClient));
      const entity = await test.step(`arrange: ${title}`, () => resource.create({ name: uniqueId(prefix) }));
      cleanupStack.push(`delete ${title} ${entity.id}`, () => resource.delete([entity.id]));

      await test.step(`act: delete ${title}`, () => resource.delete([entity.id]));

      await test.step(`assert: ${title} is not found`, async () => {
        expect(await resource.find(entity.id)).toBeUndefined();
      });
    });

    if (selectSearchable !== undefined) {
      test(`search ${title}s by keyword`, async ({ httpClient, cleanupStack }) => {
        const resource = selectSearchable(new DynamicContentClient(httpClient));
        const entity = await test.step(`arrange: ${title}`, () => resource.create({ name: uniqueId(prefix) }));
        cleanupStack.push(`delete ${title} ${entity.id}`, () => resource.delete([entity.id]));

        const found = await test.step(`act: search by ${title} name`, () => resource.search({ keyword: entity.name }));

        await test.step(`assert: ${title} is in the results`, async () => {
          expect(found.map(({ id }) => id)).toContain(entity.id);
        });
      });

      test(`delete ${title}s in bulk`, async ({ httpClient, cleanupStack }) => {
        const resource = selectSearchable(new DynamicContentClient(httpClient));
        const entities = await test.step(`arrange: two ${title}s`, () =>
          Promise.all([resource.create({ name: uniqueId(prefix) }), resource.create({ name: uniqueId(prefix) })]));
        const ids = entities.map(({ id }) => id);
        cleanupStack.push(`delete ${title}s ${ids.join(", ")}`, () => resource.delete(ids));

        await test.step(`act: delete both ${title}s`, () => resource.delete(ids));

        await test.step(`assert: neither ${title} is found`, async () => {
          expect(await Promise.all(ids.map((id) => resource.find(id)))).toEqual([undefined, undefined]);
        });
      });
    }
  }

  test("get a new content publication template", async ({ httpClient }) => {
    const dynamicContentClient = new DynamicContentClient(httpClient);

    const template = await test.step("act: get new publication", () => dynamicContentClient.newPublication());

    await test.step("assert: template is unsaved and has a condition tree", async () => {
      expect(template.id ?? null).toBeNull();
      expect(template.dynamicExpression).toMatchObject({ id: "DynamicContentConditionTree" });
    });
  });

  test("add and update a content publication condition", async ({ httpClient, cleanupStack }) => {
    const { publications } = new DynamicContentClient(httpClient);
    const publication = await test.step("arrange: inactive publication", () =>
      publications.create(newInactivePublication()));
    cleanupStack.push(`delete content publication ${publication.id}`, () => publications.delete([publication.id]));

    await test.step("act: add an age condition of 21", () =>
      publications.update({ ...publication, dynamicExpression: ageConditionTree(21) }));
    await test.step("assert: condition is saved", async () => {
      expect((await publications.get(publication.id)).dynamicExpression).toMatchObject({
        children: [{ id: "BlockContentCondition", children: [{ id: "ConditionAgeIs", value: 21 }] }],
      });
    });

    const withCondition = await publications.get(publication.id);
    await test.step("act: change the age condition to 31", () =>
      publications.update({ ...withCondition, dynamicExpression: ageConditionTree(31) }));
    await test.step("assert: condition value is updated", async () => {
      expect((await publications.get(publication.id)).dynamicExpression).toMatchObject({
        children: [{ children: [{ id: "ConditionAgeIs", value: 31 }] }],
      });
    });
  });
});
