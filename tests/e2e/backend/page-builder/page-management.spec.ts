import * as allure from "allure-js-commons";

import { expect, test } from "@fixtures";
import { Column, DetailsToolbar, Route, Status } from "@pages/backend/page-builder/constants";
import { DISABLED_TOOLBAR_BUTTON } from "@pages/backend/shell/blade-toolbar";

import { arrangeDraftPage, DEFAULT_LANGUAGE, uiPageName } from "./page-builder-support";

const DESIGNER_APP = "page-builder-designer";

test.beforeEach(async () => {
  await allure.feature("Page Builder Shell / Page management (E2E)");
});

test.describe("page management (platform admin)", () => {
  test("create a draft page", async ({ pageBuilder, pageBuilderClient, cleanupStack, env }) => {
    const name = uiPageName(pageBuilderClient, cleanupStack, env.storeId);

    await test.step(`act: create ${name} from the draft list`, async () => {
      await pageBuilder.open(Route.draft);
      const details = await pageBuilder.addPage();
      await details.fill({ name, permalink: `/${name}` });
      await details.language.select(DEFAULT_LANGUAGE);
      await details.saveButton.click();
      await expect(pageBuilder.notifications.success.first()).toBeVisible();
    });

    await test.step("assert: the draft list shows the page with the entered values", async () => {
      const listing = await pageBuilder.waitUntilListed(Route.draft, name);
      const row = listing.pageRow(name);
      expect(await row.value(Column.permalink)).toBe(`/${name}`);
      expect(await row.value(Column.language)).toBe(DEFAULT_LANGUAGE);
      expect(await row.badges(Column.status)).toEqual([Status.draft]);
    });

    await test.step("assert: the draft counter matches the draft list", async () => {
      const { counter, total } = await pageBuilder.waitUntilCounterMatchesList(Route.draft);
      expect(counter).toBe(total);
    });
  });

  test("rename a page and change its permalink", async ({ pageBuilder, pageBuilderClient, cleanupStack, env }) => {
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);
    const renamed = `${page.name}-edited`;

    const modifiedBefore = await test.step(`arrange: open ${page.name}`, async () => {
      await pageBuilder.open(Route.draft);
      await pageBuilder.openPage(page.name);
      return pageBuilder.listBlade.pageRow(page.name).value(Column.modified);
    });

    await test.step(`act: rename to ${renamed} and save`, async () => {
      await pageBuilder.detailsBlade.fill({ name: renamed, permalink: `/${renamed}` });
      await pageBuilder.detailsBlade.saveButton.click();
      await expect(pageBuilder.notifications.success.first()).toBeVisible();
    });

    await test.step("assert: the blade keeps the new values", async () => {
      await expect(pageBuilder.detailsBlade.nameInput).toHaveValue(renamed);
      await expect(pageBuilder.detailsBlade.permalinkInput).toHaveValue(`/${renamed}`);
    });

    await test.step("assert: the list shows only the new name with a fresh modified date", async () => {
      expect(await (await pageBuilder.waitUntilListed(Route.draft, page.name, false)).hasPage(page.name)).toBe(false);
      const row = (await pageBuilder.waitUntilListed(Route.draft, renamed)).pageRow(renamed);
      expect(await row.value(Column.permalink)).toBe(`/${renamed}`);
      expect(await row.value(Column.modified)).not.toBe(modifiedBefore);
    });
  });

  test("open a page in the designer", async ({ pageBuilder, pageBuilderClient, cleanupStack, env }) => {
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);

    const details = await test.step(`arrange: open ${page.name}`, async () => {
      await pageBuilder.open(Route.draft);
      return pageBuilder.openPage(page.name);
    });
    const designerButton = details.toolbar.button(DetailsToolbar.openDesigner);
    await expect(designerButton).not.toHaveClass(DISABLED_TOOLBAR_BUTTON);

    const designer = await test.step("act: open the designer", async () => {
      const [popup] = await Promise.all([pageBuilder.page.context().waitForEvent("page"), designerButton.click()]);
      await popup.waitForLoadState("domcontentloaded");
      return popup;
    });

    await test.step("assert: the designer app opened in a new tab", async () => {
      expect(designer.url()).toContain(DESIGNER_APP);
      await designer.close();
    });
  });

  test("archive a draft page", async ({ pageBuilder, pageBuilderClient, cleanupStack, env }) => {
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);

    await test.step(`arrange: open ${page.name}`, async () => {
      await pageBuilder.open(Route.draft);
      await pageBuilder.openPage(page.name);
    });

    await test.step("act: archive the page and confirm", async () => {
      await pageBuilder.detailsBlade.toolbar.click(DetailsToolbar.archive);
      await expect(pageBuilder.popup.content).toContainText("archive");
      await pageBuilder.popup.confirm();
    });

    await test.step("assert: the page left the draft list for the archived list", async () => {
      expect(await (await pageBuilder.waitUntilListed(Route.draft, page.name, false)).hasPage(page.name)).toBe(false);
      const row = (await pageBuilder.waitUntilListed(Route.archived, page.name)).pageRow(page.name);
      expect(await row.badges(Column.status)).toEqual([Status.archived]);
    });
  });
});
