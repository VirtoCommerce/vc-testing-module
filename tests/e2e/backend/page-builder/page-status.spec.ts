import type { PageBuilderRoute } from "@pages/backend/page-builder/constants";
import type { PageBuilderShell } from "@pages/backend/page-builder/page-builder-shell";
import type { PageDetailsBlade } from "@pages/backend/page-builder/page-details-blade";

import * as allure from "allure-js-commons";

import { expect, test } from "@fixtures";
import { ALL_COLUMNS, Column, DetailsToolbar, Route, Status } from "@pages/backend/page-builder/constants";
import { DISABLED_TOOLBAR_BUTTON } from "@pages/backend/shell/blade-toolbar";

import { arrangeDraftPage } from "./page-builder-support";

const SAVE_TOAST = "Page saved successfully";
const NO_STATUS_TOAST =
  "PageBuilderModule shows a toast only for Save; publish, unpublish and archive raise no vc-notification.";
const TOAST_DISMISS_TIMEOUT_MS = 15_000;
const DAY_MS = 86_400_000;

test.beforeEach(async () => {
  await allure.feature("Page Builder Shell / Page status (E2E)");
});

test.describe("status filters (platform admin)", () => {
  test("the draft filter lists only drafts and its counter matches", async ({
    pageBuilder,
    pageBuilderClient,
    cleanupStack,
    env,
  }) => {
    await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);

    await test.step("act: open the draft list", () => pageBuilder.open(Route.draft));

    await test.step("assert: the grid has every column and only draft badges", async () => {
      for (const column of ALL_COLUMNS) {
        await expect(pageBuilder.listBlade.grid.columnHeader(column)).toBeVisible();
      }
      await expectOnlyStatus(pageBuilder, Status.draft);
    });
    await expectCounterMatchesList(pageBuilder, Route.draft);
  });

  test("the active filter lists only published pages and its counter matches", async ({
    pageBuilder,
    pageBuilderClient,
    cleanupStack,
    env,
  }) => {
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);
    await test.step(`arrange: publish ${page.name}`, () => pageBuilderClient.setStatus(page.id, "Published"));

    await test.step("act: open the active list", () => pageBuilder.open(Route.active));

    await test.step("assert: only published badges are listed", () => expectOnlyStatus(pageBuilder, Status.published));
    await expectCounterMatchesList(pageBuilder, Route.active);
  });

  test("the pending filter lists published pages with a future start date", async ({
    pageBuilder,
    pageBuilderClient,
    cleanupStack,
    env,
  }) => {
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);

    await test.step("arrange: schedule the page to start in a week and publish it", async () => {
      const details = await openFrom(pageBuilder, Route.draft, page.name);
      await details.schedulingSection.expand();
      await details.startDate.select(new Date(Date.now() + 7 * DAY_MS));
      await details.saveButton.click();
      await expect(pageBuilder.notifications.success.first()).toBeVisible();
      await expect(details.toolbar.button(DetailsToolbar.publish)).not.toHaveClass(DISABLED_TOOLBAR_BUTTON);
      await details.toolbar.click(DetailsToolbar.publish);
    });

    const listing = await test.step("act: open the pending list", () =>
      pageBuilder.waitUntilListed(Route.pending, page.name));

    await test.step("assert: the page is published and scheduled, and pending lists only published pages", async () => {
      expect(await listing.pageRow(page.name).badges(Column.status)).toEqual(
        expect.arrayContaining([Status.published, Status.scheduled]),
      );
      await expectOnlyStatus(pageBuilder, Status.published);
    });
  });

  test("the archived filter lists only archived pages", async ({
    pageBuilder,
    pageBuilderClient,
    cleanupStack,
    env,
  }) => {
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);
    await test.step(`arrange: archive ${page.name}`, async () => {
      await (await openFrom(pageBuilder, Route.draft, page.name)).archive();
    });

    const listing = await test.step("act: open the archived list", () =>
      pageBuilder.waitUntilListed(Route.archived, page.name));

    await test.step("assert: the page and every other row are archived", async () => {
      expect(await listing.pageRow(page.name).badges(Column.status)).toEqual([Status.archived]);
      await expectOnlyStatus(pageBuilder, Status.archived);
    });
  });
});

