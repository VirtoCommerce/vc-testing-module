import { env as processEnv, type Env } from "@config/env";
import { test as base } from "@playwright/test";

export interface GlobalOptions {
  env: Env;
}

export const globalOptions = base.extend<GlobalOptions>({
  env: [processEnv, { option: true }],
});
