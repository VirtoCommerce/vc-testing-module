import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommercePageBuilderModuleCoreModelsCreateGroupedPageRequest as CreateGroupedPageRequest,
  VirtoCommercePageBuilderModuleCoreModelsGroupedPageBuilderPage as GroupedPageData,
  VirtoCommercePageBuilderModuleCoreModelsGroupedPageBuilderPageSearchResult as GroupedPageSearchResult,
  VirtoCommercePageBuilderModuleCoreModelsPageBuilderPageSearchCriteria as PageSearchCriteria,
} from "../generated/rest-api";

export type { CreateGroupedPageRequest, GroupedPageData, GroupedPageSearchResult, PageSearchCriteria };

export const GROUPED_PAGE_FIELDS = ["id", "name", "permalink"] as const;

export const PAGE_STATUSES = ["Draft", "Published", "Archived"] as const;

export type PageStatus = (typeof PAGE_STATUSES)[number];

export type GroupedPage = WithRequired<GroupedPageData, (typeof GROUPED_PAGE_FIELDS)[number]>;
