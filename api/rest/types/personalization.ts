import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommerceCatalogPersonalizationModuleCoreModelTaggedItemOutlineSyncPushNotification as OutlineSyncNotification,
  VirtoCommerceCatalogPersonalizationModuleCoreModelTaggedItem as TaggedItemData,
  VirtoCommerceCatalogPersonalizationModuleCoreModelSearchTaggedItemSearchCriteria as TaggedItemSearchCriteria,
  VirtoCommerceCatalogPersonalizationModuleCoreModelSearchTaggedItemSearchResult as TaggedItemSearchResult,
} from "../generated/rest-api";

export type { OutlineSyncNotification, TaggedItemData, TaggedItemSearchCriteria, TaggedItemSearchResult };

export const TAGGED_ITEM_FIELDS = ["entityId", "tags"] as const;

export type TaggedItem = WithRequired<TaggedItemData, (typeof TAGGED_ITEM_FIELDS)[number]>;

export type TaggedEntityType = "Product" | "Category";

export interface TaggedEntity {
  readonly entityId: string;
  readonly entityType: TaggedEntityType;
  readonly label: string;
}
