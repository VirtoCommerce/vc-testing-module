import * as allure from "allure-js-commons";

import { expect, test } from "@fixtures";
import { ALL_COLUMNS, Route } from "@pages/backend/page-builder/constants";

import { arrangeDraftPage, DEFAULT_LANGUAGE } from "./page-builder-support";

test.beforeEach(async () => {
  await allure.feature("Page Builder Shell / Smoke (E2E)");
});

test.describe("page builder shell (platform admin)", () => {
  test("the shell loads with the grid and a readable details blade", async ({
    pageBuilder,
    pageBuilderClient,
    cleanupStack,
    env,
  }) => {
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);

    await test.step("act: open every page", () => pageBuilder.open(Route.all));

    await test.step("assert: the grid shows the documented columns", async () => {
      for (const column of ALL_COLUMNS) {
        await expect(pageBuilder.listBlade.grid.columnHeader(column)).toBeVisible();
      }
      await expect(pageBuilder.listBlade.grid.rows.first()).toBeVisible();
    });

    const details = await test.step(`act: open ${page.name}`, () => pageBuilder.openPage(page.name));

    await test.step("assert: the details blade shows the page", async () => {
      await expect(details.nameInput).toHaveValue(page.name);
      await expect(details.permalinkInput).toHaveValue(page.permalink);
      expect(await details.language.value()).toBe(DEFAULT_LANGUAGE);
    });

    await test.step("assert: collapsible sections expand and their selects offer options", async () => {
      await details.personalizationSection.expand();
      expect(await details.personalizationSection.isExpanded()).toBe(true);
      expect(await details.organization.optionTexts()).not.toEqual([]);
      await details.schedulingSection.expand();
      await expect(details.startDate.input).toBeVisible();
    });
  });

  test("the details blade shows the frontend URL next to the permalink", async ({
    pageBuilder,
    pageBuilderClient,
    cleanupStack,
    env,
  }) => {
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);

    const details = await test.step(`act: open ${page.name}`, async () => {
      await pageBuilder.open(Route.draft);
      return pageBuilder.openPage(page.name);
    });

    await test.step("assert: the permalink prefix is the frontend origin", async () => {
      await expect(details.permalinkPrefix).toBeVisible();
      const prefix = (await details.permalinkPrefix.innerText()).trim();
      expect(new URL(prefix).hostname).toBe(new URL(env.frontendBaseUrl).hostname);
      await expect(details.permalinkInput).toHaveValue(page.permalink);
    });
  });

  test("the shell shows the signed-in user, their role and the logo", async ({ pageBuilder, env }) => {
    await test.step("act: open the shell", () => pageBuilder.open(Route.all));

    await test.step("assert: the profile shows the platform admin as Administrator", async () => {
      await expect(pageBuilder.userName).toHaveText(env.admin.username);
      await expect(pageBuilder.userRole).toHaveText("Administrator");
    });

    await test.step("assert: the logo is displayed", async () => {
      await expect(pageBuilder.logo).toBeVisible();
      await expect(pageBuilder.logo).toHaveAttribute("alt", "logo");
    });
  });
});
