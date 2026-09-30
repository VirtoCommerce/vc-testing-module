import * as allure from "allure-js-commons";

import { expect, test } from "@fixtures";
import { Column, Route } from "@pages/backend/page-builder/constants";
import { DISABLED_TOOLBAR_BUTTON } from "@pages/backend/shell/blade-toolbar";

import { arrangeDraftPage, DEFAULT_LANGUAGE, uiPageName } from "./page-builder-support";

const SEARCH_MARKER = "searchable";
const NO_MATCH = "&";
const SEEDED_PAGE = "our-team";
const SORT_WINDOW_BUG =
  "POST /api/page-builder-pages/search applies the keyword only to the sorted page window (default sort " +
  "modifiedDate:DESC, take 20), so search misses pages outside the newest 20.";
const EXISTING_PERMALINK_SOURCE = "qa-dup-source";
const DUPLICATE_ACCEPTED =
  "PageBuilderModule accepts a second page with an existing permalink in the same language without an error.";
const PERMALINK_STORED_VERBATIM =
  "PageBuilderModule stores the permalink verbatim: it is neither sanitised nor rejected.";
const SPECIAL_PERMALINKS = [
  { title: "spaces", permalink: "/my page test", knownIssue: PERMALINK_STORED_VERBATIM },
  { title: "reserved characters", permalink: "/page&test?q=1#anchor", knownIssue: PERMALINK_STORED_VERBATIM },
  { title: "unicode letters", permalink: "/страница-тест", knownIssue: undefined },
] as const;

test.beforeEach(async () => {
  await allure.feature("Page Builder Shell / Search and validation (E2E)");
});

test.describe("page search (platform admin)", () => {
  test("search matches part of the name and ignores case", async ({
    pageBuilder,
    pageBuilderClient,
    cleanupStack,
    env,
  }) => {
    const page = await arrangeDraftPage(
      pageBuilderClient,
      cleanupStack,
      env.storeId,
      uiPageName(pageBuilderClient, cleanupStack, env.storeId, `qa-${SEARCH_MARKER}`),
    );
    const listing = pageBuilder.listBlade;
    const rows = listing.pageRows(page.name);
    await test.step("arrange: open every page", () => pageBuilder.open(Route.all));

    const lowerCaseNames = await test.step(`act and assert: "${SEARCH_MARKER}" finds the page`, async () => {
      await listing.search(SEARCH_MARKER);
      await expect(rows).toHaveCount(1);
      return listing.names();
    });

    await test.step(`act and assert: "${SEARCH_MARKER.toUpperCase()}" returns the same pages`, async () => {
      await listing.search(SEARCH_MARKER.toUpperCase());
      await expect(rows).toHaveCount(1);
      expect(await listing.names()).toEqual(lowerCaseNames);
    });

    await test.step(`act and assert: "${NO_MATCH}" excludes the page without an error`, async () => {
      await listing.search(NO_MATCH);
      await expect(rows).toHaveCount(0);
      await expect(pageBuilder.notifications.error).toHaveCount(0);
    });

    await test.step("act and assert: clearing the search lists the page again", async () => {
      await listing.clearSearch();
      await expect(rows).toHaveCount(1);
    });
  });

  test("search finds a page beyond the first page of the default sort", async ({ pageBuilder }) => {
    await test.step("arrange: open every page", () => pageBuilder.open(Route.all));
    const pagination = await pageBuilder.listBlade.grid.paginationInfo();
    test.skip(
      pagination === undefined || pagination.total <= pagination.last,
      "The store has a single page of results, so the defect cannot show",
    );
    test.fail(true, SORT_WINDOW_BUG);

    await test.step(`act: search for "${SEEDED_PAGE}"`, () => pageBuilder.listBlade.search(SEEDED_PAGE));

    await test.step(`assert: ${SEEDED_PAGE} is found`, async () => {
      await expect(pageBuilder.listBlade.pageRows(SEEDED_PAGE)).toHaveCount(1);
    });
  });
});

test.describe("page validation (platform admin)", () => {
  test("Save stays disabled until both required fields are filled", async ({ pageBuilder }) => {
    const details = await test.step("arrange: start a new page", async () => {
      await pageBuilder.open(Route.draft);
      return pageBuilder.addPage();
    });

    for (const [fields, enabled] of [
      [{}, false],
      [{ name: "qa-missing-permalink" }, false],
      [{ name: "", permalink: "/qa-missing-name" }, false],
      [{ name: "qa-both-fields" }, true],
    ] as const) {
      await test.step(`act and assert: with ${JSON.stringify(fields)} Save is ${enabled ? "enabled" : "disabled"}`, async () => {
        await details.fill(fields);
        if (enabled) {
          await expect(details.saveButton).not.toHaveClass(DISABLED_TOOLBAR_BUTTON);
        } else {
          await expect(details.saveButton).toHaveClass(DISABLED_TOOLBAR_BUTTON);
        }
      });
    }
  });

  test("a duplicate permalink is rejected", async ({ pageBuilder, pageBuilderClient, cleanupStack, env }) => {
    test.fail(true, DUPLICATE_ACCEPTED);
    const existing = await arrangeDraftPage(
      pageBuilderClient,
      cleanupStack,
      env.storeId,
      uiPageName(pageBuilderClient, cleanupStack, env.storeId, EXISTING_PERMALINK_SOURCE),
    );
    const name = uiPageName(pageBuilderClient, cleanupStack, env.storeId, "qa-dup");

    await test.step(`act: create ${name} with the permalink ${existing.permalink}`, async () => {
      await pageBuilder.open(Route.draft);
      const details = await pageBuilder.addPage();
      await details.fill({ name, permalink: existing.permalink });
      await details.language.select(DEFAULT_LANGUAGE);
      await details.saveButton.click();
      await pageBuilder.page.waitForLoadState("networkidle");
    });

    await test.step("assert: an error is shown or the page is not created", async () => {
      const errored = (await pageBuilder.notifications.error.count()) > 0;
      const created = await (await pageBuilder.waitUntilListed(Route.draft, name)).hasPage(name);
      expect(errored || !created).toBe(true);
    });
  });

  for (const { title, permalink, knownIssue } of SPECIAL_PERMALINKS) {
    test(`a permalink with ${title} is sanitised or rejected`, async ({
      pageBuilder,
      pageBuilderClient,
      cleanupStack,
      env,
    }) => {
      test.fail(knownIssue !== undefined, knownIssue);
      const name = uiPageName(pageBuilderClient, cleanupStack, env.storeId, "qa-chars");

      await test.step(`act: create ${name} with the permalink "${permalink}"`, async () => {
        await pageBuilder.open(Route.draft);
        const details = await pageBuilder.addPage();
        await details.fill({ name, permalink });
        await details.language.select(DEFAULT_LANGUAGE);
        await details.saveButton.click();
        await pageBuilder.page.waitForLoadState("networkidle");
      });

      await test.step("assert: no server error is shown", async () => {
        await expect(pageBuilder.notifications.error).toHaveCount(0);
      });

      await test.step("assert: a stored permalink has no spaces, query or fragment", async () => {
        const listing = await pageBuilder.waitUntilListed(Route.draft, name);
        if (await listing.hasPage(name)) {
          const stored = await listing.pageRow(name).value(Column.permalink);
          expect(stored).not.toMatch(/[\s?#]/);
        }
      });
    });
  }
});
