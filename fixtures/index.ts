import { mergeTests } from "@playwright/test";

import { test as cartTest } from "./cart.fixture";
import { test as cleanupTest } from "./cleanup.fixture";
import { test as datasetTest } from "./dataset.fixture";
import { test as frontendContextTest } from "./frontend-context.fixture";
import { test as pageBuilderTest } from "./page-builder.fixture";

export type { ApiOptions } from "./api.fixture";
export type { BrowserOptions } from "./browser.fixture";
export type { ShopperAccount, SignedInCustomerAccount } from "./customer-account.fixture";
export type { Shopper } from "./shopper.fixture";

export { expect } from "@playwright/test";

export { withItems } from "./cart.fixture";

export const test = mergeTests(cartTest, cleanupTest, datasetTest, frontendContextTest, pageBuilderTest);
