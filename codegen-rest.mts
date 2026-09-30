import { resolve } from "node:path";

import { generateApi } from "swagger-typescript-api";

const SWAGGER_PATH = "/docs/PlatformUI/swagger.json";

const backendBaseUrl = process.env["BACKEND_BASE_URL"];
if (backendBaseUrl === undefined) {
  throw new Error("BACKEND_BASE_URL is not set");
}

await generateApi({
  url: new URL(SWAGGER_PATH, backendBaseUrl).href,
  output: resolve("api/rest/generated"),
  fileName: "rest-api.ts",
  generateClient: false,
  enumStyle: "union",
  addReadonly: true,
  sortTypes: true,
  silent: true,
});
