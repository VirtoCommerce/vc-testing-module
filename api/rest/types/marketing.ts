import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommerceCoreModuleCoreConditionsIConditionTree as ConditionTree,
  VirtoCommerceMarketingModuleCoreModelPromotionsCoupon as CouponData,
  VirtoCommerceMarketingModuleCoreModelPromotionsSearchCouponSearchCriteria as CouponSearchCriteria,
  VirtoCommerceMarketingModuleCoreModelPromotionsSearchCouponSearchResult as CouponSearchResult,
  VirtoCommerceMarketingModuleCoreModelDynamicContentDynamicContentConditionTree as DynamicContentConditionTree,
  VirtoCommerceMarketingModuleCoreModelDynamicContentFolder as DynamicContentFolderData,
  VirtoCommerceMarketingModuleCoreModelDynamicContentItem as DynamicContentItemData,
  VirtoCommerceMarketingModuleCoreModelDynamicContentItemSearchCriteria as DynamicContentItemSearchCriteria,
  VirtoCommerceMarketingModuleCoreModelDynamicContentSearchDynamicContentItemSearchResult as DynamicContentItemSearchResult,
  VirtoCommerceMarketingModuleCoreModelDynamicContentPlace as DynamicContentPlaceData,
  VirtoCommerceMarketingModuleCoreModelDynamicContentPlaceSearchCriteria as DynamicContentPlaceSearchCriteria,
  VirtoCommerceMarketingModuleCoreModelDynamicContentSearchDynamicContentPlaceSearchResult as DynamicContentPlaceSearchResult,
  VirtoCommerceMarketingModuleCoreModelDynamicContentPublication as DynamicContentPublicationData,
  VirtoCommerceMarketingModuleCoreModelDynamicContentPublicationSearchCriteria as DynamicContentPublicationSearchCriteria,
  VirtoCommerceMarketingModuleCoreModelDynamicContentSearchDynamicContentPublicationSearchResult as DynamicContentPublicationSearchResult,
  VirtoCommerceMarketingModuleCoreModelPromotionsPromotion as PromotionData,
  VirtoCommerceMarketingModuleCoreModelPromotionsSearchPromotionSearchCriteria as PromotionSearchCriteria,
  VirtoCommerceMarketingModuleCoreModelPromotionsSearchPromotionSearchResult as PromotionSearchResult,
} from "../generated/rest-api";

export type {
  ConditionTree,
  CouponData,
  CouponSearchCriteria,
  CouponSearchResult,
  DynamicContentConditionTree,
  DynamicContentFolderData,
  DynamicContentItemData,
  DynamicContentItemSearchCriteria,
  DynamicContentItemSearchResult,
  DynamicContentPlaceData,
  DynamicContentPlaceSearchCriteria,
  DynamicContentPlaceSearchResult,
  DynamicContentPublicationData,
  DynamicContentPublicationSearchCriteria,
  DynamicContentPublicationSearchResult,
  PromotionData,
  PromotionSearchCriteria,
  PromotionSearchResult,
};

export const PROMOTION_FIELDS = ["id", "name"] as const;
export const COUPON_FIELDS = ["id", "code", "promotionId"] as const;

export type Promotion = WithRequired<PromotionData, (typeof PROMOTION_FIELDS)[number]>;
export type Coupon = WithRequired<CouponData, (typeof COUPON_FIELDS)[number]>;

export interface NamedEntityData {
  id?: string | null;
  name?: string | null;
}

export type NamedEntity<Data extends NamedEntityData> = WithRequired<Data, "id" | "name">;
