import type { Credentials } from "@api/auth/credentials";
import type { HttpClient } from "@api/http/http-client";

import * as allure from "allure-js-commons";

import { GetOrganizationsDocument } from "@api/graphql/generated/graphql";
import { OrganizationMembershipsClient } from "@api/rest/clients/organization-memberships-client";
import {
  addOrganizationMembership,
  arrangeCustomerAccount,
  arrangeOrganization,
  signInWithoutCache,
} from "@dataset/arrange/customer-account";
import { expect, test } from "@fixtures";

const ORGANIZATIONS_PAGE_SIZE = 200;
const LOCK_VISIBLE_TIMEOUT_MS = 20_000;
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

interface OrganizationFlag {
  readonly id: string;
  readonly isLockedForCurrentUser: boolean | null;
}

test.beforeEach(async () => {
  await allure.feature("Contacts / Locked Organizations");
});

test.describe("locked organizations (customer account)", () => {
  test("a locked organization stays listed, flagged as locked", async ({
    customerAccount,
    platformAdminHttpClient,
    anonymousHttpClient,
    cleanupStack,
    env,
  }) => {
    const organizationId = await test.step("arrange: second organization", () =>
      arrangeOrganization(platformAdminHttpClient, cleanupStack));
    const membership = await test.step("arrange: membership in the second organization", () =>
      addOrganizationMembership(platformAdminHttpClient, cleanupStack, customerAccount, organizationId));
    await test.step("assert: the organization is listed as not locked", async () => {
      expect(await flagOf(anonymousHttpClient, customerAccount.credentials, env.storeId, organizationId)).toBe(false);
    });

    await test.step("act: lock the account in the second organization", () =>
      new OrganizationMembershipsClient(platformAdminHttpClient).lock(membership.id));

    await test.step("assert: after signing in again, the organization is listed as locked", async () => {
      await expect
        .poll(() => flagOf(anonymousHttpClient, customerAccount.credentials, env.storeId, organizationId), {
          timeout: LOCK_VISIBLE_TIMEOUT_MS,
        })
        .toBe(true);
      const page = await listOrganizations(anonymousHttpClient, customerAccount.credentials, env.storeId);
      expect(page.totalCount).toBe(page.items.length);
    });
  });

  test("an expired timed lock is not reported as locked", async ({
    customerAccount,
    platformAdminHttpClient,
    anonymousHttpClient,
    cleanupStack,
    env,
  }) => {
    const organizationId = await test.step("arrange: second organization", () =>
      arrangeOrganization(platformAdminHttpClient, cleanupStack));
    const membership = await test.step("arrange: membership in the second organization", () =>
      addOrganizationMembership(platformAdminHttpClient, cleanupStack, customerAccount, organizationId));

    await test.step("act: lock the account until yesterday", () =>
      new OrganizationMembershipsClient(platformAdminHttpClient).lock(
        membership.id,
        new Date(Date.now() - ONE_DAY_MS),
      ));

    await test.step("assert: the organization is listed as not locked", async () => {
      expect(await flagOf(anonymousHttpClient, customerAccount.credentials, env.storeId, organizationId)).toBe(false);
    });
  });

  test("locking one user does not lock the organization for another user", async ({
    customerAccount,
    platformAdminHttpClient,
    anonymousHttpClient,
    cleanupStack,
    env,
  }) => {
    const organizationId = await test.step("arrange: shared organization", () =>
      arrangeOrganization(platformAdminHttpClient, cleanupStack));
    const membership = await test.step("arrange: first user's membership in the shared organization", () =>
      addOrganizationMembership(platformAdminHttpClient, cleanupStack, customerAccount, organizationId));
    const otherAccount = await test.step("arrange: second user of the shared organization", () =>
      arrangeCustomerAccount(platformAdminHttpClient, cleanupStack, {
        storeId: env.storeId,
        role: "org-employee",
        organizationId,
      }));

    await test.step("act: lock the first user in the shared organization", () =>
      new OrganizationMembershipsClient(platformAdminHttpClient).lock(membership.id));

    await test.step("assert: the first user sees the organization as locked", async () => {
      await expect
        .poll(() => flagOf(anonymousHttpClient, customerAccount.credentials, env.storeId, organizationId), {
          timeout: LOCK_VISIBLE_TIMEOUT_MS,
        })
        .toBe(true);
    });
    await test.step("assert: the second user sees it as not locked", async () => {
      expect(await flagOf(anonymousHttpClient, otherAccount.credentials, env.storeId, organizationId)).toBe(false);
    });
  });
});

async function listOrganizations(
  anonymousHttpClient: HttpClient,
  credentials: Credentials,
  storeId: string,
): Promise<{ totalCount: number; items: OrganizationFlag[] }> {
  const graphqlClient = await signInWithoutCache(anonymousHttpClient, credentials, storeId);
  const { me } = await graphqlClient.execute(GetOrganizationsDocument, { first: ORGANIZATIONS_PAGE_SIZE });
  const organizations = me?.contact?.organizations;
  return {
    totalCount: organizations?.totalCount ?? 0,
    items: (organizations?.items ?? []).flatMap((item) =>
      item === null ? [] : [{ id: item.id, isLockedForCurrentUser: item.isLockedForCurrentUser }],
    ),
  };
}

async function flagOf(
  anonymousHttpClient: HttpClient,
  credentials: Credentials,
  storeId: string,
  organizationId: string,
): Promise<boolean | null | undefined> {
  const { items } = await listOrganizations(anonymousHttpClient, credentials, storeId);
  return items.find(({ id }) => id === organizationId)?.isLockedForCurrentUser;
}
