import type { CatalogData, CatalogLanguage, CatalogProductData, CategoryData } from "@api/rest/types/catalog";

import { uniqueId } from "@core/unique-id";

export const SEEDED_CATALOG_ID = "catalog-acme-electronics";

export const DEFAULT_LANGUAGE = { languageCode: "en-US", isDefault: true } satisfies CatalogLanguage;

export function newCatalog(name = uniqueId("test-catalog")): CatalogData {
  return { name, isVirtual: false, defaultLanguage: DEFAULT_LANGUAGE, languages: [DEFAULT_LANGUAGE] };
}

export function newCategory(catalogId: string): CategoryData {
  const code = uniqueId("test-category");
  return { catalogId, name: code, code, isActive: true };
}

export function newProduct(catalogId: string, categoryId: string): CatalogProductData {
  const code = uniqueId("test-product");
  return { catalogId, categoryId, name: code, code, productType: "Physical" };
}
