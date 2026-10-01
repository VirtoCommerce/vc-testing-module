import type { Page } from "@playwright/test";
import type { HttpClient } from "@api/http/http-client";
import type { CleanupStack } from "@core/cleanup-stack";
import type { SignedInCustomerAccount } from "@fixtures";

import * as allure from "allure-js-commons";

import { CustomersClient } from "@api/rest/clients/customers-client";
import { OrganizationMembershipsClient } from "@api/rest/clients/organization-memberships-client";
import { requireFields } from "@core/required-fields";
import { uniqueId } from "@core/unique-id";
import { addOrganizationMembership, arrangeOrganization } from "@dataset/arrange/customer-account";
import { expect, test } from "@fixtures";
import { HomePage, SignInPage } from "@pages/frontend/pages/simple-pages";

const NO_MATCH = "NonExistentOrg";
const FRONTEND_SEARCH_THRESHOLD = 10;
const SPECIAL_CHARACTER_TERMS = [
  { term: "[e2e]", description: "literal brackets" },
  { term: "(parentheses)", description: "parentheses" },
  { term: "Company &", description: "an ampersand" },
  { term: "Test* Des", description: "an asterisk" },
] as const;

interface ArrangedOrganization {
  readonly id: string;
  readonly name: string;
  readonly membershipId: string;
}

test.beforeEach(async () => {
  await allure.feature("Account / Organizations menu (E2E)");
});

test.describe("organizations menu (signed-in customer account)", () => {
  test.use({ shopperAccount: "customer-account" });

  test("switch the active organization", async ({ page, customerAccount, platformAdminHttpClient, cleanupStack }) => {
    const defaultName = await organizationName(platformAdminHttpClient, customerAccount.organizationId);
    const other = await arrangeMemberOrganization(platformAdminHttpClient, cleanupStack, customerAccount);
    const { topHeader } = new HomePage(page);

    await test.step(`arrange: the header shows ${defaultName}`, async () => {
      await new HomePage(page).navigate();
      await expect(topHeader.accountButton.organizationNameLabel).toHaveText(defaultName);
    });

    await test.step(`act: switch to ${other.name}`, async () => {
      await topHeader.accountButton.root.click();
      await topHeader.accountMenu.selectOrganization(other.name);
    });

    await test.step(`assert: the header shows ${other.name}`, async () => {
      await expect(topHeader.accountButton.organizationNameLabel).toHaveText(other.name);
    });
  });

  test("search organizations by part of their name", async ({
    page,
    customerAccount,
    platformAdminHttpClient,
    cleanupStack,
  }) => {
    const token = uniqueId("org");
    await arrangeSearchableOrganizations(platformAdminHttpClient, cleanupStack, customerAccount, [
      `${token} Alpha`,
      `${token} Beta`,
    ]);
    const { topHeader } = new HomePage(page);

    await test.step("arrange: open the account menu", () => openAccountMenu(page));

    await test.step(`act: search for "${token}"`, () => topHeader.accountMenu.searchOrganizations(token));

    await test.step(`assert: both matching organizations are listed and every result contains "${token}"`, async () => {
      await expect(topHeader.accountMenu.organization(`${token} Beta`)).toBeVisible();
      const names = await topHeader.accountMenu.organizationNames();
      expect(names.filter((name) => name.includes(token))).toHaveLength(2);
    });
  });

  test("searching organizations without matches shows the empty state", async ({
    page,
    customerAccount,
    platformAdminHttpClient,
    cleanupStack,
  }) => {
    await arrangeSearchableOrganizations(platformAdminHttpClient, cleanupStack, customerAccount, []);
    const { topHeader } = new HomePage(page);

    await test.step("arrange: open the account menu", () => openAccountMenu(page));

    await test.step(`act: search for "${NO_MATCH}"`, () => topHeader.accountMenu.searchOrganizations(NO_MATCH));

    await test.step("assert: the empty state is shown", async () => {
      await expect(topHeader.accountMenu.organizationsEmptyList).toBeVisible();
    });
  });

  for (const { term, description } of SPECIAL_CHARACTER_TERMS) {
    test(`search organizations by a term with ${description}`, async ({
      page,
      customerAccount,
      platformAdminHttpClient,
      cleanupStack,
    }) => {
      const [other] = await arrangeSearchableOrganizations(platformAdminHttpClient, cleanupStack, customerAccount, [
        `${term} ${uniqueId("org")}`,
      ]);
      const { topHeader } = new HomePage(page);

      await test.step("arrange: open the account menu", () => openAccountMenu(page));

      await test.step(`act: search for "${term}"`, () => topHeader.accountMenu.searchOrganizations(term));

      await test.step(`assert: an organization containing "${term}" is found`, async () => {
        await expect(
          topHeader.accountMenu.organization(requireFields(other, ["name"], "Searched organization").name),
        ).toBeVisible();
      });
    });
  }
});

