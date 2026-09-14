import { existsSync } from "node:fs";
import { dirname, join } from "node:path";

function findEnvFile(): string | undefined {
  let dir = __dirname;
  for (;;) {
    const candidate = join(dir, ".env");
    if (existsSync(candidate)) {
      return candidate;
    }
    const parent = dirname(dir);
    if (parent === dir) {
      return undefined;
    }
    dir = parent;
  }
}

function loadEnv(): void {
  const file = findEnvFile();
  if (file !== undefined) {
    process.loadEnvFile(file);
  }
}

function optional(name: string, fallback: string): string {
  return process.env[name]?.trim() ?? fallback;
}

function bool(name: string, fallback: boolean): boolean {
  const value = process.env[name]?.trim().toLowerCase();
  if (value === undefined || value === "") {
    return fallback;
  }
  return value === "true" || value === "1" || value === "yes";
}

function required(name: string): string {
  const value = process.env[name]?.trim();
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

function requiredUrl(name: string): string {
  const value = required(name);
  try {
    new URL(value);
  } catch {
    throw new Error(`Environment variable ${name} is not a valid URL: ${value}`);
  }
  return value;
}

export interface Env {
  readonly backendBaseUrl: string;
  readonly frontendBaseUrl: string;
  readonly storeId: string;
  readonly verifySsl: boolean;
  readonly adminUsername: string;
  readonly adminPassword: string;
  readonly usersPassword: string;
  readonly quantityControl: string;
  readonly rangeFilterType: string;
  readonly checkoutMode: string;
}

loadEnv();

export const env = {
  backendBaseUrl: requiredUrl("BACKEND_BASE_URL"),
  frontendBaseUrl: requiredUrl("FRONTEND_BASE_URL"),
  storeId: optional("STORE_ID", "store-acme"),
  verifySsl: bool("VERIFY_SSL", false),
  adminUsername: optional("ADMIN_USERNAME", "admin"),
  adminPassword: required("ADMIN_PASSWORD"),
  usersPassword: required("USERS_PASSWORD"),
  quantityControl: optional("QUANTITY_CONTROL", "stepper"),
  rangeFilterType: optional("RANGE_FILTER_TYPE", "slider"),
  checkoutMode: optional("CHECKOUT_MODE", "single-page"),
} satisfies Env;
