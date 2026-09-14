import { env } from "@config/env";
import type { GlobalOptions } from "@fixtures/base";
import { defineConfig, devices } from "@playwright/test";

const isCI = Boolean(process.env.CI);

export default defineConfig<GlobalOptions>({
  testDir: "./tests",
  fullyParallel: true,
  forbidOnly: isCI,
  retries: isCI ? 2 : 0,
  reporter: isCI ? [["list"], ["html", { open: "never" }]] : [["list"]],
  use: {
    baseURL: env.frontendBaseUrl,
    testIdAttribute: "data-test-id",
    ignoreHTTPSErrors: !env.verifySsl,
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
