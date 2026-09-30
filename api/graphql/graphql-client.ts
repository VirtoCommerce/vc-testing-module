import type { DocumentTypeDecoration } from "@graphql-typed-document-node/core";
import type { HttpClient } from "../http/http-client";
import type { GraphqlErrorEntry } from "./graphql-error";

import { array, looseObject, unknown } from "zod";

import { GraphqlError, GraphqlErrorEntrySchema } from "./graphql-error";

export type GraphqlDocument<R, V> = DocumentTypeDecoration<R, V> & { toString(): string };

type VariablesArg<V> = Record<string, never> extends V ? [variables?: V] : [variables: V];

export interface GraphqlResult<R> {
  readonly operationName: string;
  readonly status: number;
  readonly data: R | null;
  readonly errors: readonly GraphqlErrorEntry[];
}

const GraphqlResponseSchema = looseObject({
  data: unknown().optional(),
  errors: array(GraphqlErrorEntrySchema).optional(),
});

const GRAPHQL_PATH = "/graphql";
const ANONYMOUS_OPERATION = "(anonymous)";
const OPERATION_NAME = /\b(?:query|mutation|subscription)\s+([A-Za-z_]\w*)/;

export class GraphqlClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async execute<R, V>(document: GraphqlDocument<R, V>, ...variables: VariablesArg<V>): Promise<R> {
    const result = await this.executeRaw(document, ...variables);
    if (result.errors.length > 0) {
      throw new GraphqlError(result.operationName, result.status, result.errors);
    }
    if (result.data === null) {
      throw new GraphqlError(result.operationName, result.status, [{ message: "response has no data" }]);
    }
    return result.data;
  }

  async executeRaw<R, V>(document: GraphqlDocument<R, V>, ...[variables]: VariablesArg<V>): Promise<GraphqlResult<R>> {
    const query = document.toString();
    const operationName = OPERATION_NAME.exec(query)?.[1] ?? ANONYMOUS_OPERATION;

    const response = await this.#httpClient.post(GRAPHQL_PATH, {
      json: { query, operationName, variables: variables ?? {} },
    });
    const body = response.parse(GraphqlResponseSchema);
    const errors = body.errors ?? [];

    if (!response.ok && errors.length === 0) {
      response.expectOk();
    }

    return { operationName, status: response.status, data: (body.data ?? null) as R | null, errors };
  }
}
