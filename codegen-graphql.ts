import type { CodegenConfig } from "@graphql-codegen/cli";

import { existsSync } from "node:fs";

import { getEnv } from "./core/env";

if (existsSync(".env")) {
  process.loadEnvFile();
}

const schema = new URL("/graphql", getEnv().backendBaseUrl).href;

const config: CodegenConfig = {
  schema,
  documents: ["api/graphql/fragments/**/*.graphql", "api/graphql/operations/**/*.graphql"],
  generates: {
    "api/graphql/generated/schema.graphql": {
      plugins: ["schema-ast"],
    },
    "api/graphql/generated/": {
      preset: "client",
      presetConfig: {
        fragmentMasking: false,
      },
      config: {
        documentMode: "string",
        enumsAsTypes: true,
        useTypeImports: true,
        strictScalars: true,
        scalars: {
          Date: "string",
          DateTime: "string",
          Decimal: "number",
          Long: "number",
          Seconds: "number",
          StoreAssetUrl: "string",
          OptionalDecimal: "number | null",
          OptionalNullableDecimal: "number | null",
          OptionalString: "string | null",
          DynamicPropertyValue: "unknown",
          PropertyValue: "unknown",
          ModuleSettingValue: "unknown",
        },
      },
    },
  },
  hooks: {
    afterAllFileWrite: ["biome check --write"],
  },
};

export default config;
