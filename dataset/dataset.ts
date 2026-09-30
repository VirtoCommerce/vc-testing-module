import type { Credentials } from "@api/auth/credentials";
import type { CatalogProduct, CatalogProductData } from "@api/rest/types/catalog";
import type { ApplicationUserData } from "@api/rest/types/security";
import type { WithRequired } from "@core/required-fields";
import type { ManifestItemName } from "./manifest";

import { readdirSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";

import { CATALOG_PRODUCT_FIELDS } from "@api/rest/types/catalog";
import { deepFreeze } from "@core/deep-freeze";
import { fromEnv, interpolate, jsonStringContent } from "@core/interpolate";
import { requireFields } from "@core/required-fields";

import { MANIFEST_ITEMS } from "./manifest";

export type DatasetItem = Readonly<Record<string, unknown>>;
export type Dataset = { readonly [Name in ManifestItemName]: readonly DatasetItem[] };

const DATA_DIR = resolve(__dirname, "data");
const USER_FIELDS = ["userName", "password"] as const;
const USER_IDENTITY_FIELDS = ["id", "userName"] as const;

export type DatasetUser = WithRequired<ApplicationUserData, (typeof USER_IDENTITY_FIELDS)[number]>;

export function loadDataset(): Dataset {
  const dataset = {} as Record<ManifestItemName, DatasetItem[]>;
  for (const { name, dir } of MANIFEST_ITEMS) {
    dataset[name] = readItems(join(DATA_DIR, dir));
  }
  return deepFreeze(dataset);
}

export function getCredentials(dataset: Dataset, username: string): Credentials {
  const item = dataset.users.find((user) => user["userName"] === username);
  const { password } = requireFields(
    item as ApplicationUserData | undefined,
    USER_FIELDS,
    `Dataset user "${username}"`,
  );
  return { username, password };
}

export function getUser(dataset: Dataset, username: string): DatasetUser {
  const item = dataset.users.find((user) => user["userName"] === username);
  return requireFields(item as ApplicationUserData | undefined, USER_IDENTITY_FIELDS, `Dataset user "${username}"`);
}

export function getProduct(dataset: Dataset, id: string): CatalogProduct {
  const item = dataset.products.find((product) => product["id"] === id);
  return requireFields(item as CatalogProductData | undefined, CATALOG_PRODUCT_FIELDS, `Dataset product "${id}"`);
}

function readItems(dir: string): DatasetItem[] {
  return readdirSync(dir, { withFileTypes: true, recursive: true })
    .filter((item) => item.isFile() && item.name.endsWith(".json"))
    .map((item) => join(item.parentPath, item.name))
    .sort()
    .map((file) => JSON.parse(interpolate(readFileSync(file, "utf-8"), { ENV: fromEnv }, jsonStringContent)));
}
