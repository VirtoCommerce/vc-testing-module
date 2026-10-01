import type { HttpClient } from "../../http/http-client";
import type {
  OutlineSyncNotification,
  TaggedEntity,
  TaggedItem,
  TaggedItemData,
  TaggedItemSearchCriteria,
  TaggedItemSearchResult,
} from "../types/personalization";

import { requireFields } from "@core/required-fields";

import { TAGGED_ITEM_FIELDS } from "../types/personalization";

const PERSONALIZATION_PATH = "/api/personalization";
const TAGGED_ITEM_PATH = `${PERSONALIZATION_PATH}/taggeditem`;

export class PersonalizationClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async getTaggedItem(entityId: string): Promise<TaggedItem> {
    const response = await this.#httpClient.get(`${TAGGED_ITEM_PATH}/${encodeURIComponent(entityId)}`);
    return requireFields(response.expectOk().json<TaggedItemData>(), TAGGED_ITEM_FIELDS, `Tagged item "${entityId}"`);
  }

  async countTags(entityId: string): Promise<number> {
    const response = await this.#httpClient.get(`${TAGGED_ITEM_PATH}/${encodeURIComponent(entityId)}/tags/count`);
    return response.expectOk().json<number>();
  }

  async search(criteria: TaggedItemSearchCriteria): Promise<TaggedItem[]> {
    const response = await this.#httpClient.post(`${PERSONALIZATION_PATH}/search`, { json: criteria });
    const { results } = response.expectOk().json<TaggedItemSearchResult>();
    return (results ?? []).map((item) => requireFields(item, TAGGED_ITEM_FIELDS, "Found tagged item"));
  }

  async setTags(entity: TaggedEntity, tags: string[]): Promise<void> {
    const [existing] = await this.search({ entityIds: [entity.entityId] });
    const item: TaggedItemData = { ...entity, id: existing?.id ?? null, tags };
    (await this.#httpClient.put(TAGGED_ITEM_PATH, { json: item })).expectOk();
  }

  async synchronizeOutlines(): Promise<OutlineSyncNotification> {
    const response = await this.#httpClient.post(`${PERSONALIZATION_PATH}/outlines/synchronize`, { json: {} });
    return response.expectOk().json<OutlineSyncNotification>();
  }
}
