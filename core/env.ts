import type { output } from "zod";

import { coerce, enum as enumOf, object, prettifyError, string, stringbool, url } from "zod";

export const QUANTITY_CONTROL = ["stepper", "button"] as const;
export type QuantityControl = (typeof QUANTITY_CONTROL)[number];

export const RANGE_FILTER_TYPE = ["slider", "default"] as const;
export type RangeFilterType = (typeof RANGE_FILTER_TYPE)[number];

export const CHECKOUT_MODE = ["single-page", "multi-step"] as const;
export type CheckoutMode = (typeof CHECKOUT_MODE)[number];

const positiveInt = coerce.number().int().positive();

const EnvSchema = object({
  BACKEND_BASE_URL: url(),
  FRONTEND_BASE_URL: url(),
  PAGE_BUILDER_PATH: string().default("/apps/page-builder-shell/"),
  STORE_ID: string(),
  ADMIN_USERNAME: string(),
  ADMIN_PASSWORD: string(),
  USERS_PASSWORD: string(),
  REQUEST_TIMEOUT_MS: positiveInt.default(30_000),
  VERIFY_SSL: stringbool().default(true),
  RUN_DESTRUCTIVE_TESTS: stringbool().default(false),
  PAGE_SIZE: positiveInt.default(20),
  E2E_WORKERS: positiveInt.optional(),
  QUANTITY_CONTROL: enumOf(QUANTITY_CONTROL).default("stepper"),
  RANGE_FILTER_TYPE: enumOf(RANGE_FILTER_TYPE).default("slider"),
  CHECKOUT_MODE: enumOf(CHECKOUT_MODE).default("single-page"),
  GOOGLE_MAPS_API_KEY: string().optional(),
  SEED_ONLY: string().optional(),
}).transform((vars) =>
  Object.freeze({
    backendBaseUrl: vars.BACKEND_BASE_URL,
    frontendBaseUrl: vars.FRONTEND_BASE_URL,
    pageBuilderPath: vars.PAGE_BUILDER_PATH,
    storeId: vars.STORE_ID,
    admin: Object.freeze({ username: vars.ADMIN_USERNAME, password: vars.ADMIN_PASSWORD }),
    usersPassword: vars.USERS_PASSWORD,
    requestTimeoutMs: vars.REQUEST_TIMEOUT_MS,
    verifySsl: vars.VERIFY_SSL,
    runDestructiveTests: vars.RUN_DESTRUCTIVE_TESTS,
    pageSize: vars.PAGE_SIZE,
    e2eWorkers: vars.E2E_WORKERS,
    quantityControl: vars.QUANTITY_CONTROL,
    rangeFilterType: vars.RANGE_FILTER_TYPE,
    checkoutMode: vars.CHECKOUT_MODE,
    googleMapsApiKey: vars.GOOGLE_MAPS_API_KEY,
    seedOnly: vars.SEED_ONLY,
  }),
);

export type Env = output<typeof EnvSchema>;

let cachedEnv: Env | undefined;

export function getEnv(): Env {
  if (!cachedEnv) {
    const result = EnvSchema.safeParse(process.env);
    if (!result.success) {
      throw new Error(`Invalid environment:\n${prettifyError(result.error)}`);
    }
    cachedEnv = result.data;
  }
  return cachedEnv;
}
