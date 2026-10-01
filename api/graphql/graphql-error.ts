import type { output } from "zod";

import { array, looseObject, number, record, string, union, unknown } from "zod";

export const GraphqlErrorEntrySchema = looseObject({
  message: string(),
  path: array(union([string(), number()])).optional(),
  extensions: record(string(), unknown()).optional(),
});

export type GraphqlErrorEntry = output<typeof GraphqlErrorEntrySchema>;

export class GraphqlError extends Error {
  override readonly name = "GraphqlError";
  readonly operationName: string;
  readonly status: number;
  readonly errors: readonly GraphqlErrorEntry[];

  constructor(operationName: string, status: number, errors: readonly GraphqlErrorEntry[]) {
    super(
      `GraphQL operation ${operationName} returned ${errors.length} error(s) with status ${status}:\n${errors.map(describe).join("\n")}`,
    );
    this.operationName = operationName;
    this.status = status;
    this.errors = errors;
  }
}

function describe(entry: GraphqlErrorEntry): string {
  const location = entry.path === undefined ? "" : ` (at ${entry.path.join(".")})`;
  return `  - ${entry.message}${location}`;
}
