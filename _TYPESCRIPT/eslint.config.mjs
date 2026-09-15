import tseslint from "typescript-eslint";
import playwright from "eslint-plugin-playwright";
import prettierConfig from "eslint-config-prettier";

export default tseslint.config(
  {
    ignores: [
      "node_modules/**",
      "test-results/**",
      "playwright-report/**",
      "blob-report/**",
      "src/api/graphql/generated/**",
    ],
  },
  {
    files: ["**/*.ts"],
    extends: [...tseslint.configs.recommendedTypeChecked, ...tseslint.configs.stylisticTypeChecked],
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      "@typescript-eslint/consistent-type-imports": [
        "error",
        { prefer: "type-imports", fixStyle: "separate-type-imports" },
      ],
      "@typescript-eslint/no-import-type-side-effects": "error",
      "no-useless-constructor": "off",
      "@typescript-eslint/no-useless-constructor": "error",
      "@typescript-eslint/no-restricted-imports": [
        "error",
        {
          paths: [
            {
              name: "@playwright/test",
              importNames: ["test"],
              message:
                "Import { test, expect } from '@fixtures/base' so custom fixtures (env) are available.",
            },
          ],
          patterns: [
            {
              group: ["../*", "../**"],
              message:
                "Use an alias (@config/*, @fixtures/*, @page-objects/*) instead of parent-relative imports. Same-directory './sibling' imports are fine.",
            },
          ],
        },
      ],
      "@typescript-eslint/explicit-function-return-type": [
        "error",
        { allowExpressions: false, allowTypedFunctionExpressions: true },
      ],
    },
  },
  {
    ...playwright.configs["flat/recommended"],
    files: ["tests/**/*.ts"],
  },
  {
    files: ["src/fixtures/*.ts"],
    rules: {
      "@typescript-eslint/no-restricted-imports": [
        "error",
        {
          patterns: [
            {
              group: ["../*", "../**"],
              message:
                "Use an alias (@config/*, @fixtures/*, @page-objects/*) instead of parent-relative imports. Same-directory './sibling' imports are fine.",
            },
          ],
        },
      ],
    },
  },
  prettierConfig,
);
