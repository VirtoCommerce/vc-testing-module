import * as allure from "allure-js-commons";

import {
  ChangeOrganizationContactRoleDocument,
  GetContactLockStatusDocument,
  GetContactRolesInOrganizationDocument,
  LockOrganizationContactDocument,
  UnlockOrganizationContactDocument,
} from "@api/graphql/generated/graphql";
import { arrangeCustomerAccount } from "@dataset/arrange/customer-account";
import { expect, test } from "@fixtures";

const TARGET_ROLE = "purchasing-agent";

test.beforeEach(async () => {
  await allure.feature("Contacts / Management");
});

test.describe("organization contact management (maintainer)", () => {
  test.use({ customerAccountRole: "org-maintainer" });

  test("change the role of an organization contact", async ({
    customerAccount,
    platformAdminHttpClient,
    cleanupStack,
    env,
  }) => {
    const employee = await test.step("arrange: employee in the maintainer's organization", () =>
      arrangeCustomerAccount(platformAdminHttpClient, cleanupStack, {
        storeId: env.storeId,
        role: "org-employee",
        organizationId: customerAccount.organizationId,
      }));

    const { changeOrganizationContactRole } = await test.step(`act: give the employee the ${TARGET_ROLE} role`, () =>
      customerAccount.graphqlClient.execute(ChangeOrganizationContactRoleDocument, {
        command: { memberId: employee.contactId, roleIds: [TARGET_ROLE], storeId: env.storeId },
      }));

    await test.step(`assert: the employee has the ${TARGET_ROLE} role in the organization`, async () => {
      expect(changeOrganizationContactRole?.succeeded).toBe(true);
      const { contact } = await customerAccount.graphqlClient.execute(GetContactRolesInOrganizationDocument, {
        id: employee.contactId,
      });
      expect(contact?.rolesInOrganization?.map((role) => role?.id)).toContain(TARGET_ROLE);
    });
  });

  test("lock and unlock an organization contact", async ({
    customerAccount,
    platformAdminHttpClient,
    cleanupStack,
    env,
  }) => {
    const employee = await test.step("arrange: employee in the maintainer's organization", () =>
      arrangeCustomerAccount(platformAdminHttpClient, cleanupStack, {
        storeId: env.storeId,
        role: "org-employee",
        organizationId: customerAccount.organizationId,
      }));
    async function isLocked(): Promise<boolean | null | undefined> {
      const { contact } = await customerAccount.graphqlClient.execute(GetContactLockStatusDocument, {
        id: employee.contactId,
      });
      return contact?.isLockedInOrganization;
    }

    await test.step("act: lock the employee", () =>
      customerAccount.graphqlClient.execute(LockOrganizationContactDocument, {
        command: { memberId: employee.contactId },
      }));
    await test.step("assert: the employee is locked in the organization", async () => {
      expect(await isLocked()).toBe(true);
    });

    await test.step("act: unlock the employee", () =>
      customerAccount.graphqlClient.execute(UnlockOrganizationContactDocument, {
        command: { memberId: employee.contactId },
      }));
    await test.step("assert: the employee is unlocked", async () => {
      expect(await isLocked()).toBe(false);
    });
  });
});
