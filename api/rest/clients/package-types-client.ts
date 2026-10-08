import type { HttpClient } from "../../http/http-client";
import type { PackageType, PackageTypeData } from "../types/core";

import { requireFields } from "@core/required-fields";

import { PACKAGE_TYPE_FIELDS } from "../types/core";

const PACKAGE_TYPES_PATH = "/api/packageTypes";

export class PackageTypesClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async list(): Promise<PackageType[]> {
    const packageTypes = (await this.#httpClient.get(PACKAGE_TYPES_PATH)).expectOk().json<PackageTypeData[]>();
    return packageTypes.map((packageType) => requireFields(packageType, PACKAGE_TYPE_FIELDS, "Package type"));
  }

  async find(id: string): Promise<PackageType | undefined> {
    return (await this.list()).find((packageType) => packageType.id === id);
  }

  async create(packageType: PackageTypeData): Promise<void> {
    (await this.#httpClient.post(PACKAGE_TYPES_PATH, { json: packageType })).expectOk();
  }

  async update(packageType: PackageTypeData): Promise<void> {
    (await this.#httpClient.put(PACKAGE_TYPES_PATH, { json: packageType })).expectOk();
  }

  async delete(id: string): Promise<void> {
    (await this.#httpClient.delete(PACKAGE_TYPES_PATH, { query: { ids: id } })).expectOk();
  }
}
