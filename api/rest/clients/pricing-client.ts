import type { HttpClient, QueryParams } from "../../http/http-client";
import type {
  Price,
  PriceData,
  Pricelist,
  PricelistAssignment,
  PricelistAssignmentData,
  PricelistAssignmentSearchResult,
  PricelistData,
  PricelistSearchResult,
  PricesSearchCriteria,
  ProductPriceData,
  ProductPriceSearchResult,
} from "../types/pricing";

import { requireFields } from "@core/required-fields";

import { PRICE_FIELDS, PRICELIST_ASSIGNMENT_FIELDS, PRICELIST_FIELDS } from "../types/pricing";

const PRICELISTS_PATH = "/api/pricing/pricelists";
const ASSIGNMENTS_PATH = "/api/pricing/assignments";

export class PricingClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async getPricelist(id: string): Promise<Pricelist> {
    return requireFields(await this.#fetchPricelist(id), PRICELIST_FIELDS, `Pricelist "${id}"`);
  }

  async findPricelist(id: string): Promise<Pricelist | undefined> {
    const pricelist = await this.#fetchPricelist(id);
    return pricelist === undefined ? undefined : requireFields(pricelist, PRICELIST_FIELDS, `Pricelist "${id}"`);
  }

  async createPricelist(pricelist: PricelistData): Promise<Pricelist> {
    const response = await this.#httpClient.post(PRICELISTS_PATH, { json: pricelist });
    return requireFields(response.expectOk().json<PricelistData>(), PRICELIST_FIELDS, "Created pricelist");
  }

  async updatePricelist(pricelist: PricelistData): Promise<void> {
    (await this.#httpClient.put(PRICELISTS_PATH, { json: pricelist })).expectOk();
  }

  async searchPricelists(query: QueryParams): Promise<Pricelist[]> {
    const { results } = (await this.#httpClient.get(PRICELISTS_PATH, { query }))
      .expectOk()
      .json<PricelistSearchResult>();
    return (results ?? []).map((pricelist) => requireFields(pricelist, PRICELIST_FIELDS, "Found pricelist"));
  }

  async deletePricelist(id: string): Promise<void> {
    (await this.#httpClient.delete(PRICELISTS_PATH, { query: { ids: id } })).expectOk();
  }

  async savePrices(productPrices: ProductPriceData[]): Promise<void> {
    (await this.#httpClient.put("/api/products/prices", { json: productPrices })).expectOk();
  }

  async saveProductPrices(productPrice: ProductPriceData & { productId: string }): Promise<void> {
    const path = `/api/products/${encodeURIComponent(productPrice.productId)}/prices`;
    (await this.#httpClient.put(path, { json: productPrice })).expectOk();
  }

  async searchPrices(criteria: PricesSearchCriteria): Promise<Price[]> {
    const { results } = (await this.#httpClient.post("/api/catalog/products/prices/search", { json: criteria }))
      .expectOk()
      .json<ProductPriceSearchResult>();
    return (results ?? [])
      .flatMap((productPrice) => productPrice.prices ?? [])
      .map((price) => requireFields(price, PRICE_FIELDS, "Found price"));
  }

  async searchPricesByPricelist(pricelistId: string): Promise<Price[]> {
    const { results } = (
      await this.#httpClient.get("/api/catalog/products/prices/search", { query: { PriceListId: pricelistId } })
    )
      .expectOk()
      .json<ProductPriceSearchResult>();
    return (results ?? [])
      .flatMap((productPrice) => productPrice.prices ?? [])
      .map((price) => requireFields(price, PRICE_FIELDS, "Found price"));
  }

  async getPricesWidget(productId: string, catalogId: string): Promise<Price[]> {
    const path = `/api/products/${encodeURIComponent(productId)}/${encodeURIComponent(catalogId)}/pricesWidget`;
    return (await this.#httpClient.get(path))
      .expectOk()
      .json<PriceData[]>()
      .map((price) => requireFields(price, PRICE_FIELDS, `Widget price of product "${productId}"`));
  }

  async deletePrices(priceIds: readonly string[]): Promise<void> {
    (await this.#httpClient.delete("/api/pricing/products/prices", { query: { priceIds } })).expectOk();
  }

  async deleteProductPrices(pricelistId: string, productIds: readonly string[]): Promise<void> {
    const path = `${PRICELISTS_PATH}/${encodeURIComponent(pricelistId)}/products/prices`;
    (await this.#httpClient.delete(path, { query: { productIds } })).expectOk();
  }

  async getAssignment(id: string): Promise<PricelistAssignment> {
    return requireFields(await this.#fetchAssignment(id), PRICELIST_ASSIGNMENT_FIELDS, `Assignment "${id}"`);
  }

  async findAssignment(id: string): Promise<PricelistAssignment | undefined> {
    const assignment = await this.#fetchAssignment(id);
    return assignment === undefined
      ? undefined
      : requireFields(assignment, PRICELIST_ASSIGNMENT_FIELDS, `Assignment "${id}"`);
  }

  async getNewAssignment(): Promise<PricelistAssignmentData> {
    return (await this.#httpClient.get(`${ASSIGNMENTS_PATH}/new`)).expectOk().json<PricelistAssignmentData>();
  }

  async createAssignment(assignment: PricelistAssignmentData): Promise<PricelistAssignment> {
    const response = await this.#httpClient.post(ASSIGNMENTS_PATH, { json: assignment });
    return requireFields(
      response.expectOk().json<PricelistAssignmentData>(),
      PRICELIST_ASSIGNMENT_FIELDS,
      "Created assignment",
    );
  }

  async updateAssignment(assignment: PricelistAssignmentData): Promise<void> {
    (await this.#httpClient.put(ASSIGNMENTS_PATH, { json: assignment })).expectOk();
  }

  async searchAssignments(query: QueryParams): Promise<PricelistAssignment[]> {
    const { results } = (await this.#httpClient.get(ASSIGNMENTS_PATH, { query }))
      .expectOk()
      .json<PricelistAssignmentSearchResult>();
    return (results ?? []).map((assignment) =>
      requireFields(assignment, PRICELIST_ASSIGNMENT_FIELDS, "Found assignment"),
    );
  }

  async deleteAssignment(id: string): Promise<void> {
    (await this.#httpClient.delete(ASSIGNMENTS_PATH, { query: { ids: id } })).expectOk();
  }

  async deleteFilteredAssignments(query: QueryParams): Promise<void> {
    (await this.#httpClient.delete("/api/pricing/filteredAssignments", { query })).expectOk();
  }

  async #fetchPricelist(id: string): Promise<PricelistData | undefined> {
    const response = (await this.#httpClient.get(`${PRICELISTS_PATH}/${encodeURIComponent(id)}`)).expectOk();
    return response.json<PricelistData | null>() ?? undefined;
  }

  async #fetchAssignment(id: string): Promise<PricelistAssignmentData | undefined> {
    const response = (await this.#httpClient.get(`${ASSIGNMENTS_PATH}/${encodeURIComponent(id)}`)).expectOk();
    return response.json<PricelistAssignmentData | null>() ?? undefined;
  }
}
