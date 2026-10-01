import type {
  ContactData,
  CustomerAddress,
  EmployeeData,
  MemberData,
  OrganizationData,
} from "@api/rest/types/customers";
import type { WithRequired } from "@core/required-fields";

import { uniqueId } from "@core/unique-id";

export type ContactDraft = WithRequired<ContactData, "id" | "name" | "firstName" | "lastName">;
export type OrganizationDraft = WithRequired<OrganizationData, "id" | "name">;
export type EmployeeDraft = WithRequired<EmployeeData, "id" | "name" | "firstName" | "lastName">;
export type MemberDraft = WithRequired<MemberData, "id" | "name" | "memberType">;

export function newContact(organizationIds: string[] = []): ContactDraft {
  const firstName = uniquePersonName("Testfirst");
  const lastName = uniquePersonName("Testlast");
  return {
    id: crypto.randomUUID(),
    memberType: "Contact",
    firstName,
    lastName,
    name: `${firstName} ${lastName}`,
    ...(organizationIds.length === 0 ? {} : { organizations: organizationIds }),
  };
}

export function newOrganization(name = uniqueId("test-organization")): OrganizationDraft {
  return { id: crypto.randomUUID(), memberType: "Organization", name };
}

export function newEmployee(): EmployeeDraft {
  const firstName = uniquePersonName("Testemployee");
  const lastName = uniquePersonName("Testlast");
  return { id: crypto.randomUUID(), memberType: "Employee", firstName, lastName, name: `${firstName} ${lastName}` };
}

export function newMember(
  memberType: "Organization" | "Vendor" = "Organization",
  name = uniqueId("test-member"),
): MemberDraft {
  return { id: crypto.randomUUID(), memberType, name };
}

export function newAddress(): CustomerAddress {
  return {
    addressType: "BillingAndShipping",
    countryCode: "USA",
    countryName: "United States",
    city: "New York",
    line1: `${uniqueId("test-street")} Main St`,
    postalCode: "10001",
    regionId: "NY",
  };
}

function uniquePersonName(prefix: string): string {
  const letters = Array.from(crypto.getRandomValues(new Uint8Array(8)), (byte) =>
    String.fromCharCode(97 + (byte % 26)),
  ).join("");
  return `${prefix} ${letters.charAt(0).toUpperCase()}${letters.slice(1)}`;
}
