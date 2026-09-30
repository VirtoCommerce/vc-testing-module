import type { HttpClient } from "../../http/http-client";
import type { SettingEntry, SettingEntryData } from "../types/settings";

import { requireFields } from "@core/required-fields";

import { SETTING_FIELDS } from "../types/settings";

const SETTINGS_PATH = "/api/platform/settings";

export class SettingsClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async get(name: string): Promise<SettingEntry> {
    const response = await this.#httpClient.get(`${SETTINGS_PATH}/${encodeURIComponent(name)}`);
    return requireFields(response.expectOk().json<SettingEntryData>(), SETTING_FIELDS, `Setting "${name}"`);
  }

  async list(): Promise<SettingEntry[]> {
    return this.#list(SETTINGS_PATH, "Setting");
  }

  async listByModule(moduleId: string): Promise<SettingEntry[]> {
    return this.#list(`${SETTINGS_PATH}/modules/${encodeURIComponent(moduleId)}`, `Setting of "${moduleId}"`);
  }

  async getUiCustomization(): Promise<SettingEntry> {
    const response = await this.#httpClient.get(`${SETTINGS_PATH}/ui/customization`);
    return requireFields(response.expectOk().json<SettingEntryData>(), SETTING_FIELDS, "UI customization setting");
  }

  async getValues(name: string): Promise<unknown[]> {
    const response = await this.#httpClient.get(`${SETTINGS_PATH}/values/${encodeURIComponent(name)}`);
    return response.expectOk().json<unknown[]>();
  }

  async save(settings: SettingEntryData[]): Promise<void> {
    (await this.#httpClient.post(SETTINGS_PATH, { json: settings })).expectOk();
  }

  async #list(path: string, label: string): Promise<SettingEntry[]> {
    const settings = (await this.#httpClient.get(path)).expectOk().json<SettingEntryData[]>();
    return settings.map((setting) => requireFields(setting, SETTING_FIELDS, label));
  }
}
