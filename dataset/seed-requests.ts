import type { DatasetItem } from "./dataset";
import type { ManifestEntry } from "./manifest";

import { fromEnv, fromPayloadItem, interpolate } from "@core/interpolate";
import { topologicalSort } from "@core/topological-sort";

export interface SeedRequest {
  readonly path: string;
  readonly body: unknown;
}

export function seedRequests(entry: ManifestEntry, items: readonly DatasetItem[]): SeedRequest[] {
  if (entry.payloadType === "array") {
    return [{ path: resolveEndpoint(entry.endpoint), body: items }];
  }
  const { parentRefField } = entry;
  const ordered = parentRefField === undefined ? items : topologicalSort(items, idOf, (item) => item[parentRefField]);
  return ordered.map((item) => ({
    path: resolveEndpoint(entry.endpoint, item),
    body: item,
  }));
}

function resolveEndpoint(endpoint: string, item?: DatasetItem): string {
  return interpolate(endpoint, { ENV: fromEnv, PAYLOAD_ITEM: fromPayloadItem(item) }, encodeURIComponent);
}

function idOf({ id }: DatasetItem): unknown {
  return id;
}
