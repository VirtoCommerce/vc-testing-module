import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { FrontendContext } from "@dataset/frontend-context";

import * as allure from "allure-js-commons";

import { GetOrganizationContactsDocument } from "@api/graphql/generated/graphql";
import { requireFields } from "@core/required-fields";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const MAINTAINER_USERNAME = "acme_store_maintainer_1@acme.com";
const CONTACT_ID = "contact-acme-store-employee-1";
const CONTACT_FULL_NAME = "ACME Employee A";
const CONTACT_EMAIL = "acme_store_employee_1@acme.com";
const ROLE_IDS = ["org-maintainer", "org-employee", "purchasing-agent", "store-admin", "store-manager"] as const;
const STATUSES = ["Approved", "Invited", "Locked"] as const;
const CONTACTS_PAGE_SIZE = 100;

test.beforeEach(async () => {
  await allure.feature("Contacts / Search");
});

test.describe("organization contact search (seeded maintainer)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, MAINTAINER_USERNAME)) });

  test("find a contact by full name", async ({ graphqlClient, frontendContext }) => {
    const contacts = await test.step(`act: search "${CONTACT_FULL_NAME}"`, () =>
      searchContacts(graphqlClient, organizationOf(frontendContext), CONTACT_FULL_NAME));

    await test.step("assert: the contact is found by name", async () => {
      expect(contacts.find(({ id }) => id === CONTACT_ID)?.fullName).toContain(CONTACT_FULL_NAME);
    });
  });

  test("find a contact by email", async ({ graphqlClient, frontendContext }) => {
    const contacts = await test.step(`act: search "${CONTACT_EMAIL}"`, () =>
      searchContacts(graphqlClient, organizationOf(frontendContext), CONTACT_EMAIL));

    await test.step("assert: the contact with that account email is found", async () => {
      const contact = contacts.find(({ id }) => id === CONTACT_ID);
      expect(contact?.securityAccounts?.map((account) => account?.userName)).toContain(CONTACT_EMAIL);
    });
  });

  for (const roleId of ROLE_IDS) {
    test(`filter contacts by role ${roleId}`, async ({ graphqlClient, frontendContext }) => {
      const contacts = await test.step(`act: filter by role ${roleId}`, () =>
        searchContacts(graphqlClient, organizationOf(frontendContext), `'roleId':'${roleId}'`));

      await test.step(`assert: every contact has the ${roleId} role`, async () => {
        expect(contacts.length).toBeGreaterThan(0);
        const withoutRole = contacts.filter(
          (contact) =>
            !contact.securityAccounts?.some((account) => account?.roles?.some((role) => role?.id === roleId)),
        );
        expect(withoutRole.map(({ id }) => id)).toEqual([]);
      });
    });
  }

  for (const status of STATUSES) {
    test(`filter contacts by status ${status}`, async ({ graphqlClient, frontendContext }) => {
      const contacts = await test.step(`act: filter by status ${status}`, () =>
        searchContacts(graphqlClient, organizationOf(frontendContext), `'status':'${status}'`));

      await test.step(`assert: every contact is ${status}`, async () => {
        expect(contacts.length).toBeGreaterThan(0);
        expect(contacts.filter((contact) => contact.status !== status).map(({ id }) => id)).toEqual([]);
      });
    });
  }
});

function organizationOf(context: FrontendContext): string {
  return requireFields(context, ["organizationId"], `Organization of ${context.userName}`).organizationId;
}

async function searchContacts(graphqlClient: GraphqlClient, organizationId: string, searchPhrase: string) {
  const { organization } = await graphqlClient.execute(GetOrganizationContactsDocument, {
    organizationId,
    searchPhrase,
    first: CONTACTS_PAGE_SIZE,
  });
  return (organization?.contacts?.items ?? []).flatMap((contact) => (contact === null ? [] : [contact]));
}
