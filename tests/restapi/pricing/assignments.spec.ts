import * as allure from "allure-js-commons";

import { PricingClient } from "@api/rest/clients/pricing-client";
import { SEEDED_CATALOG_ID } from "@dataset/builders/catalog";
import { newPricelist, newPricelistAssignment } from "@dataset/builders/pricing";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Pricing / Assignments");
});

test.describe("pricelist assignments (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create an assignment", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));
    const draft = newPricelistAssignment(pricelist.id);

    const assignment = await test.step("act: create assignment", () => pricingClient.createAssignment(draft));
    cleanupStack.push(`delete assignment ${assignment.id}`, () => pricingClient.deleteAssignment(assignment.id));

    await test.step("assert: assignment links the pricelist to the seeded catalog", async () => {
      expect(assignment).toMatchObject({ name: draft.name, pricelistId: pricelist.id, catalogId: SEEDED_CATALOG_ID });
    });
  });

  test("rename an assignment", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));
    const assignment = await test.step("arrange: assignment", () =>
      pricingClient.createAssignment(newPricelistAssignment(pricelist.id)));
    cleanupStack.push(`delete assignment ${assignment.id}`, () => pricingClient.deleteAssignment(assignment.id));
    const newName = `${assignment.name}-renamed`;

    await test.step("act: rename assignment", () => pricingClient.updateAssignment({ ...assignment, name: newName }));

    await test.step("assert: assignment has the new name", async () => {
      expect((await pricingClient.getAssignment(assignment.id)).name).toBe(newName);
    });
  });

  test("describe an assignment", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));
    const assignment = await test.step("arrange: assignment", () =>
      pricingClient.createAssignment(newPricelistAssignment(pricelist.id)));
    cleanupStack.push(`delete assignment ${assignment.id}`, () => pricingClient.deleteAssignment(assignment.id));
    const description = `Description of ${assignment.name}`;

    await test.step("act: set assignment description", () =>
      pricingClient.updateAssignment({ ...assignment, description }));

    await test.step("assert: assignment has the description", async () => {
      expect((await pricingClient.getAssignment(assignment.id)).description).toBe(description);
    });
  });

  test("get a new assignment template", async ({ httpClient }) => {
    const pricingClient = new PricingClient(httpClient);

    const template = await test.step("act: get new assignment", () => pricingClient.getNewAssignment());

    await test.step("assert: template is unsaved and has a condition tree", async () => {
      expect(template.id ?? null).toBeNull();
      expect(template.dynamicExpression).toBeTruthy();
    });
  });

  test("get an assignment by id", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));
    const assignment = await test.step("arrange: assignment", () =>
      pricingClient.createAssignment(newPricelistAssignment(pricelist.id)));
    cleanupStack.push(`delete assignment ${assignment.id}`, () => pricingClient.deleteAssignment(assignment.id));

    const reloaded = await test.step("act: get assignment", () => pricingClient.getAssignment(assignment.id));

    await test.step("assert: fields match the created assignment", async () => {
      expect(reloaded).toMatchObject({ id: assignment.id, name: assignment.name });
    });
  });

  test("search assignments by pricelist", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));
    const assignment = await test.step("arrange: assignment", () =>
      pricingClient.createAssignment(newPricelistAssignment(pricelist.id)));
    cleanupStack.push(`delete assignment ${assignment.id}`, () => pricingClient.deleteAssignment(assignment.id));

    const found = await test.step("act: search by pricelist", () =>
      pricingClient.searchAssignments({ PriceListId: pricelist.id }));

    await test.step("assert: only the pricelist assignment is found", async () => {
      expect(found.map(({ id }) => id)).toEqual([assignment.id]);
    });
  });

  test("delete an assignment", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));
    const assignment = await test.step("arrange: assignment", () =>
      pricingClient.createAssignment(newPricelistAssignment(pricelist.id)));
    cleanupStack.push(`delete assignment ${assignment.id}`, () => pricingClient.deleteAssignment(assignment.id));

    await test.step("act: delete assignment", () => pricingClient.deleteAssignment(assignment.id));

    await test.step("assert: assignment is not found", async () => {
      expect(await pricingClient.findAssignment(assignment.id)).toBeUndefined();
    });
  });

  test("delete assignments matching a search phrase", async ({ httpClient, cleanupStack }) => {
    const pricingClient = new PricingClient(httpClient);
    const pricelist = await test.step("arrange: pricelist", () => pricingClient.createPricelist(newPricelist()));
    cleanupStack.push(`delete pricelist ${pricelist.id}`, () => pricingClient.deletePricelist(pricelist.id));
    const assignment = await test.step("arrange: assignment", () =>
      pricingClient.createAssignment(newPricelistAssignment(pricelist.id)));
    cleanupStack.push(`delete assignment ${assignment.id}`, () => pricingClient.deleteAssignment(assignment.id));

    await test.step("act: delete assignments matching the name", () =>
      pricingClient.deleteFilteredAssignments({ SearchPhrase: assignment.name, PriceListId: pricelist.id }));

    await test.step("assert: assignment is not found", async () => {
      expect(await pricingClient.findAssignment(assignment.id)).toBeUndefined();
    });
  });
});
