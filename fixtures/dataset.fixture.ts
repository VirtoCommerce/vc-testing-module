import type { Dataset } from "@dataset/dataset";

import { test as base } from "@playwright/test";

import { loadDataset } from "@dataset/dataset";

export interface DatasetWorkerFixtures {
  readonly dataset: Dataset;
}

export const test = base.extend<Record<never, never>, DatasetWorkerFixtures>({
  dataset: [
    async ({}, use) => {
      await use(loadDataset());
    },
    { scope: "worker" },
  ],
});
