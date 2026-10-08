import type { HttpClient } from "../../http/http-client";
import type {
  DynamicContentFolderData,
  DynamicContentItemData,
  DynamicContentItemSearchCriteria,
  DynamicContentPlaceData,
  DynamicContentPlaceSearchCriteria,
  DynamicContentPublicationData,
  DynamicContentPublicationSearchCriteria,
  NamedEntity,
  NamedEntityData,
} from "../types/marketing";

import { requireFields } from "@core/required-fields";

const NAMED_ENTITY_FIELDS = ["id", "name"] as const;

export class DynamicContentResource<Data extends NamedEntityData> {
  protected readonly httpClient: HttpClient;
  protected readonly path: string;
  protected readonly label: string;

  constructor(httpClient: HttpClient, path: string, label: string) {
    this.httpClient = httpClient;
    this.path = path;
    this.label = label;
  }

  async get(id: string): Promise<NamedEntity<Data>> {
    return requireFields(await this.find(id), NAMED_ENTITY_FIELDS, `${this.label} "${id}"`);
  }

  async find(id: string): Promise<NamedEntity<Data> | undefined> {
    const response = await this.httpClient.get(`${this.path}/${encodeURIComponent(id)}`);
    if (response.status === 404) {
      return undefined;
    }
    return requireFields(response.expectOk().json<Data>(), NAMED_ENTITY_FIELDS, `${this.label} "${id}"`);
  }

  async create(entity: Data): Promise<NamedEntity<Data>> {
    const response = await this.httpClient.post(this.path, { json: entity });
    return requireFields(response.expectOk().json<Data>(), NAMED_ENTITY_FIELDS, `Created ${this.label}`);
  }

  async update(entity: Data): Promise<void> {
    (await this.httpClient.put(this.path, { json: entity })).expectOk();
  }

  async delete(ids: readonly string[]): Promise<void> {
    (await this.httpClient.delete(this.path, { query: { ids } })).expectOk();
  }
}

export class SearchableDynamicContentResource<
  Data extends NamedEntityData,
  Criteria,
> extends DynamicContentResource<Data> {
  async search(criteria: Criteria): Promise<NamedEntity<Data>[]> {
    const response = await this.httpClient.post(`${this.path}/search`, { json: criteria });
    const { results } = response.expectOk().json<{ results?: Data[] | null }>();
    return (results ?? []).map((entity) => requireFields(entity, NAMED_ENTITY_FIELDS, `Found ${this.label}`));
  }
}

export class DynamicContentClient {
  readonly folders: DynamicContentResource<DynamicContentFolderData>;
  readonly items: SearchableDynamicContentResource<DynamicContentItemData, DynamicContentItemSearchCriteria>;
  readonly places: SearchableDynamicContentResource<DynamicContentPlaceData, DynamicContentPlaceSearchCriteria>;
  readonly publications: SearchableDynamicContentResource<
    DynamicContentPublicationData,
    DynamicContentPublicationSearchCriteria
  >;
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
    this.folders = new DynamicContentResource(httpClient, "/api/marketing/contentfolders", "Content folder");
    this.items = new SearchableDynamicContentResource(httpClient, "/api/marketing/contentitems", "Content item");
    this.places = new SearchableDynamicContentResource(httpClient, "/api/marketing/contentplaces", "Content place");
    this.publications = new SearchableDynamicContentResource(
      httpClient,
      "/api/marketing/contentpublications",
      "Content publication",
    );
  }

  async newPublication(): Promise<DynamicContentPublicationData> {
    const response = await this.#httpClient.get("/api/marketing/contentpublications/new");
    return response.expectOk().json<DynamicContentPublicationData>();
  }
}