test.describe("status transitions (platform admin)", () => {
  test("publishing a draft moves it to the active list", async ({
    pageBuilder,
    pageBuilderClient,
    cleanupStack,
    env,
  }) => {
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);

    await test.step("act: publish the draft", () => publish(pageBuilder, page.name));

    await test.step("assert: the page left the draft list", async () => {
      expect(await (await pageBuilder.waitUntilListed(Route.draft, page.name, false)).hasPage(page.name)).toBe(false);
    });
    await test.step("assert: the page is listed as published", async () => {
      const row = (await pageBuilder.waitUntilListed(Route.active, page.name)).pageRow(page.name);
      expect(await row.badges(Column.status)).toEqual([Status.published]);
    });
    await expectCounterMatchesList(pageBuilder, Route.draft);
    await expectCounterMatchesList(pageBuilder, Route.active);
  });

  test("a published page can be archived", async ({ pageBuilder, pageBuilderClient, cleanupStack, env }) => {
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);
    await test.step(`arrange: publish ${page.name}`, () => pageBuilderClient.setStatus(page.id, "Published"));

    await test.step("act: archive the published page", async () => {
      await (await openFrom(pageBuilder, Route.active, page.name)).archive();
    });

    await test.step("assert: the page left the active list for the archived list", async () => {
      expect(await (await pageBuilder.waitUntilListed(Route.active, page.name, false)).hasPage(page.name)).toBe(false);
      const row = (await pageBuilder.waitUntilListed(Route.archived, page.name)).pageRow(page.name);
      expect(await row.badges(Column.status)).toEqual([Status.archived]);
    });
  });

  test("unpublishing returns a page to the draft list", async ({
    pageBuilder,
    pageBuilderClient,
    cleanupStack,
    env,
  }) => {
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);
    await test.step(`arrange: publish ${page.name}`, () => pageBuilderClient.setStatus(page.id, "Published"));

    await test.step("act: unpublish the page", async () => {
      const details = await openFrom(pageBuilder, Route.active, page.name);
      await expect(details.toolbar.button(DetailsToolbar.unpublish)).not.toHaveClass(DISABLED_TOOLBAR_BUTTON);
      await details.toolbar.click(DetailsToolbar.unpublish);
    });

    await test.step("assert: the page is a draft again and can be republished", async () => {
      expect(await (await pageBuilder.waitUntilListed(Route.active, page.name, false)).hasPage(page.name)).toBe(false);
      const row = (await pageBuilder.waitUntilListed(Route.draft, page.name)).pageRow(page.name);
      expect(await row.badges(Column.status)).toEqual([Status.draft]);
      const details = await pageBuilder.openPage(page.name);
      await expect(details.toolbar.button(DetailsToolbar.publish)).not.toHaveClass(DISABLED_TOOLBAR_BUTTON);
    });
  });
});

test.describe("user feedback (platform admin)", () => {
  test("saving a page shows a success toast and disables Save again", async ({
    pageBuilder,
    pageBuilderClient,
    cleanupStack,
    env,
  }) => {
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);
    const details = await openFrom(pageBuilder, Route.draft, page.name);

    await test.step("assert: Save is disabled until a field changes", async () => {
      await expect(details.saveButton).toHaveClass(DISABLED_TOOLBAR_BUTTON);
      await details.fill({ name: `${page.name}-toast` });
      await expect(details.saveButton).not.toHaveClass(DISABLED_TOOLBAR_BUTTON);
    });

    await test.step("act: save", () => details.saveButton.click());

    await test.step(`assert: "${SAVE_TOAST}" appears, Save is disabled and the toast goes away`, async () => {
      await expect(pageBuilder.notifications.successWith(SAVE_TOAST)).toBeVisible();
      await expect(details.saveButton).toHaveClass(DISABLED_TOOLBAR_BUTTON);
      await expect(pageBuilder.notifications.all).toHaveCount(0, { timeout: TOAST_DISMISS_TIMEOUT_MS });
    });
  });

  test("publishing a page shows a success toast", async ({ pageBuilder, pageBuilderClient, cleanupStack, env }) => {
    test.fail(true, NO_STATUS_TOAST);
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);

    await test.step("act: publish the draft", () => publish(pageBuilder, page.name));

    await test.step("assert: a published toast appears", async () => {
      await expect(pageBuilder.notifications.successWith("published")).toBeVisible();
    });
  });

  test("unpublishing a page shows a success toast", async ({ pageBuilder, pageBuilderClient, cleanupStack, env }) => {
    test.fail(true, NO_STATUS_TOAST);
    const page = await arrangeDraftPage(pageBuilderClient, cleanupStack, env.storeId);
    await test.step(`arrange: publish ${page.name}`, () => pageBuilderClient.setStatus(page.id, "Published"));

    await test.step("act: unpublish the page", async () => {
      await (await openFrom(pageBuilder, Route.active, page.name)).toolbar.click(DetailsToolbar.unpublish);
    });

    await test.step("assert: an unpublished toast appears", async () => {
      await expect(pageBuilder.notifications.successWith("unpublished")).toBeVisible();
    });
  });
});

async function openFrom(
  pageBuilder: PageBuilderShell,
  route: PageBuilderRoute,
  name: string,
): Promise<PageDetailsBlade> {
  await pageBuilder.open(route);
  return pageBuilder.openPage(name);
}

async function publish(pageBuilder: PageBuilderShell, name: string): Promise<void> {
  const details = await openFrom(pageBuilder, Route.draft, name);
  await expect(details.toolbar.button(DetailsToolbar.publish)).not.toHaveClass(DISABLED_TOOLBAR_BUTTON);
  await details.toolbar.click(DetailsToolbar.publish);
  await pageBuilder.page.waitForLoadState("networkidle");
}

async function expectOnlyStatus(pageBuilder: PageBuilderShell, status: string): Promise<void> {
  const statuses = await pageBuilder.listBlade.statuses();
  expect(statuses.length).toBeGreaterThan(0);
  expect(statuses.filter((value) => !value.includes(status))).toEqual([]);
}

async function expectCounterMatchesList(pageBuilder: PageBuilderShell, route: PageBuilderRoute): Promise<void> {
  await test.step(`assert: the ${route} counter matches the list total`, async () => {
    const { counter, total } = await pageBuilder.waitUntilCounterMatchesList(route);
    expect(counter).toBe(total);
  });
}
