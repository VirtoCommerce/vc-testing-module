import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommerceCustomerModuleCoreModelContact as ContactData,
  CustomerAddress,
  VirtoCommerceCustomerModuleCoreModelEmployee as EmployeeData,
  VirtoCommerceCustomerModuleCoreModelMember as MemberData,
  VirtoCommerceCustomerModuleCoreModelSearchMemberSearchResult as MemberSearchResult,
  VirtoCommerceCustomerModuleCoreModelSearchMembersSearchCriteria as MembersSearchCriteria,
  VirtoCommerceCustomerModuleCoreModelOrganization as OrganizationData,
  VirtoCommerceCustomerModuleCoreModelVendor as VendorData,
  VirtoCommerceCustomerModuleCoreModelSearchVendorSearchResult as VendorSearchResult,
} from "../generated/rest-api";

export type {
  ContactData,
  CustomerAddress,
  EmployeeData,
  MemberData,
  MemberSearchResult,
  MembersSearchCriteria,
  OrganizationData,
  VendorData,
  VendorSearchResult,
};

export const MEMBER_FIELDS = ["id", "name", "memberType"] as const;

export interface MemberBaseData {
  id?: string | null;
  name?: string | null;
  memberType?: string | null;
}

export type Member<Data extends MemberBaseData> = WithRequired<Data, (typeof MEMBER_FIELDS)[number]>;
