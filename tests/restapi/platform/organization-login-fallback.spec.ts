import * as allure from "allure-js-commons";

import { CustomersClient } from "@api/rest/clients/customers-client";
import { OrganizationMembershipsClient } from "@api/rest/clients/organization-memberships-client";
import { UsersClient } from "@api/rest/clients/users-client";
import { arrangeUser } from "@dataset/arrange/security";
import { newContact, newOrganization } from "@dataset/builders/customer";
import { newUser } from "@dataset/builders/security";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Platform / Organization Login Fallback");
});

test.describe("organization login fallback (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("VCST-5317: sign in with a stale organization once every organization is locked", async ({
    httpClient,
    anonymousHttpClient,
    cleanupStack,
    env,
  }) => {
    const customersClient = new CustomersClient(httpClient);
    const usersClient = new UsersClient(httpClient);
    const membershipsClient = new OrganizationMembershipsClient(httpClient);
    const staleOrganization = newOrganization();
    const organizations = [staleOrganization, newOrganization()];
    const organizationIds = organizations.map(({ id }) => id);
    cleanupStack.push(`delete organizations ${organizationIds.join(", ")}`, () =>
      customersClient.organizations.delete(organizationIds),
    );
    await test.step("arrange: two organizations", () => customersClient.organizations.createMany(organizations));
    const contact = newContact(organizationIds);
    cleanupStack.push(`delete contact ${contact.id}`, () => customersClient.contacts.delete([contact.id]));
    await test.step("arrange: contact in both organizations", () => customersClient.contacts.create(contact));
    const draft = newUser(env.storeId, { userType: "Customer", memberId: contact.id });
    const user = await test.step("arrange: customer user of the contact", () =>
      arrangeUser(usersClient, cleanupStack, draft));
    await test.step("arrange: user is locked in every organization", async () => {
      for (const organizationId of organizationIds) {
        const membership =
          (await membershipsClient.find(user.id, organizationId)) ??
          (await membershipsClient.create({ userId: user.id, organizationId }));
        cleanupStack.push(`delete membership ${membership.id}`, () => membershipsClient.delete([membership.id]));
        await membershipsClient.lock(membership.id);
      }
    });

    const response = await test.step("act: sign in with the first, now locked, organization", () =>
      anonymousHttpClient.post("/connect/token", {
        form: {
          grant_type: "password",
          scope: "offline_access",
          username: draft.userName,
          password: draft.password,
          storeId: env.storeId,
          organization_id: staleOrganization.id,
        },
      }));

    await test.step("assert: sign-in succeeds without the stale organization", async () => {
      expect(response.status).toBe(200);
      expect(response.json()).toMatchObject({ access_token: expect.any(String) });
    });
  });
});
