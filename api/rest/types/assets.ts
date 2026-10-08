import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommerceAssetsModuleCoreAssetsBlobEntry as BlobEntryData,
  VirtoCommerceAssetsModuleCoreAssetsBlobEntrySearchResult as BlobEntrySearchResult,
  VirtoCommerceAssetsModuleCoreAssetsBlobInfo as BlobInfoData,
} from "../generated/rest-api";

export type { BlobEntryData, BlobEntrySearchResult, BlobInfoData };

export const BLOB_FIELDS = ["name", "url"] as const;

export type BlobEntry = WithRequired<BlobEntryData, (typeof BLOB_FIELDS)[number]>;
export type BlobInfo = WithRequired<BlobInfoData, (typeof BLOB_FIELDS)[number]>;
