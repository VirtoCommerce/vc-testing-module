import type { output } from "zod";

import { enum as enumOf, object, record, string } from "zod";

export const HEALTH_STATUSES = ["Healthy", "Degraded", "Unhealthy"] as const;

export const HealthReportSchema = record(
  string(),
  object({
    Status: enumOf(HEALTH_STATUSES),
    Description: string().nullable(),
  }),
);

export type HealthReport = output<typeof HealthReportSchema>;
