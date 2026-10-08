import type { HttpClient } from "../../http/http-client";
import type { HealthReport } from "../types/health";

import { HealthReportSchema } from "../types/health";

const HEALTH_PATH = "/health";

export class HealthClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async getReport(): Promise<HealthReport> {
    return (await this.#httpClient.get(HEALTH_PATH)).expectOk().parse(HealthReportSchema);
  }
}
