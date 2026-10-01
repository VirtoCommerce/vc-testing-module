import type { CreateGroupedPageRequest } from "@api/rest/types/page-builder";
import type { WithRequired } from "@core/required-fields";

import { uniqueId } from "@core/unique-id";

export const TEST_PAGE_PREFIX = "qa-page";

export type PageDraft = WithRequired<CreateGroupedPageRequest, "storeId" | "name" | "permalink" | "cultureName">;

export interface PageOptions {
  readonly name?: string;
  readonly cultureName: string;
  readonly texts?: readonly string[];
}

export function newPage(storeId: string, options: PageOptions): PageDraft {
  const name = options.name ?? uniqueId(TEST_PAGE_PREFIX);
  const permalink = `/${name}`;
  return {
    storeId,
    name,
    permalink,
    cultureName: options.cultureName,
    visibility: true,
    content: JSON.stringify({
      settings: { cultureName: options.cultureName, header: name, name, permalink, seoInfo: { pageTitle: name } },
      content: (options.texts ?? []).map((text, index) => ({
        id: `text-${index}`,
        heading: "h2",
        type: "text",
        text: { html: `<p>${text}</p>\n`, markdown: text },
      })),
    }),
  };
}
