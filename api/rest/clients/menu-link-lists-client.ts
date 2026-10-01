import type { HttpClient } from "../../http/http-client";
import type { MenuLinkList, MenuLinkListData } from "../types/content";

import { requireFields } from "@core/required-fields";

import { MENU_LINK_LIST_FIELDS } from "../types/content";

export class MenuLinkListsClient {
  readonly #httpClient: HttpClient;
  readonly #path: string;

  constructor(httpClient: HttpClient, storeId: string) {
    this.#httpClient = httpClient;
    this.#path = `/api/cms/${encodeURIComponent(storeId)}/menu`;
  }

  async list(): Promise<MenuLinkList[]> {
    const response = (await this.#httpClient.get(this.#path)).expectOk();
    const lists = response.text === "" ? [] : response.json<MenuLinkListData[]>();
    return lists.map((list) => requireFields(list, MENU_LINK_LIST_FIELDS, "Menu link list"));
  }

  async get(id: string): Promise<MenuLinkList> {
    return requireFields(await this.#fetch(id), MENU_LINK_LIST_FIELDS, `Menu link list "${id}"`);
  }

  async find(id: string): Promise<MenuLinkList | undefined> {
    const list = await this.#fetch(id);
    return list === undefined ? undefined : requireFields(list, MENU_LINK_LIST_FIELDS, `Menu link list "${id}"`);
  }

  async save(list: MenuLinkListData): Promise<void> {
    (await this.#httpClient.post(this.#path, { json: list })).expectOk();
  }

  async delete(id: string): Promise<void> {
    (await this.#httpClient.delete(this.#path, { query: { listIds: id } })).expectOk();
  }

  async isNameAvailable(name: string, language: string, listId?: string): Promise<boolean> {
    const response = await this.#httpClient.get(`${this.#path}/checkname`, {
      query: { name, language, id: listId },
    });
    return response.expectOk().json<{ result: boolean }>().result;
  }

  async #fetch(id: string): Promise<MenuLinkListData | undefined> {
    const response = (await this.#httpClient.get(`${this.#path}/${encodeURIComponent(id)}`)).expectOk();
    return response.json<MenuLinkListData | null>() ?? undefined;
  }
}
