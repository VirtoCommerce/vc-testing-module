import { defineConfig } from "allure";

export default defineConfig({
  name: "VC testing module",
  output: "allure-report",
  plugins: {
    awesome: {
      options: {
        groupBy: ["parentSuite", "suite", "subSuite"],
      },
    },
  },
});