test.describe("organizations menu with locked memberships (sign-in after locking)", () => {
  test("a locked organization stays listed but cannot be selected", async ({
    page,
    customerAccount,
    platformAdminHttpClient,
    cleanupStack,
  }) => {
    const defaultName = await organizationName(platformAdminHttpClient, customerAccount.organizationId);
    const locked = await arrangeMemberOrganization(platformAdminHttpClient, cleanupStack, customerAccount);
    await test.step(`arrange: lock the membership in ${locked.name}`, () =>
      new OrganizationMembershipsClient(platformAdminHttpClient).lock(locked.membershipId));
    const { accountMenu } = new HomePage(page).topHeader;

    await test.step("act: sign in and open the account menu", async () => {
      await signIn(page, customerAccount);
      await openAccountMenu(page);
    });

    await test.step(`assert: ${locked.name} is listed but disabled`, async () => {
      await expect(accountMenu.organization(locked.name)).toBeVisible();
      await expect(accountMenu.organizationOption(locked.name)).toBeDisabled();
    });
    await test.step(`assert: ${defaultName} is still selectable`, async () => {
      await expect(accountMenu.organizationOption(defaultName)).toBeEnabled();
    });
  });

  test("with every organization locked the whole list is disabled and account pages stay reachable", async ({
    page,
    customerAccount,
    platformAdminHttpClient,
    cleanupStack,
  }) => {
    const other = await arrangeMemberOrganization(platformAdminHttpClient, cleanupStack, customerAccount);
    const membershipsClient = new OrganizationMembershipsClient(platformAdminHttpClient);
    await test.step("arrange: lock both memberships", async () => {
      const defaultMembership = requireFields(
        await membershipsClient.find(customerAccount.userId, customerAccount.organizationId),
        ["id"],
        "Default organization membership",
      );
      for (const membershipId of [defaultMembership.id, other.membershipId]) {
        await membershipsClient.lock(membershipId);
      }
    });
    const { accountMenu } = new HomePage(page).topHeader;

    await test.step("act: sign in and open the account menu", async () => {
      await signIn(page, customerAccount);
      await openAccountMenu(page);
    });

    await test.step("assert: both organizations are listed and disabled", async () => {
      await expect(accountMenu.organizationOptions).toHaveCount(2);
      for (const option of await accountMenu.organizationOptions.all()) {
        await expect(option).toBeDisabled();
      }
    });

    await test.step("assert: the dashboard is still reachable", async () => {
      await accountMenu.dashboardLink.click();
      await expect(page).toHaveURL(/\/account\/dashboard/);
    });
  });

  test("reopening the menu picks up a lock applied while it was closed", async ({
    page,
    customerAccount,
    platformAdminHttpClient,
    cleanupStack,
  }) => {
    const other = await arrangeMemberOrganization(platformAdminHttpClient, cleanupStack, customerAccount);
    const { accountButton, accountMenu } = new HomePage(page).topHeader;

    await test.step(`arrange: sign in and see ${other.name} selectable`, async () => {
      await signIn(page, customerAccount);
      await openAccountMenu(page);
      await expect(accountMenu.organizationOption(other.name)).toBeEnabled();
      await accountButton.root.click();
      await expect(accountMenu.root).toBeHidden();
    });

    await test.step(`act: lock the membership in ${other.name} while the menu is closed`, () =>
      new OrganizationMembershipsClient(platformAdminHttpClient).lock(other.membershipId));

    await test.step(`assert: after reopening, ${other.name} is disabled`, async () => {
      await accountButton.root.click();
      await expect(accountMenu.organizationOption(other.name)).toBeDisabled();
    });
  });
});

async function arrangeMemberOrganization(
  platformAdminHttpClient: HttpClient,
  cleanupStack: CleanupStack,
  account: SignedInCustomerAccount,
  name = uniqueId("test-organization"),
): Promise<ArrangedOrganization> {
  return test.step(`arrange: membership in organization ${name}`, async () => {
    const id = await arrangeOrganization(platformAdminHttpClient, cleanupStack, name);
    const membership = await addOrganizationMembership(platformAdminHttpClient, cleanupStack, account, id);
    return { id, name, membershipId: membership.id };
  });
}

async function arrangeSearchableOrganizations(
  platformAdminHttpClient: HttpClient,
  cleanupStack: CleanupStack,
  account: SignedInCustomerAccount,
  names: readonly string[],
): Promise<ArrangedOrganization[]> {
  const fillers = Array.from({ length: Math.max(0, FRONTEND_SEARCH_THRESHOLD - names.length) }, () =>
    uniqueId("test-organization"),
  );
  const arranged: ArrangedOrganization[] = [];
  for (const name of [...names, ...fillers]) {
    arranged.push(await arrangeMemberOrganization(platformAdminHttpClient, cleanupStack, account, name));
  }
  return arranged;
}

async function organizationName(platformAdminHttpClient: HttpClient, organizationId: string): Promise<string> {
  const organization = await new CustomersClient(platformAdminHttpClient).organizations.get(organizationId);
  return organization.name;
}

async function signIn(page: Page, account: SignedInCustomerAccount): Promise<void> {
  await new SignInPage(page).signIn(account.credentials.username, account.credentials.password);
  await page.waitForURL((url) => !url.pathname.startsWith("/sign-in"));
}

async function openAccountMenu(page: Page): Promise<void> {
  const homePage = new HomePage(page);
  await homePage.navigate();
  await homePage.topHeader.accountButton.root.click();
  await expect(homePage.topHeader.accountMenu.root).toBeVisible();
}
