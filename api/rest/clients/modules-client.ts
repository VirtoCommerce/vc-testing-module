import type { HttpClient } from "../../http/http-client";
import type { ModuleDescriptorData } from "../types/modules";

import { requireFields } from "@core/required-fields";

import { MODULE_DESCRIPTOR_FIELDS } from "../types/modules";

const MODULES_PATH = "/api/platform/modules";

export class ModulesClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async getInstalledIds(): Promise<ReadonlySet<string>> {
    const modules = (await this.#httpClient.get(MODULES_PATH)).expectOk().json<ModuleDescriptorData[]>();
    return new Set(
      modules
        .filter((module) => module.isInstalled)
        .map((module) => requireFields(module, MODULE_DESCRIPTOR_FIELDS, "Installed module").id),
    );
  }

  async list(): Promise<ModuleDescriptorData[]> {
    return (await this.#httpClient.get(MODULES_PATH)).expectOk().json<ModuleDescriptorData[]>();
  }

  async reload(): Promise<void> {
    (await this.#httpClient.post(`${MODULES_PATH}/reload`)).expectOk();
  }

  async restart(): Promise<void> {
    (await this.#httpClient.post(`${MODULES_PATH}/restart`)).expectOk();
  }
}
