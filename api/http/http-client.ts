import type { APIRequestContext } from "@playwright/test";
import type { HttpMethod } from "./http-method";

import { HttpResponse } from "./http-response";

export type QueryValue = string | number | boolean;
export type QueryParams = Readonly<Record<string, QueryValue | readonly QueryValue[] | undefined>>;
export type HttpHeaders = Readonly<Record<string, string>>;
export type HeadersSource = HttpHeaders | (() => Promise<HttpHeaders>);

const JSON_CONTENT_TYPE: HttpHeaders = { "Content-Type": "application/json" };

export interface MultipartFile {
  readonly name: string;
  readonly mimeType: string;
  readonly buffer: Buffer;
}

export interface RequestOptions {
  readonly query?: QueryParams;
  readonly headers?: HttpHeaders;
  readonly json?: unknown;
  readonly form?: Readonly<Record<string, string>>;
  readonly multipart?: Readonly<Record<string, string | MultipartFile>>;
  readonly timeoutMs?: number;
}

export class HttpClient {
  readonly #context: APIRequestContext;
  readonly #headersSources: readonly HeadersSource[];

  constructor(context: APIRequestContext, headersSources: readonly HeadersSource[] = []) {
    this.#context = context;
    this.#headersSources = headersSources;
  }

  withHeaders(source: HeadersSource): HttpClient {
    return new HttpClient(this.#context, [...this.#headersSources, source]);
  }

  get(path: string, options?: RequestOptions): Promise<HttpResponse> {
    return this.send("GET", path, options);
  }

  post(path: string, options?: RequestOptions): Promise<HttpResponse> {
    return this.send("POST", path, options);
  }

  put(path: string, options?: RequestOptions): Promise<HttpResponse> {
    return this.send("PUT", path, options);
  }

  patch(path: string, options?: RequestOptions): Promise<HttpResponse> {
    return this.send("PATCH", path, options);
  }

  delete(path: string, options?: RequestOptions): Promise<HttpResponse> {
    return this.send("DELETE", path, options);
  }

  async send(method: HttpMethod, path: string, options: RequestOptions = {}): Promise<HttpResponse> {
    const response = await this.#context.fetch(path, {
      method,
      params: toSearchParams(options.query ?? {}),
      headers: {
        ...(await this.#resolveHeaders()),
        ...(options.json === undefined ? {} : JSON_CONTENT_TYPE),
        ...options.headers,
      },
      ...(options.json === undefined ? {} : { data: JSON.stringify(options.json) }),
      ...(options.form === undefined ? {} : { form: options.form }),
      ...(options.multipart === undefined ? {} : { multipart: { ...options.multipart } }),
      ...(options.timeoutMs === undefined ? {} : { timeout: options.timeoutMs }),
      failOnStatusCode: false,
    });

    try {
      return new HttpResponse({
        method,
        url: response.url(),
        status: response.status(),
        statusText: response.statusText(),
        headers: response.headers(),
        text: await response.text(),
      });
    } finally {
      await response.dispose();
    }
  }

  async #resolveHeaders(): Promise<HttpHeaders> {
    const resolved = await Promise.all(
      this.#headersSources.map((source) => (typeof source === "function" ? source() : source)),
    );
    return Object.assign({}, ...resolved);
  }
}

function toSearchParams(query: QueryParams): URLSearchParams {
  const params = new URLSearchParams();
  for (const [name, value] of Object.entries(query)) {
    for (const item of value === undefined ? [] : [value].flat()) {
      params.append(name, String(item));
    }
  }
  return params;
}
