import type { CompletenessChannelData } from "@api/rest/types/completeness";

import { uniqueId } from "@core/unique-id";

import { SEEDED_CATALOG_ID } from "./catalog";

export const DEFAULT_COMPLETENESS_EVALUATOR = "DefaultCompletenessEvaluator";

export function newCompletenessChannel(name = uniqueId("test-channel")): CompletenessChannelData {
  return {
    name,
    catalogId: SEEDED_CATALOG_ID,
    catalogName: SEEDED_CATALOG_ID,
    evaluatorType: DEFAULT_COMPLETENESS_EVALUATOR,
    languages: ["en-US"],
    currencies: ["USD"],
  };
}
