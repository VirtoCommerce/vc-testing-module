import { PageBuilderClient } from "@api/rest/clients/page-builder-client";
import { PageBuilderShell } from "@pages/backend/page-builder/page-builder-shell";

import { test as base } from "./shopper.fixture";

export interface PageBuilderFixtures {
  readonly pageBuilder: PageBuilderShell;
  readonly pageBuilderClient: PageBuilderClient;
}

export const test = base.extend<PageBuilderFixtures>({
  pageBuilder: async ({ page, env }, use) => {
    await use(new PageBuilderShell(page, { path: env.pageBuilderPath, storeId: env.storeId }));
  },

  pageBuilderClient: async ({ platformAdminHttpClient }, use) => {
    await use(new PageBuilderClient(platformAdminHttpClient));
  },
});
