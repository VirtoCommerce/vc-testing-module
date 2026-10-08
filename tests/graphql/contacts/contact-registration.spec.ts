import * as allure from "allure-js-commons";

import { RequestRegistrationDocument } from "@api/graphql/generated/graphql";
import { CustomersClient } from "@api/rest/clients/customers-client";
import { UsersClient } from "@api/rest/clients/users-client";
import { requireFields } from "@core/required-fields";
import { uniqueId } from "@core/unique-id";
import { registerAccountRemoval } from "@dataset/arrange/security";
import { newPassword } from "@dataset/builders/security";
import { expect, test } from "@fixtures";

const APPROVED = "Approved";
const REGISTRATION_TIMEOUT_MS = 30_000;

test.beforeEach(async () => {
  await allure.feature("Contacts / Registration");
});

test.describe("contact registration (anonymous)", () => {
  test("register a personal contact", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
  }) => {
    const email = `${uniqueId("test-register-personal")}@example.com`;
    registerAccountRemoval(
      new UsersClient(platformAdminHttpClient),
      new CustomersClient(platformAdminHttpClient),
      cleanupStack,
      email,
    );

    const { requestRegistration } = await test.step(`act: register ${email}`, () =>
      graphqlClient.execute(RequestRegistrationDocument, {
        command: {
          storeId: frontendContext.storeId,
          languageCode: frontendContext.cultureName,
          contact: { firstName: "John", lastName: "Doe" },
          account: { username: email, email, password: newPassword() },
        },
      }));
    const contact = requireFields(requestRegistration?.contact ?? undefined, ["id"], "Registered contact");

    await test.step("assert: registration succeeded without an organization", async () => {
      expect(requestRegistration).toMatchObject({
        result: { succeeded: true },
        organization: null,
        contact: { firstName: "John", lastName: "Doe" },
        account: { email },
      });
    });
    await test.step("assert: the contact is approved and belongs to no organization", async () => {
      const { contacts } = new CustomersClient(platformAdminHttpClient);
      await expect
        .poll(async () => (await contacts.find(contact.id))?.status, { timeout: REGISTRATION_TIMEOUT_MS })
        .toBe(APPROVED);
      expect((await contacts.get(contact.id)).organizations ?? []).toEqual([]);
    });
  });

  test("register a contact with a new organization", async ({
    graphqlClient,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
  }) => {
    const email = `${uniqueId("test-register-organization")}@example.com`;
    const organizationName = uniqueId("test-registered-organization");
    registerAccountRemoval(
      new UsersClient(platformAdminHttpClient),
      new CustomersClient(platformAdminHttpClient),
      cleanupStack,
      email,
    );

    const { requestRegistration } = await test.step(`act: register ${email} with ${organizationName}`, () =>
      graphqlClient.execute(RequestRegistrationDocument, {
        command: {
          storeId: frontendContext.storeId,
          languageCode: frontendContext.cultureName,
          contact: { firstName: "Jane", lastName: "Smith" },
          account: { username: email, email, password: newPassword() },
          organization: { name: organizationName },
        },
      }));
    const contact = requireFields(requestRegistration?.contact ?? undefined, ["id"], "Registered contact");
    const organization = requireFields(
      requestRegistration?.organization ?? undefined,
      ["id"],
      "Registered organization",
    );
    const { contacts, organizations } = new CustomersClient(platformAdminHttpClient);
    cleanupStack.push(`delete organization ${organization.id}`, () => organizations.delete([organization.id]));

    await test.step("assert: registration succeeded with the organization", async () => {
      expect(requestRegistration).toMatchObject({
        result: { succeeded: true },
        organization: { name: organizationName },
        contact: { firstName: "Jane", lastName: "Smith" },
        account: { email },
      });
    });
    await test.step("assert: the approved contact belongs to the organization", async () => {
      await expect
        .poll(async () => (await contacts.find(contact.id))?.organizations ?? [], { timeout: REGISTRATION_TIMEOUT_MS })
        .toContain(organization.id);
      expect((await contacts.get(contact.id)).status).toBe(APPROVED);
    });
  });
});
