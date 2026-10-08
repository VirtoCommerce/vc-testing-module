import type { HttpClient } from "../../http/http-client";
import type { Job, JobData } from "../types/jobs";

import { requireFields } from "@core/required-fields";

import { JOB_FIELDS } from "../types/jobs";

const JOBS_PATH = "/api/platform/jobs";

export class JobsClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async get(id: string): Promise<Job> {
    const response = await this.#httpClient.get(`${JOBS_PATH}/${encodeURIComponent(id)}`);
    return requireFields(response.expectOk().json<JobData>(), JOB_FIELDS, `Job "${id}"`);
  }
}
