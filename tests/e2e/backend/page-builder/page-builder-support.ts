import type { PageBuilderClient } from "@api/rest/clients/page-builder-client";
import type { GroupedPage } from "@api/rest/types/page-builder";
import type { CleanupStack } from "@core/cleanup-stack";

import { uniqueId } from "@core/unique-id";
import { arrangePage, registerPagesRemoval } from "@dataset/arrange/page-builder";
import { newPage, TEST_PAGE_PREFIX } from "@dataset/builders/page-builder";
import { test } from "@fixtures";

export const DEFAULT_LANGUAGE = "en-US";

export function arrangeDraftPage(
  pageBuilderClient: PageBuilderClient,
  cleanupStack: CleanupStack,
  storeId: string,
  name = uniqueId(TEST_PAGE_PREFIX),
): Promise<GroupedPage> {
  return test.step(`arrange: draft page ${name}`, () =>
    arrangePage(pageBuilderClient, cleanupStack, newPage(storeId, { name, cultureName: DEFAULT_LANGUAGE })));
}

export function uiPageName(
  pageBuilderClient: PageBuilderClient,
  cleanupStack: CleanupStack,
  storeId: string,
  prefix = TEST_PAGE_PREFIX,
): string {
  const name = uniqueId(prefix);
  registerPagesRemoval(pageBuilderClient, cleanupStack, storeId, name);
  return name;
}
