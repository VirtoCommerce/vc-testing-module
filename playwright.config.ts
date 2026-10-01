import type { ApiOptions, BrowserOptions } from "@fixtures";

import { existsSync } from "node:fs";

import { defineConfig, devices } from "@playwright/test";

import { getEnv } from "@core/env";

if (existsSync(".env")) {
  process.loadEnvFile();
}

const env = getEnv();

const DESTRUCTIVE_TAG = /@destructive/;
const E2E_EXPECT_TIMEOUT_MS = 30_000;
const E2E_TEST_TIMEOUT_MS = 120_000;
const E2E_FRONTEND_WORKERS = env.e2eWorkers ?? (process.env["CI"] ? 2 : undefined);
const E2E_USE = {
  ...devices["Desktop Chrome"],
  viewport: { width: 1920, height: 1080 },
  screenshot: "only-on-failure",
  actionTimeout: 30_000,
  navigationTimeout: 30_000,
} as const;

export default defineConfig<ApiOptions & BrowserOptions>({
  testDir: "tests",
  ...(env.runDestructiveTests ? {} : { grepInvert: DESTRUCTIVE_TAG }),
  fullyParallel: true,
  reporter: [["list"], ["allure-playwright", { resultsDir: "allure-results" }]],
  use: {
    ignoreHTTPSErrors: !env.verifySsl,
    trace: "retain-on-failure",
  },
  projects: [
    {
      name: "seed",
      testDir: "tests/setup",
      testMatch: "*.setup.ts",
      retries: 0,
    },
    {
      name: "restapi",
      testDir: "tests/restapi",
    },
    {
      name: "graphql",
      testDir: "tests/graphql",
    },
    {
      name: "e2e-frontend",
      testDir: "tests/e2e/frontend",
      ...(E2E_FRONTEND_WORKERS === undefined ? {} : { workers: E2E_FRONTEND_WORKERS }),
      timeout: E2E_TEST_TIMEOUT_MS,
      expect: { timeout: E2E_EXPECT_TIMEOUT_MS },
      use: { ...E2E_USE, app: "frontend", baseURL: env.frontendBaseUrl },
    },
    {
      name: "e2e-backend",
      testDir: "tests/e2e/backend",
      workers: 1,
      timeout: E2E_TEST_TIMEOUT_MS,
      expect: { timeout: E2E_EXPECT_TIMEOUT_MS },
      use: { ...E2E_USE, app: "backend", baseURL: env.backendBaseUrl, user: env.admin },
    },
  ],
});
