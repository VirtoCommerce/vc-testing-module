import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommerceContentModuleCoreModelContentFolder as ContentFolderData,
  VirtoCommerceContentModuleCoreModelContentItem as ContentItemData,
  VirtoCommerceContentModuleCoreModelContentStatistic as ContentStatisticData,
  VirtoCommerceContentModuleCoreModelMenuLink as MenuLink,
  VirtoCommerceContentModuleCoreModelMenuLinkList as MenuLinkListData,
} from "../generated/rest-api";

export type { ContentFolderData, ContentItemData, ContentStatisticData, MenuLink, MenuLinkListData };

export type ContentType = "pages" | "blogs" | "themes";

export const CONTENT_ITEM_FIELDS = ["name", "type", "url", "relativeUrl"] as const;
export const CONTENT_STATISTIC_FIELDS = ["pagesCount", "blogsCount", "themesCount"] as const;
export const MENU_LINK_LIST_FIELDS = ["id", "name", "storeId", "language"] as const;

export type ContentItem = WithRequired<ContentItemData, (typeof CONTENT_ITEM_FIELDS)[number]>;
export type ContentStatistic = WithRequired<ContentStatisticData, (typeof CONTENT_STATISTIC_FIELDS)[number]>;
export type MenuLinkList = WithRequired<MenuLinkListData, (typeof MENU_LINK_LIST_FIELDS)[number]>;
