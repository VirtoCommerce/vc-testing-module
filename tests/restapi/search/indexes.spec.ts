import * as allure from "allure-js-commons";

import { JobsClient } from "@api/rest/clients/jobs-client";
import { SearchIndexesClient } from "@api/rest/clients/search-indexes-client";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const PRODUCT_DOCUMENT_TYPE = "Product";
const INDEXED_PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai";
const SINGLE_DOCUMENT_TIMEOUT_MS = 30_000;
const FULL_REBUILD_TIMEOUT_MS = 300_000;

test.beforeEach(async () => {
  await allure.feature("Search / Indexes");
});

test.describe("search indexes (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("list indexes", async ({ httpClient }) => {
    const searchIndexesClient = new SearchIndexesClient(httpClient);

    const indexes = await test.step("act: get indexes", () => searchIndexesClient.list());

    await test.step("assert: product index is listed", async () => {
      expect(indexes.map(({ documentType }) => documentType)).toContain(PRODUCT_DOCUMENT_TYPE);
    });
  });

  test("get an indexed product document", async ({ httpClient }) => {
    const searchIndexesClient = new SearchIndexesClient(httpClient);

    const documents = await test.step("act: get product document", () =>
      searchIndexesClient.getDocuments(PRODUCT_DOCUMENT_TYPE, INDEXED_PRODUCT_ID));

    await test.step("assert: document is found", async () => {
      expect(documents).toHaveLength(1);
    });
  });

  test("reindex a product", async ({ httpClient }) => {
    const searchIndexesClient = new SearchIndexesClient(httpClient);
    const jobsClient = new JobsClient(httpClient);

    const notification = await test.step("act: start product indexation", () =>
      searchIndexesClient.startIndexation([
        { documentType: PRODUCT_DOCUMENT_TYPE, documentIds: [INDEXED_PRODUCT_ID] },
      ]));

    await test.step("assert: indexation job succeeds", () =>
      expectJobSucceeded(jobsClient, notification.jobId, SINGLE_DOCUMENT_TIMEOUT_MS));

    await test.step("assert: product is still indexed", async () => {
      expect(await searchIndexesClient.getDocuments(PRODUCT_DOCUMENT_TYPE, INDEXED_PRODUCT_ID)).toHaveLength(1);
    });
  });

  test("cancel an indexation", async ({ httpClient }) => {
    const searchIndexesClient = new SearchIndexesClient(httpClient);
    const jobsClient = new JobsClient(httpClient);
    const notification = await test.step("arrange: started product indexation", () =>
      searchIndexesClient.startIndexation([
        { documentType: PRODUCT_DOCUMENT_TYPE, documentIds: [INDEXED_PRODUCT_ID] },
      ]));

    await test.step("act: cancel indexation", () => searchIndexesClient.cancelIndexation(notification.jobId));

    await test.step("assert: indexation job is finished", async () => {
      await expect
        .poll(async () => (await jobsClient.get(notification.jobId)).completed, { timeout: SINGLE_DOCUMENT_TIMEOUT_MS })
        .toBe(true);
    });
  });

  test("drop and rebuild the product index", { tag: "@destructive" }, async ({ httpClient }) => {
    test.setTimeout(FULL_REBUILD_TIMEOUT_MS + 30_000);
    const searchIndexesClient = new SearchIndexesClient(httpClient);
    const jobsClient = new JobsClient(httpClient);

    const notification = await test.step("act: rebuild product index from scratch", () =>
      searchIndexesClient.startIndexation([{ documentType: PRODUCT_DOCUMENT_TYPE, deleteExistingIndex: true }]));

    await test.step("assert: rebuild job succeeds", () =>
      expectJobSucceeded(jobsClient, notification.jobId, FULL_REBUILD_TIMEOUT_MS));

    await test.step("assert: products are indexed again", async () => {
      expect(await searchIndexesClient.getDocuments(PRODUCT_DOCUMENT_TYPE, INDEXED_PRODUCT_ID)).toHaveLength(1);
    });
  });
});

async function expectJobSucceeded(jobsClient: JobsClient, jobId: string, timeout: number): Promise<void> {
  await expect.poll(async () => (await jobsClient.get(jobId)).completed, { timeout }).toBe(true);
  expect((await jobsClient.get(jobId)).state).toBe("Succeeded");
}
