import type { InputMemberAddressType, MemberAddressFragment } from "@api/graphql/generated/graphql";
import type { GraphqlClient } from "@api/graphql/graphql-client";

import { UpdateMemberAddressesDocument } from "@api/graphql/generated/graphql";
import { requireFields } from "@core/required-fields";

import { addressDescribedAs } from "../builders/address";

export type SavedMemberAddress = MemberAddressFragment & {
  readonly id: string;
  readonly city: string;
  readonly countryCode: string;
  readonly line1: string;
  readonly description: string;
};

export async function saveMemberAddresses(
  graphqlClient: GraphqlClient,
  memberId: string,
  drafts: readonly (InputMemberAddressType & { readonly description: string })[],
): Promise<SavedMemberAddress[]> {
  const { updateMemberAddresses } = await graphqlClient.execute(UpdateMemberAddressesDocument, {
    command: { memberId, addresses: [...drafts] },
  });
  const saved = updateMemberAddresses?.addresses?.items;
  return drafts.map((draft) =>
    requireFields(
      addressDescribedAs(saved, draft.description),
      ["id", "city", "countryCode", "line1", "description"],
      `Saved address ${draft.description}`,
    ),
  );
}

export async function saveMemberAddress(
  graphqlClient: GraphqlClient,
  memberId: string,
  draft: InputMemberAddressType & { readonly description: string },
): Promise<SavedMemberAddress> {
  const [saved] = await saveMemberAddresses(graphqlClient, memberId, [draft]);
  return requireFields(saved, ["id"], `Saved address ${draft.description}`);
}

export function toMemberAddressInput(address: SavedMemberAddress): InputMemberAddressType {
  return {
    id: address.id,
    key: address.key,
    addressType: address.addressType,
    city: address.city,
    countryCode: address.countryCode,
    countryName: address.countryName,
    description: address.description,
    email: address.email,
    firstName: address.firstName,
    middleName: address.middleName,
    lastName: address.lastName,
    line1: address.line1,
    line2: address.line2,
    name: address.name,
    organization: address.organization,
    outerId: address.outerId,
    phone: address.phone,
    postalCode: address.postalCode,
    regionId: address.regionId,
    regionName: address.regionName,
    zip: address.zip,
  };
}
