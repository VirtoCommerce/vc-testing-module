import { mergeTests } from "@playwright/test";

import { auth } from "./auth";
import { globalOptions } from "./global-options";
import { pages } from "./pages";

export const test = mergeTests(globalOptions, auth, pages);

export { expect } from "@playwright/test";
export type { Auth, WorkerUser } from "./auth";
export type { GlobalOptions } from "./global-options";
export type { Pages } from "./pages";
