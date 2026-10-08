import * as allure from "allure-js-commons";

import { CustomersClient } from "@api/rest/clients/customers-client";
import { newMember } from "@dataset/builders/customer";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Contacts / Vendors");
});

test.describe("vendors (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("search vendors", async ({ httpClient, cleanupStack }) => {
    const customersClient = new CustomersClient(httpClient);
    const vendor = await test.step("arrange: vendor", () => customersClient.members.create(newMember("Vendor")));
    cleanupStack.push(`delete vendor ${vendor.id}`, () => customersClient.members.delete([vendor.id]));

    const found = await test.step("act: search vendors by id", () =>
      customersClient.searchVendors({ objectIds: [vendor.id] }));

    await test.step("assert: vendor is found", async () => {
      expect(found).toEqual([expect.objectContaining({ id: vendor.id, memberType: "Vendor" })]);
    });
  });
});
