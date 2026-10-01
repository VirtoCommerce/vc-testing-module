import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommerceCustomerModuleCoreModelLockMembershipRequest as LockMembershipRequest,
  VirtoCommerceCustomerModuleCoreModelOrganizationMembership as OrganizationMembershipData,
} from "../generated/rest-api";

export type { LockMembershipRequest, OrganizationMembershipData };

export const ORGANIZATION_MEMBERSHIP_FIELDS = ["id", "userId", "organizationId"] as const;

export type OrganizationMembership = WithRequired<
  OrganizationMembershipData,
  (typeof ORGANIZATION_MEMBERSHIP_FIELDS)[number]
>;
