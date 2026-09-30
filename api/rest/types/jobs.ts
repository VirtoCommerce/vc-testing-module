import type { WithRequired } from "@core/required-fields";
import type { VirtoCommercePlatformCoreJobsJob as JobData } from "../generated/rest-api";

export type { JobData };

export const JOB_FIELDS = ["id", "state", "completed"] as const;

export type Job = WithRequired<JobData, (typeof JOB_FIELDS)[number]>;
