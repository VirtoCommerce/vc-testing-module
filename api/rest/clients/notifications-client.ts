import type { HttpClient } from "../../http/http-client";
import type {
  EmailNotificationMessage,
  NotificationJournalPage,
  NotificationMessageSearchCriteria,
} from "../types/notifications";

const NOTIFICATION_JOURNAL_PATH = "/api/notifications/journal";

export class NotificationsClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async searchJournal(criteria: NotificationMessageSearchCriteria): Promise<EmailNotificationMessage[]> {
    const response = await this.#httpClient.post(NOTIFICATION_JOURNAL_PATH, { json: criteria });
    return response.expectOk().json<NotificationJournalPage>().results ?? [];
  }
}
