import type { HttpClient } from "../../http/http-client";
import type { Currency, CurrencyData } from "../types/core";

import { requireFields } from "@core/required-fields";

import { CURRENCY_FIELDS } from "../types/core";

const CURRENCIES_PATH = "/api/currencies";

export class CurrenciesClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async list(): Promise<Currency[]> {
    const currencies = (await this.#httpClient.get(CURRENCIES_PATH)).expectOk().json<CurrencyData[]>();
    return currencies.map((currency) => requireFields(currency, CURRENCY_FIELDS, "Currency"));
  }

  async find(code: string): Promise<Currency | undefined> {
    return (await this.list()).find((currency) => currency.code === code);
  }

  async create(currency: CurrencyData): Promise<void> {
    (await this.#httpClient.post(CURRENCIES_PATH, { json: currency })).expectOk();
  }

  async update(currency: CurrencyData): Promise<void> {
    (await this.#httpClient.put(CURRENCIES_PATH, { json: currency })).expectOk();
  }

  async delete(code: string): Promise<void> {
    (await this.#httpClient.delete(CURRENCIES_PATH, { query: { codes: code } })).expectOk();
  }
}
