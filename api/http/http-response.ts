import type { output, ZodType } from "zod";
import type { HttpMethod } from "./http-method";

import { prettifyError } from "zod";

import { HttpError } from "./http-error";

const MAX_BODY_LENGTH = 1_000;

export interface HttpResponseInit {
  readonly method: HttpMethod;
  readonly url: string;
  readonly status: number;
  readonly statusText: string;
  readonly headers: Readonly<Record<string, string>>;
  readonly text: string;
}

export class HttpResponse implements HttpResponseInit {
  readonly method: HttpMethod;
  readonly url: string;
  readonly status: number;
  readonly statusText: string;
  readonly headers: Readonly<Record<string, string>>;
  readonly text: string;

  constructor(init: HttpResponseInit) {
    this.method = init.method;
    this.url = init.url;
    this.status = init.status;
    this.statusText = init.statusText;
    this.headers = Object.fromEntries(Object.entries(init.headers).map(([name, value]) => [name.toLowerCase(), value]));
    this.text = init.text;
  }

  get ok(): boolean {
    return this.status >= 200 && this.status < 300;
  }

  header(name: string): string | undefined {
    return this.headers[name.toLowerCase()];
  }

  expectOk(): this {
    if (!this.ok) {
      throw this.#error();
    }
    return this;
  }

  json<T = unknown>(): T {
    try {
      return JSON.parse(this.text) as T;
    } catch (error) {
      throw this.#error("response body is not valid JSON", { cause: error });
    }
  }

  parse<S extends ZodType>(schema: S): output<S> {
    const result = schema.safeParse(this.json());
    if (!result.success) {
      throw this.#error(`unexpected response body:\n${prettifyError(result.error)}`, { cause: result.error });
    }
    return result.data;
  }

  #error(reason?: string, options?: ErrorOptions): HttpError {
    return new HttpError(this.#describe(reason), this.status, options);
  }

  #describe(reason?: string): string {
    const summary = `${this.method} ${this.url} → ${this.status} ${this.statusText}`.trimEnd();
    const body =
      this.text.length > MAX_BODY_LENGTH
        ? `${this.text.slice(0, MAX_BODY_LENGTH)}... (${this.text.length} chars)`
        : this.text;
    return [reason ? `${summary}: ${reason}` : summary, body].filter(Boolean).join("\n");
  }
}
