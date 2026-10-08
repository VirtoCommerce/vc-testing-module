import type { HttpClient } from "../../http/http-client";
import type {
  Permission,
  Role,
  RoleData,
  RoleSearchCriteria,
  RoleSearchResult,
  SecurityResult,
} from "../types/security";

import { requireFields } from "@core/required-fields";

import { ROLE_FIELDS } from "../types/security";

const ROLES_PATH = "/api/platform/security/roles";

export class RolesClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async save(role: RoleData): Promise<SecurityResult> {
    return (await this.#httpClient.put(ROLES_PATH, { json: role })).expectOk().json<SecurityResult>();
  }

  async get(name: string): Promise<Role> {
    return requireFields(await this.find(name), ROLE_FIELDS, `Role "${name}"`);
  }

  async find(name: string): Promise<Role | undefined> {
    const role = (await this.#httpClient.get(`${ROLES_PATH}/${encodeURIComponent(name)}`))
      .expectOk()
      .json<RoleData | null>();
    return role === null ? undefined : requireFields(role, ROLE_FIELDS, `Role "${name}"`);
  }

  async search(criteria: RoleSearchCriteria): Promise<Role[]> {
    const response = await this.#httpClient.post(`${ROLES_PATH}/search`, { json: criteria });
    const { roles } = response.expectOk().json<RoleSearchResult>();
    return (roles ?? []).map((role) => requireFields(role, ROLE_FIELDS, "Found role"));
  }

  async delete(ids: readonly string[]): Promise<void> {
    (await this.#httpClient.delete(ROLES_PATH, { query: { ids } })).expectOk();
  }

  async listPermissions(): Promise<Permission[]> {
    return (await this.#httpClient.get("/api/platform/security/permissions")).expectOk().json<Permission[]>();
  }
}
