import type { PageBuilderClient } from "@api/rest/clients/page-builder-client";
import type { GroupedPage } from "@api/rest/types/page-builder";
import type { CleanupStack } from "@core/cleanup-stack";
import type { PageDraft } from "../builders/page-builder";

export async function arrangePage(
  pageBuilderClient: PageBuilderClient,
  cleanupStack: CleanupStack,
  draft: PageDraft,
): Promise<GroupedPage> {
  const page = await pageBuilderClient.createGroupPage(draft);
  cleanupStack.push(`delete page ${page.name}`, () => pageBuilderClient.delete(page.id));
  return page;
}

export async function arrangePublishedPage(
  pageBuilderClient: PageBuilderClient,
  cleanupStack: CleanupStack,
  draft: PageDraft,
): Promise<GroupedPage> {
  const page = await arrangePage(pageBuilderClient, cleanupStack, draft);
  await pageBuilderClient.setStatus(page.id, "Published");
  return page;
}

export function registerPagesRemoval(
  pageBuilderClient: PageBuilderClient,
  cleanupStack: CleanupStack,
  storeId: string,
  nameToken: string,
): void {
  cleanupStack.push(`delete every page whose name contains ${nameToken}`, async () => {
    const pages = await pageBuilderClient.search({ storeId, keyword: nameToken, take: 100 });
    for (const page of pages.filter(({ name }) => name.includes(nameToken))) {
      await pageBuilderClient.delete(page.id);
    }
  });
}
