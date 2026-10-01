import type { HttpClient, MultipartFile } from "../../http/http-client";
import type {
  ContentItem,
  ContentItemData,
  ContentStatistic,
  ContentStatisticData,
  ContentType,
} from "../types/content";

import { requireFields } from "@core/required-fields";

import { CONTENT_ITEM_FIELDS, CONTENT_STATISTIC_FIELDS } from "../types/content";

export function contentPath(contentType: ContentType, storeId: string): string {
  return `/api/content/${contentType}/${encodeURIComponent(storeId)}`;
}

export class ContentClient {
  readonly #httpClient: HttpClient;
  readonly #storeId: string;

  constructor(httpClient: HttpClient, storeId: string) {
    this.#httpClient = httpClient;
    this.#storeId = storeId;
  }

  async getStatistic(): Promise<ContentStatistic> {
    const response = await this.#httpClient.get(`/api/content/${encodeURIComponent(this.#storeId)}/stats`);
    return requireFields(
      response.expectOk().json<ContentStatisticData>(),
      CONTENT_STATISTIC_FIELDS,
      `Content statistic of store "${this.#storeId}"`,
    );
  }

  async createFolder(contentType: ContentType, name: string): Promise<void> {
    const response = await this.#httpClient.post(`${this.#path(contentType)}/folder`, {
      json: { name, type: "folder" },
    });
    response.expectOk();
  }

  async upload(contentType: ContentType, folderUrl: string, file: MultipartFile): Promise<ContentItem[]> {
    const response = await this.#httpClient.post(this.#path(contentType), {
      query: { folderUrl },
      multipart: { file },
    });
    return response
      .expectOk()
      .json<ContentItemData[]>()
      .map((item) => requireFields(item, CONTENT_ITEM_FIELDS, `Uploaded ${contentType} item`));
  }

  async search(contentType: ContentType, keyword: string): Promise<ContentItem[]> {
    const response = await this.#httpClient.get(`${this.#path(contentType)}/search`, { query: { keyword } });
    return response
      .expectOk()
      .json<ContentItemData[]>()
      .map((item) => requireFields(item, CONTENT_ITEM_FIELDS, `Found ${contentType} item`));
  }

  async getByName(contentType: ContentType, name: string): Promise<ContentItem> {
    return requireFields(
      await this.findByName(contentType, name),
      CONTENT_ITEM_FIELDS,
      `${contentType} item "${name}"`,
    );
  }

  async findByName(contentType: ContentType, name: string): Promise<ContentItem | undefined> {
    return (await this.search(contentType, name)).find((item) => item.name === name);
  }

  async getFileContent(contentType: ContentType, relativeUrl: string): Promise<string | undefined> {
    const response = await this.#httpClient.get(this.#path(contentType), { query: { relativeUrl } });
    return response.status === 404 ? undefined : response.expectOk().text;
  }

  async move(contentType: ContentType, oldUrl: string, newUrl: string): Promise<void> {
    (await this.#httpClient.get(`${this.#path(contentType)}/move`, { query: { oldUrl, newUrl } })).expectOk();
  }

  async delete(contentType: ContentType, url: string): Promise<void> {
    (await this.#httpClient.delete(this.#path(contentType), { query: { urls: url } })).expectOk();
  }

  async removeFolder(contentType: ContentType, name: string): Promise<void> {
    const folder = await this.findByName(contentType, name);
    if (folder !== undefined) {
      await this.delete(contentType, folder.url);
    }
  }

  #path(contentType: ContentType): string {
    return contentPath(contentType, this.#storeId);
  }
}
