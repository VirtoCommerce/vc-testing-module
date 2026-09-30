import type { ManifestItem, ManifestItemName } from "./manifest";

import { MANIFEST_ITEMS } from "./manifest";

export interface SeedScope {
  readonly entities: readonly ManifestItem[];
  readonly skipped: readonly ManifestItem[];
}

export function resolveSeedScope(
  installedModuleIds: ReadonlySet<string>,
  only: readonly ManifestItemName[] | undefined,
): SeedScope {
  const selected = only === undefined ? MANIFEST_ITEMS : MANIFEST_ITEMS.filter((item) => only.includes(item.name));
  return {
    entities: selected.filter((entity) => installedModuleIds.has(entity.moduleId)),
    skipped: selected.filter((entity) => !installedModuleIds.has(entity.moduleId)),
  };
}

export function parseSeedOnly(value: string | undefined): readonly ManifestItemName[] | undefined {
  const names = (value ?? "")
    .split(",")
    .map((name) => name.trim())
    .filter((name) => name !== "");
  if (names.length === 0) {
    return undefined;
  }
  const knownNames: readonly string[] = MANIFEST_ITEMS.map((item) => item.name);
  const unknownNames = names.filter((name) => !knownNames.includes(name));
  if (unknownNames.length > 0) {
    throw new Error(`Unknown entities: ${unknownNames.join(", ")}. Known entities: ${knownNames.join(", ")}`);
  }
  return names as ManifestItemName[];
}
