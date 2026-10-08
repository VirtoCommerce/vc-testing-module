import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommerceSearchModuleCoreModelIndexingOptions as IndexingOptions,
  VirtoCommerceSearchModuleCoreModelIndexProgressPushNotification as IndexProgressNotificationData,
  VirtoCommerceSearchModuleCoreModelIndexState as IndexStateData,
} from "../generated/rest-api";

export type { IndexingOptions, IndexProgressNotificationData, IndexStateData };

export const INDEX_STATE_FIELDS = ["provider", "scope", "documentType"] as const;
export const INDEX_PROGRESS_NOTIFICATION_FIELDS = ["id", "jobId"] as const;

export type IndexState = WithRequired<IndexStateData, (typeof INDEX_STATE_FIELDS)[number]>;
export type IndexProgressNotification = WithRequired<
  IndexProgressNotificationData,
  (typeof INDEX_PROGRESS_NOTIFICATION_FIELDS)[number]
>;

export type IndexedDocument = Readonly<Record<string, unknown>>;
