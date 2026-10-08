import * as allure from "allure-js-commons";

import { CurrenciesClient } from "@api/rest/clients/currencies-client";
import { uniqueId } from "@core/unique-id";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Core / Currencies");
});

test.describe("currencies (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create a currency", async ({ httpClient, cleanupStack }) => {
    const currenciesClient = new CurrenciesClient(httpClient);
    const code = uniqueId("QA");
    cleanupStack.push(`delete currency ${code}`, () => currenciesClient.delete(code));

    await test.step("act: create currency", () => currenciesClient.create({ code, name: `Test currency ${code}` }));

    await test.step("assert: currency is listed", async () => {
      expect(await currenciesClient.find(code)).toMatchObject({ code, name: `Test currency ${code}` });
    });
  });

  test("rename a currency", async ({ httpClient, cleanupStack }) => {
    const currenciesClient = new CurrenciesClient(httpClient);
    const code = uniqueId("QA");
    cleanupStack.push(`delete currency ${code}`, () => currenciesClient.delete(code));
    await test.step("arrange: currency", () => currenciesClient.create({ code, name: `Test currency ${code}` }));
    const newName = `Test currency ${code} renamed`;

    await test.step("act: rename currency", () => currenciesClient.update({ code, name: newName }));

    await test.step("assert: currency has the new name", async () => {
      expect((await currenciesClient.find(code))?.name).toBe(newName);
    });
  });

  test("delete a currency", async ({ httpClient, cleanupStack }) => {
    const currenciesClient = new CurrenciesClient(httpClient);
    const code = uniqueId("QA");
    cleanupStack.push(`delete currency ${code}`, () => currenciesClient.delete(code));
    await test.step("arrange: currency", () => currenciesClient.create({ code, name: `Test currency ${code}` }));

    await test.step("act: delete currency", () => currenciesClient.delete(code));

    await test.step("assert: currency is not listed", async () => {
      expect(await currenciesClient.find(code)).toBeUndefined();
    });
  });
});
