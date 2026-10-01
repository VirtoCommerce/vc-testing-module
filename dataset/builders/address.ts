import type { InputAddressType, InputMemberAddressType } from "@api/graphql/generated/graphql";

import { uniqueId } from "@core/unique-id";

export const BILLING_AND_SHIPPING_ADDRESS_TYPE = 3;

export const TEST_ADDRESS = {
  firstName: "John",
  lastName: "Doe",
  line1: "1 Test Street",
  city: "Test City",
  countryCode: "USA",
  countryName: "United States of America",
  postalCode: "10001",
  regionId: "NY",
  regionName: "New York",
  phone: "+1 (555) 000-0000",
  email: "john.doe@test.com",
  addressType: BILLING_AND_SHIPPING_ADDRESS_TYPE,
} as const satisfies InputAddressType;

const COMPARED_ADDRESS_FIELDS = [
  "countryCode",
  "countryName",
  "regionId",
  "regionName",
  "city",
  "line1",
  "line2",
] as const satisfies readonly (keyof InputAddressType)[];

export function comparableAddress(address: InputAddressType): Partial<InputAddressType> {
  return Object.fromEntries(
    COMPARED_ADDRESS_FIELDS.filter((field) => address[field] !== undefined).map((field) => [field, address[field]]),
  );
}

export function newMemberAddress(
  prefix: string,
  overrides: Partial<InputMemberAddressType> = {},
): InputMemberAddressType & { readonly description: string } {
  const unique = uniqueId(prefix);
  return {
    ...TEST_ADDRESS,
    line1: `${TEST_ADDRESS.line1} #${unique}`,
    ...overrides,
    key: unique,
    description: unique,
  };
}

export function addressDescribedAs<Address extends { readonly description?: string | null }>(
  addresses: readonly (Address | null)[] | null | undefined,
  description: string,
): Address | undefined {
  return addresses?.find((address) => address?.description === description) ?? undefined;
}
