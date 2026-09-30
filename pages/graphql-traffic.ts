import type { Response } from "@playwright/test";

interface GraphqlRequestBody {
  readonly operationName?: string;
  readonly query?: string;
}

export function isGraphqlOperation(operationName: string): (response: Response) => boolean {
  return (response) => graphqlBodies(response).some((body) => body.operationName === operationName);
}

export function isGraphqlMutation(fragment = ""): (response: Response) => boolean {
  const needle = fragment.toLowerCase();
  return (response) =>
    graphqlBodies(response).some((body) => {
      const query = body.query?.trimStart().toLowerCase();
      return query?.startsWith("mutation") === true && query.includes(needle);
    });
}

function graphqlBodies(response: Response): readonly GraphqlRequestBody[] {
  const request = response.request();
  if (request.method() !== "POST" || !request.url().includes("/graphql")) {
    return [];
  }
  try {
    const body: unknown = request.postDataJSON();
    return (Array.isArray(body) ? body : [body]).filter(isRequestBody);
  } catch {
    return [];
  }
}

function isRequestBody(value: unknown): value is GraphqlRequestBody {
  return typeof value === "object" && value !== null;
}
