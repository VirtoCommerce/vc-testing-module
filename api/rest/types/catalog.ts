import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommerceCatalogModuleCoreModelCatalog as CatalogData,
  VirtoCommerceCatalogModuleCoreModelCatalogLanguage as CatalogLanguage,
  VirtoCommerceCatalogModuleCoreModelCatalogProduct as CatalogProductData,
  VirtoCommerceCatalogModuleCoreModelSearchCatalogSearchCriteria as CatalogSearchCriteria,
  VirtoCommerceCatalogModuleCoreModelSearchCatalogSearchResult as CatalogSearchResult,
  VirtoCommerceCatalogModuleCoreModelCategory as CategoryData,
  VirtoCommerceCatalogModuleCoreModelListEntriesMoveRequest as ListEntriesMoveRequest,
  VirtoCommerceCatalogModuleCoreModelListEntryListEntryBase as ListEntryData,
  VirtoCommerceCatalogModuleCoreModelSearchCatalogListEntrySearchCriteria as ListEntrySearchCriteria,
  VirtoCommerceCatalogModuleCoreModelSearchListEntrySearchResult as ListEntrySearchResult,
  VirtoCommerceCatalogModuleCoreModelAsset as ProductAsset,
  VirtoCommerceCatalogModuleCoreModelImage as ProductImage,
} from "../generated/rest-api";

export type {
  CatalogData,
  CatalogLanguage,
  CatalogProductData,
  CatalogSearchCriteria,
  CatalogSearchResult,
  CategoryData,
  ListEntriesMoveRequest,
  ListEntryData,
  ListEntrySearchCriteria,
  ListEntrySearchResult,
  ProductAsset,
  ProductImage,
};

export const CATALOG_FIELDS = ["id", "name"] as const;
export const CATEGORY_FIELDS = ["id", "code", "name", "catalogId"] as const;
export const CATALOG_PRODUCT_FIELDS = ["id", "code", "name", "catalogId"] as const;
export const LIST_ENTRY_FIELDS = ["id", "name"] as const;

export type Catalog = WithRequired<CatalogData, (typeof CATALOG_FIELDS)[number]>;
export type Category = WithRequired<CategoryData, (typeof CATEGORY_FIELDS)[number]>;
export type CatalogProduct = WithRequired<CatalogProductData, (typeof CATALOG_PRODUCT_FIELDS)[number]>;
export type ListEntry = WithRequired<ListEntryData, (typeof LIST_ENTRY_FIELDS)[number]>;
