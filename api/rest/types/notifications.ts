import type {
  VirtoCommerceNotificationsModuleCoreModelNotificationMessage as NotificationMessageData,
  VirtoCommerceNotificationsModuleCoreModelSearchNotificationMessageSearchCriteria as NotificationMessageSearchCriteria,
} from "../generated/rest-api";

export type { NotificationMessageData, NotificationMessageSearchCriteria };

export type EmailNotificationMessage = NotificationMessageData & {
  readonly from?: string | null;
  readonly to?: string | null;
  readonly subject?: string | null;
  readonly body?: string | null;
};

export interface NotificationJournalPage {
  readonly totalCount?: number;
  readonly results?: EmailNotificationMessage[] | null;
}
