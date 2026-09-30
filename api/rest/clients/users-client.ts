import type { HttpClient } from "../../http/http-client";
import type {
  ApplicationUser,
  ApplicationUserData,
  IdentityResult,
  SecurityResult,
  UserApiKey,
  UserApiKeyData,
  UserDetail,
  UserSearchCriteria,
  UserSearchResult,
} from "../types/security";

import { requireFields } from "@core/required-fields";

import { APPLICATION_USER_FIELDS, USER_API_KEY_FIELDS } from "../types/security";

const SECURITY_PATH = "/api/platform/security";
const USERS_PATH = `${SECURITY_PATH}/users`;

export class UsersClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async create(user: ApplicationUserData): Promise<SecurityResult> {
    return (await this.#httpClient.post(`${USERS_PATH}/create`, { json: user })).expectOk().json<SecurityResult>();
  }

  async get(userName: string): Promise<ApplicationUser> {
    return requireFields(await this.find(userName), APPLICATION_USER_FIELDS, `User "${userName}"`);
  }

  async find(userName: string): Promise<ApplicationUser | undefined> {
    return this.#fetch(`${USERS_PATH}/${encodeURIComponent(userName)}`, `User "${userName}"`);
  }

  async getById(id: string): Promise<ApplicationUser> {
    const user = await this.#fetch(`${USERS_PATH}/id/${encodeURIComponent(id)}`, `User "${id}"`);
    return requireFields(user, APPLICATION_USER_FIELDS, `User "${id}"`);
  }

  async search(criteria: UserSearchCriteria): Promise<ApplicationUser[]> {
    const response = await this.#httpClient.post(`${USERS_PATH}/search`, { json: criteria });
    const { users } = response.expectOk().json<UserSearchResult>();
    return (users ?? []).map((user) => requireFields(user, APPLICATION_USER_FIELDS, "Found user"));
  }

  async update(user: ApplicationUserData): Promise<SecurityResult> {
    return (await this.#httpClient.put(USERS_PATH, { json: user })).expectOk().json<SecurityResult>();
  }

  async delete(userNames: readonly string[]): Promise<void> {
    (await this.#httpClient.delete(USERS_PATH, { query: { names: userNames } })).expectOk();
  }

  async lock(id: string): Promise<SecurityResult> {
    return (await this.#httpClient.post(`${USERS_PATH}/${encodeURIComponent(id)}/lock`))
      .expectOk()
      .json<SecurityResult>();
  }

  async unlock(id: string): Promise<SecurityResult> {
    return (await this.#httpClient.post(`${USERS_PATH}/${encodeURIComponent(id)}/unlock`))
      .expectOk()
      .json<SecurityResult>();
  }

  async changePassword(userName: string, oldPassword: string, newPassword: string): Promise<SecurityResult> {
    const path = `${USERS_PATH}/${encodeURIComponent(userName)}/changepassword`;
    return (await this.#httpClient.post(path, { json: { oldPassword, newPassword } }))
      .expectOk()
      .json<SecurityResult>();
  }

  async resetPassword(userName: string, newPassword: string): Promise<SecurityResult> {
    const path = `${USERS_PATH}/${encodeURIComponent(userName)}/resetpassword`;
    return (await this.#httpClient.post(path, { json: { newPassword, forcePasswordChangeOnNextSignIn: false } }))
      .expectOk()
      .json<SecurityResult>();
  }

  async generatePasswordResetToken(id: string): Promise<string> {
    const path = `${USERS_PATH}/${encodeURIComponent(id)}/generatePasswordResetToken`;
    return (await this.#httpClient.get(path)).expectOk().text;
  }

  async confirmPasswordReset(id: string, token: string, newPassword: string): Promise<SecurityResult> {
    const path = `${USERS_PATH}/${encodeURIComponent(id)}/resetpasswordconfirm`;
    return (await this.#httpClient.post(path, { json: { token, newPassword } })).expectOk().json<SecurityResult>();
  }

  async validatePassword(password: string): Promise<IdentityResult> {
    return (await this.#httpClient.post(`${SECURITY_PATH}/validatepassword`, { json: password }))
      .expectOk()
      .json<IdentityResult>();
  }

  async sendVerificationEmail(id: string): Promise<void> {
    (await this.#httpClient.post(`${USERS_PATH}/${encodeURIComponent(id)}/sendVerificationEmail`)).expectOk();
  }

  async getCurrentUser(): Promise<UserDetail> {
    return (await this.#httpClient.get(`${SECURITY_PATH}/currentuser`)).expectOk().json<UserDetail>();
  }

  async listApiKeys(userId: string): Promise<UserApiKey[]> {
    const response = await this.#httpClient.get(`${USERS_PATH}/${encodeURIComponent(userId)}/apikeys`);
    return response
      .expectOk()
      .json<UserApiKeyData[]>()
      .map((apiKey) => requireFields(apiKey, USER_API_KEY_FIELDS, `API key of "${userId}"`));
  }

  async createApiKey(apiKey: UserApiKeyData): Promise<void> {
    (await this.#httpClient.post(`${USERS_PATH}/apikeys`, { json: apiKey })).expectOk();
  }

  async updateApiKey(apiKey: UserApiKeyData): Promise<void> {
    (await this.#httpClient.put(`${USERS_PATH}/apikeys`, { json: apiKey })).expectOk();
  }

  async deleteApiKeys(ids: readonly string[]): Promise<void> {
    (await this.#httpClient.delete(`${USERS_PATH}/apikeys`, { query: { ids } })).expectOk();
  }

  async #fetch(path: string, label: string): Promise<ApplicationUser | undefined> {
    const user = (await this.#httpClient.get(path)).expectOk().json<ApplicationUserData | null>();
    return user === null ? undefined : requireFields(user, APPLICATION_USER_FIELDS, label);
  }
}
