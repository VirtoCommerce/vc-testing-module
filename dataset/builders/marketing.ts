import type {
  ConditionTree,
  CouponData,
  DynamicContentConditionTree,
  DynamicContentPublicationData,
  PromotionData,
} from "@api/rest/types/marketing";
import type { WithRequired } from "@core/required-fields";

import { uniqueId } from "@core/unique-id";

interface BlockContentCondition extends ConditionTree {
  readonly all: boolean;
  readonly not: boolean;
}

interface AgeIsCondition extends ConditionTree {
  readonly compareCondition: "AtLeast";
  readonly value: number;
  readonly secondValue: number;
}

export function newPromotion(name = uniqueId("test-promotion")): PromotionData {
  return { name, isActive: false };
}

export type CouponDraft = WithRequired<CouponData, "code" | "promotionId">;

export function newCoupon(promotionId: string, maxUsesNumber: number, maxUsesPerUser: number): CouponDraft {
  return { promotionId, code: uniqueId("TEST-COUPON").toUpperCase(), maxUsesNumber, maxUsesPerUser };
}

export function newNamedContent(prefix: string): { name: string } {
  return { name: uniqueId(prefix) };
}

export function newInactivePublication(name = uniqueId("test-publication")): DynamicContentPublicationData {
  return { name, isActive: false };
}

export function ageConditionTree(minimumAge: number): DynamicContentConditionTree {
  const ageIs: AgeIsCondition = {
    id: "ConditionAgeIs",
    compareCondition: "AtLeast",
    value: minimumAge,
    secondValue: 0,
    availableChildren: [],
    children: [],
  };
  const block: BlockContentCondition = {
    id: "BlockContentCondition",
    all: false,
    not: false,
    availableChildren: [],
    children: [ageIs],
  };
  return { id: "DynamicContentConditionTree", all: true, not: false, availableChildren: [], children: [block] };
}
