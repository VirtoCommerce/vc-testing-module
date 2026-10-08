import type { HttpClient } from "../../http/http-client";
import type {
  Catalog,
  CatalogData,
  CatalogProduct,
  CatalogProductData,
  CatalogSearchCriteria,
  CatalogSearchResult,
  Category,
  CategoryData,
  ListEntriesMoveRequest,
  ListEntry,
  ListEntrySearchCriteria,
  ListEntrySearchResult,
} from "../types/catalog";

import { requireFields } from "@core/required-fields";

import { CATALOG_FIELDS, CATALOG_PRODUCT_FIELDS, CATEGORY_FIELDS, LIST_ENTRY_FIELDS } from "../types/catalog";

export const CATALOGS_PATH = "/api/catalog/catalogs";
export const CATEGORIES_PATH = "/api/catalog/categories";
export const PRODUCTS_PATH = "/api/catalog/products";
export const LIST_ENTRIES_PATH = "/api/catalog/listentries";

export class CatalogClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async saveCatalog(catalog: CatalogData): Promise<Catalog> {
    const response = await this.#httpClient.post(CATALOGS_PATH, { json: catalog });
    return requireFields(response.expectOk().json<CatalogData>(), CATALOG_FIELDS, "Saved catalog");
  }

  async updateCatalog(catalog: CatalogData): Promise<void> {
    (await this.#httpClient.put(CATALOGS_PATH, { json: catalog })).expectOk();
  }

  async searchCatalogs(criteria: CatalogSearchCriteria): Promise<Catalog[]> {
    const response = await this.#httpClient.post(`${CATALOGS_PATH}/search`, { json: criteria });
    const { results } = response.expectOk().json<CatalogSearchResult>();
    return (results ?? []).map((catalog) => requireFields(catalog, CATALOG_FIELDS, "Found catalog"));
  }

  async deleteCatalog(id: string): Promise<void> {
    (await this.#httpClient.delete(`${CATALOGS_PATH}/${encodeURIComponent(id)}`)).expectOk();
  }

  async saveCategory(category: CategoryData): Promise<Category> {
    const response = await this.#httpClient.post(CATEGORIES_PATH, { json: category });
    return requireFields(response.expectOk().json<CategoryData>(), CATEGORY_FIELDS, "Saved category");
  }

  async getProduct(id: string): Promise<CatalogProduct> {
    return requireFields(await this.#fetchProduct(id), CATALOG_PRODUCT_FIELDS, `Product "${id}"`);
  }

  async findProduct(id: string): Promise<CatalogProduct | undefined> {
    const product = await this.#fetchProduct(id);
    return product === undefined ? undefined : requireFields(product, CATALOG_PRODUCT_FIELDS, `Product "${id}"`);
  }

  async getProductClone(id: string): Promise<CatalogProductData> {
    const response = await this.#httpClient.get(`${PRODUCTS_PATH}/${encodeURIComponent(id)}/clone`);
    return response.expectOk().json<CatalogProductData>();
  }

  async saveProduct(product: CatalogProductData): Promise<CatalogProduct> {
    const response = await this.#httpClient.post(PRODUCTS_PATH, { json: product });
    return requireFields(response.expectOk().json<CatalogProductData>(), CATALOG_PRODUCT_FIELDS, "Saved product");
  }

  async deleteProduct(id: string): Promise<void> {
    (await this.#httpClient.delete(PRODUCTS_PATH, { query: { ids: id } })).expectOk();
  }

  async searchListEntries(criteria: ListEntrySearchCriteria): Promise<ListEntry[]> {
    const response = await this.#httpClient.post(LIST_ENTRIES_PATH, { json: criteria });
    const { results } = response.expectOk().json<ListEntrySearchResult>();
    return (results ?? []).map((entry) => requireFields(entry, LIST_ENTRY_FIELDS, "Found list entry"));
  }

  async getCategory(id: string): Promise<Category> {
    const response = await this.#httpClient.get(`${CATEGORIES_PATH}/${encodeURIComponent(id)}`);
    return requireFields(response.expectOk().json<CategoryData>(), CATEGORY_FIELDS, `Category "${id}"`);
  }

  async getNewCategory(catalogId: string): Promise<CategoryData> {
    const response = await this.#httpClient.get(`/api/catalog/${encodeURIComponent(catalogId)}/categories/newcategory`);
    return response.expectOk().json<CategoryData>();
  }

  async deleteListEntries(ids: string[]): Promise<void> {
    (await this.#httpClient.post(`${LIST_ENTRIES_PATH}/delete`, { json: { objectIds: ids } })).expectOk();
  }

  async moveListEntries(request: ListEntriesMoveRequest): Promise<void> {
    (await this.#httpClient.post(`${LIST_ENTRIES_PATH}/move`, { json: request })).expectOk();
  }

  async #fetchProduct(id: string): Promise<CatalogProductData | undefined> {
    const response = (await this.#httpClient.get(PRODUCTS_PATH, { query: { ids: id } })).expectOk();
    return response.status === 204 ? undefined : response.json<CatalogProductData[]>()[0];
  }
}
