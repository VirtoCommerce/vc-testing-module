import type { StoreData } from "@api/rest/types/store";
import type { WithRequired } from "@core/required-fields";

import { uniqueId } from "@core/unique-id";

import { SEEDED_CATALOG_ID } from "./catalog";

export type StoreDraft = WithRequired<StoreData, "id" | "name" | "catalog">;

export function newStore(id = uniqueId("test-store")): StoreDraft {
  return { id, name: id, catalog: SEEDED_CATALOG_ID, storeState: "Open" };
}
