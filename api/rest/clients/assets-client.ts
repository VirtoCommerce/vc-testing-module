import type { HttpClient, MultipartFile } from "../../http/http-client";
import type { BlobEntry, BlobEntrySearchResult, BlobInfo, BlobInfoData } from "../types/assets";

import { requireFields } from "@core/required-fields";

import { BLOB_FIELDS } from "../types/assets";

export const ASSETS_PATH = "/api/assets";

export class AssetsClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async list(folderUrl = ""): Promise<BlobEntry[]> {
    const response = await this.#httpClient.get(ASSETS_PATH, { query: { folderUrl } });
    const { results } = response.expectOk().json<BlobEntrySearchResult>();
    return (results ?? []).map((entry) => requireFields(entry, BLOB_FIELDS, `Asset entry in "${folderUrl}"`));
  }

  async find(name: string, folderUrl = ""): Promise<BlobEntry | undefined> {
    return (await this.list(folderUrl)).find((entry) => entry.name === name);
  }

  async createFolder(name: string, parentUrl = ""): Promise<void> {
    (await this.#httpClient.post(`${ASSETS_PATH}/folder`, { json: { name, parentUrl } })).expectOk();
  }

  async uploadFromUrl(folderUrl: string, url: string): Promise<BlobInfo> {
    const response = await this.#httpClient.post(ASSETS_PATH, { query: { folderUrl, url } });
    const [file] = response.expectOk().json<BlobInfoData[]>();
    return requireFields(file, BLOB_FIELDS, `File uploaded from ${url}`);
  }

  async upload(folderUrl: string, file: MultipartFile): Promise<BlobInfo> {
    const response = await this.#httpClient.post(ASSETS_PATH, { query: { folderUrl }, multipart: { file } });
    const [uploaded] = response.expectOk().json<BlobInfoData[]>();
    return requireFields(uploaded, BLOB_FIELDS, `File ${file.name} uploaded to "${folderUrl}"`);
  }

  async uploadToLocalStorage(file: MultipartFile): Promise<BlobInfo> {
    const response = await this.#httpClient.post(`${ASSETS_PATH}/localstorage`, { multipart: { file } });
    const [uploaded] = response.expectOk().json<BlobInfoData[]>();
    return requireFields(uploaded, BLOB_FIELDS, `File ${file.name} uploaded to local storage`);
  }

  async remove(url: string): Promise<void> {
    await this.removeMany([url]);
  }

  async removeMany(urls: readonly string[]): Promise<void> {
    (await this.#httpClient.delete(ASSETS_PATH, { query: { urls } })).expectOk();
  }

  async removeFolder(name: string): Promise<void> {
    const folder = await this.find(name);
    if (folder !== undefined) {
      await this.remove(folder.url);
    }
  }
}
