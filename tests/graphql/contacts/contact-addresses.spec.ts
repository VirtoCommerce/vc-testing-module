import * as allure from "allure-js-commons";

import {
  AddAddressToFavoritesDocument,
  DeleteMemberAddressesDocument,
  GetContactAddressesDocument,
  RemoveAddressFromFavoritesDocument,
  UpdateMemberAddressesDocument,
} from "@api/graphql/generated/graphql";
import { saveMemberAddress, toMemberAddressInput } from "@dataset/arrange/contact";
import { addressDescribedAs, comparableAddress, newMemberAddress } from "@dataset/builders/address";
import { expect, test } from "@fixtures";

test.beforeEach(async () => {
  await allure.feature("Contacts / Addresses");
});

test.describe("contact addresses (customer account)", () => {
  test("add a personal address", async ({ customerAccount }) => {
    const draft = newMemberAddress("test-personal-address");

    const address = await test.step("act: save the address on the contact", () =>
      saveMemberAddress(customerAccount.graphqlClient, customerAccount.contactId, draft));

    await test.step("assert: the contact has the address", async () => {
      expect(address).toMatchObject(comparableAddress(draft));
    });
  });

  test("add an organization address", async ({ customerAccount }) => {
    const draft = newMemberAddress("test-organization-address");

    const address = await test.step("act: save the address on the organization", () =>
      saveMemberAddress(customerAccount.graphqlClient, customerAccount.organizationId, draft));

    await test.step("assert: the organization has the address", async () => {
      expect(address).toMatchObject(comparableAddress(draft));
    });
  });

  test("update an organization address", async ({ customerAccount }) => {
    const address = await test.step("arrange: organization address", () =>
      saveMemberAddress(
        customerAccount.graphqlClient,
        customerAccount.organizationId,
        newMemberAddress("test-organization-address"),
      ));
    const changes = { city: "Updated City", line1: `2 Updated Street ${address.description}` };

    const { updateMemberAddresses } = await test.step("act: change city and street", () =>
      customerAccount.graphqlClient.execute(UpdateMemberAddressesDocument, {
        command: {
          memberId: customerAccount.organizationId,
          addresses: [{ ...toMemberAddressInput(address), ...changes }],
        },
      }));

    await test.step("assert: the address has the new city and street", async () => {
      expect(addressDescribedAs(updateMemberAddresses?.addresses?.items, address.description)).toMatchObject({
        id: address.id,
        ...changes,
      });
    });
  });

  test("remove an organization address", async ({ customerAccount }) => {
    const address = await test.step("arrange: organization address", () =>
      saveMemberAddress(
        customerAccount.graphqlClient,
        customerAccount.organizationId,
        newMemberAddress("test-organization-address"),
      ));

    const { deleteMemberAddresses } = await test.step("act: delete the address", () =>
      customerAccount.graphqlClient.execute(DeleteMemberAddressesDocument, {
        command: { memberId: customerAccount.organizationId, addresses: [toMemberAddressInput(address)] },
      }));

    await test.step("assert: the organization no longer has the address", async () => {
      expect(deleteMemberAddresses?.addresses?.items?.map((item) => item?.id)).not.toContain(address.id);
    });
  });

  test("remove a contact address", async ({ customerAccount }) => {
    const address = await test.step("arrange: contact address", () =>
      saveMemberAddress(
        customerAccount.graphqlClient,
        customerAccount.contactId,
        newMemberAddress("test-personal-address"),
      ));

    const { deleteMemberAddresses } = await test.step("act: delete the address", () =>
      customerAccount.graphqlClient.execute(DeleteMemberAddressesDocument, {
        command: { memberId: customerAccount.contactId, addresses: [toMemberAddressInput(address)] },
      }));

    await test.step("assert: the contact no longer has the address", async () => {
      expect(deleteMemberAddresses?.addresses?.items?.map((item) => item?.id)).not.toContain(address.id);
    });
  });

  test("add an address to favorites and remove it", async ({ customerAccount }) => {
    const { graphqlClient, contactId } = customerAccount;
    const address = await test.step("arrange: contact address", () =>
      saveMemberAddress(graphqlClient, contactId, newMemberAddress("test-personal-address")));
    async function isFavorite(): Promise<boolean | undefined> {
      const { contact } = await graphqlClient.execute(GetContactAddressesDocument, { id: contactId });
      return addressDescribedAs(contact?.addresses?.items, address.description)?.isFavorite;
    }

    const { addAddressToFavorites } = await test.step("act: add the address to favorites", () =>
      graphqlClient.execute(AddAddressToFavoritesDocument, { command: { addressId: address.id } }));
    await test.step("assert: the address is a favorite", async () => {
      expect(addAddressToFavorites).toBe(true);
      expect(await isFavorite()).toBe(true);
    });

    const { removeAddressFromFavorites } = await test.step("act: remove the address from favorites", () =>
      graphqlClient.execute(RemoveAddressFromFavoritesDocument, { command: { addressId: address.id } }));
    await test.step("assert: the address is no longer a favorite", async () => {
      expect(removeAddressFromFavorites).toBe(true);
      expect(await isFavorite()).toBe(false);
    });
  });
});
