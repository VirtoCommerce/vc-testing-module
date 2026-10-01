import type { SavedMemberAddress } from "@dataset/arrange/contact";
import type { SignedInCustomerAccount } from "@fixtures";
import type { AddressFilter, AddressFilters } from "@pages/frontend/components/address-filters";
import type { DropdownFilter } from "@pages/frontend/components/dropdown-filter";

import { saveMemberAddress } from "@dataset/arrange/contact";
import { newMemberAddress } from "@dataset/builders/address";
import { expect, test } from "@fixtures";

export const PRODUCT_ID = "smartphone-google-pixel-10-lemongrass";
export const QUANTITY = 3;
export const FIXED_RATE_GROUND = "FixedRate_Ground";
export const FIXED_RATE_AIR = "FixedRate_Air";
export const MANUAL_PAYMENT_METHOD = "DefaultManualPaymentMethod";

export const SAVED_ADDRESS = {
  line1: "742 Evergreen Terrace",
  city: "Morrisville",
  regionId: "NC",
  regionName: "North Carolina",
  countryCode: "USA",
  countryName: "United States of America",
  postalCode: "27560",
} as const;

export const ADDRESS_FILTERS: readonly { readonly title: string; readonly filter: AddressFilter }[] = [
  { title: "country", filter: { country: SAVED_ADDRESS.countryName } },
  { title: "country and region", filter: { country: SAVED_ADDRESS.countryName, region: SAVED_ADDRESS.regionName } },
  {
    title: "country, region and city",
    filter: { country: SAVED_ADDRESS.countryName, region: SAVED_ADDRESS.regionName, city: SAVED_ADDRESS.city },
  },
];

export function arrangeSavedOrganizationAddress(account: SignedInCustomerAccount): Promise<SavedMemberAddress> {
  return test.step(`arrange: organization address ${SAVED_ADDRESS.line1}, ${SAVED_ADDRESS.city}`, () =>
    saveMemberAddress(
      account.graphqlClient,
      account.organizationId,
      newMemberAddress("test-org-address", SAVED_ADDRESS),
    ));
}

export async function applyAddressFilter(filters: AddressFilters, filter: AddressFilter): Promise<void> {
  const levels: readonly [DropdownFilter, string | undefined][] = [
    [filters.country, filter.country],
    [filters.region, filter.region],
    [filters.city, filter.city],
  ];
  for (const [dropdown, value] of levels) {
    if (value === undefined) {
      continue;
    }
    await test.step(`act: filter by "${value}"`, async () => {
      await filters.apply(dropdown, value);
      await expect(filters.appliedChip(value).root).toBeVisible();
    });
  }
}
