import type { HttpClient } from "../../http/http-client";
import type {
  CreateGroupedPageRequest,
  GroupedPage,
  GroupedPageData,
  GroupedPageSearchResult,
  PageSearchCriteria,
  PageStatus,
} from "../types/page-builder";

import { requireFields } from "@core/required-fields";

import { GROUPED_PAGE_FIELDS } from "../types/page-builder";

const PAGES_PATH = "/api/page-builder-pages";

export class PageBuilderClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async search(criteria: PageSearchCriteria): Promise<GroupedPage[]> {
    const response = await this.#httpClient.post(`${PAGES_PATH}/search`, { json: criteria });
    const { results } = response.expectOk().json<GroupedPageSearchResult>();
    return (results ?? []).map((page) => requireFields(page, GROUPED_PAGE_FIELDS, "Found page"));
  }

  async createGroupPage(request: CreateGroupedPageRequest): Promise<GroupedPage> {
    const response = await this.#httpClient.post(`${PAGES_PATH}/create-group-page`, { json: request });
    return requireFields(response.expectOk().json<GroupedPageData>(), GROUPED_PAGE_FIELDS, "Created page");
  }

  async setStatus(groupId: string, status: PageStatus): Promise<void> {
    switch (status) {
      case "Published":
      case "Draft":
        await this.#setPublished(groupId, status === "Published");
        return;
      case "Archived":
        (await this.#httpClient.post(`${PAGES_PATH}/grouped/archive`, { query: { ids: [groupId] } })).expectOk();
        return;
    }
  }

  async delete(groupId: string): Promise<void> {
    (await this.#httpClient.delete(`${PAGES_PATH}/grouped/${encodeURIComponent(groupId)}`)).expectOk();
  }

  async #setPublished(groupId: string, publish: boolean): Promise<void> {
    const path = `${PAGES_PATH}/grouped/publishing/${encodeURIComponent(groupId)}`;
    (await this.#httpClient.post(path, { query: { publish } })).expectOk();
  }
}
