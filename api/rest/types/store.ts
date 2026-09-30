import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommerceStoreModuleCoreModelStore as GeneratedStoreData,
  VirtoCommerceStoreModuleCoreModelSearchStoreSearchCriteria as StoreSearchCriteria,
  VirtoCommerceStoreModuleCoreModelSearchStoreSearchResult as StoreSearchResult,
} from "../generated/rest-api";
import type { SettingEntryData } from "./settings";

export type { StoreSearchCriteria, StoreSearchResult };

export type StoreData = Omit<GeneratedStoreData, "settings"> & { settings?: SettingEntryData[] | null };

export const STORE_FIELDS = ["id", "name", "catalog"] as const;

export type Store = WithRequired<StoreData, (typeof STORE_FIELDS)[number]>;
