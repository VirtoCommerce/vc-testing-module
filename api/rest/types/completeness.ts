import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommerceCatalogPublishingModuleCoreModelCompletenessChannel as CompletenessChannelData,
  VirtoCommerceCatalogPublishingModuleCoreModelSearchCompletenessChannelSearchCriteria as CompletenessChannelSearchCriteria,
  VirtoCommerceCatalogPublishingModuleCoreModelSearchCompletenessChannelSearchResult as CompletenessChannelSearchResult,
  VirtoCommerceCatalogPublishingModuleCoreModelCompletenessEntry as CompletenessEntryData,
  VirtoCommerceCatalogPublishingModuleWebModelEvaluateCompletenessNotification as EvaluateCompletenessNotification,
} from "../generated/rest-api";

export type {
  CompletenessChannelData,
  CompletenessChannelSearchCriteria,
  CompletenessChannelSearchResult,
  CompletenessEntryData,
  EvaluateCompletenessNotification,
};

export const COMPLETENESS_CHANNEL_FIELDS = ["id", "name", "catalogId"] as const;
export const COMPLETENESS_ENTRY_FIELDS = ["channelId", "productId", "completenessPercent"] as const;

export type CompletenessChannel = WithRequired<CompletenessChannelData, (typeof COMPLETENESS_CHANNEL_FIELDS)[number]>;
export type CompletenessEntry = WithRequired<CompletenessEntryData, (typeof COMPLETENESS_ENTRY_FIELDS)[number]>;
