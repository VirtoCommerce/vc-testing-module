import type { InputMemberAddressType, MemberAddressFragment } from "@api/graphql/generated/graphql";
import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { SignedInCustomerAccount } from "@fixtures";

import * as allure from "allure-js-commons";

import {
  GetCurrentCustomerAddressesDocument,
  GetCurrentOrganizationAddressesDocument,
} from "@api/graphql/generated/graphql";
import { uniqueId } from "@core/unique-id";
import { saveMemberAddresses } from "@dataset/arrange/contact";
import { newMemberAddress } from "@dataset/builders/address";
import { expect, test } from "@fixtures";

const INDEXING_TIMEOUT_MS = 30_000;
const ALL_ADDRESSES_PAGE_SIZE = 200;

interface AddressQuery {
  readonly after?: string;
  readonly first?: number;
  readonly countryCodes?: string[];
  readonly regionIds?: string[];
  readonly cities?: string[];
  readonly keyword?: string;
  readonly sort?: string;
}

interface AddressPage {
  readonly totalCount: number;
  readonly items: readonly MemberAddressFragment[];
}

interface FilterCase {
  readonly filter: string;
  readonly draftOverrides: Partial<InputMemberAddressType>;
  readonly query: AddressQuery;
}

interface AddressScope {
  readonly name: "customer" | "organization";
  readonly ownerOf: (account: SignedInCustomerAccount) => string;
  readonly otherOwnerOf: (account: SignedInCustomerAccount) => string;
  readonly query: (graphqlClient: GraphqlClient, query: AddressQuery) => Promise<AddressPage>;
  readonly queryErrors: (graphqlClient: GraphqlClient) => Promise<string[]>;
}

const SCOPES: readonly AddressScope[] = [
  {
    name: "customer",
    ownerOf: (account) => account.contactId,
    otherOwnerOf: (account) => account.organizationId,
    async query(graphqlClient, query) {
      const { currentCustomerAddresses } = await graphqlClient.execute(GetCurrentCustomerAddressesDocument, query);
      return toPage(currentCustomerAddresses);
    },
    async queryErrors(graphqlClient) {
      return (await graphqlClient.executeRaw(GetCurrentCustomerAddressesDocument, {})).errors.map(
        ({ message }) => message,
      );
    },
  },
  {
    name: "organization",
    ownerOf: (account) => account.organizationId,
    otherOwnerOf: (account) => account.contactId,
    async query(graphqlClient, query) {
      const { currentOrganizationAddresses } = await graphqlClient.execute(
        GetCurrentOrganizationAddressesDocument,
        query,
      );
      return toPage(currentOrganizationAddresses);
    },
    async queryErrors(graphqlClient) {
      return (await graphqlClient.executeRaw(GetCurrentOrganizationAddressesDocument, {})).errors.map(
        ({ message }) => message,
      );
    },
  },
];

const FILTER_CASES: readonly FilterCase[] = [
  { filter: "country code", draftOverrides: { countryCode: "USA" }, query: { countryCodes: ["USA"] } },
  {
    filter: "region",
    draftOverrides: { regionId: "NY", regionName: "New York" },
    query: { regionIds: ["NY"] },
  },
];

test.beforeEach(async () => {
  await allure.feature("Contacts / Current Addresses");
});

for (const scope of SCOPES) {
  test.describe(`current ${scope.name} addresses (customer account)`, () => {
    test("list addresses with a total count", async ({ customerAccount }) => {
      const draft = newMemberAddress(`test-${scope.name}-address`);
      await test.step("arrange: one address", () =>
        saveMemberAddresses(customerAccount.graphqlClient, scope.ownerOf(customerAccount), [draft]));

      const page = await test.step("act: list addresses", () =>
        waitForAddresses(scope, customerAccount.graphqlClient, [draft.description]));

      await test.step("assert: the address is listed and counted", async () => {
        expect(page.totalCount).toBeGreaterThanOrEqual(1);
        expect(descriptionsOf(page)).toContain(draft.description);
      });
    });

    test("limit a page with first", async ({ customerAccount }) => {
      const drafts = [newMemberAddress(`test-${scope.name}-a`), newMemberAddress(`test-${scope.name}-b`)];
      await test.step("arrange: two addresses", () =>
        saveMemberAddresses(customerAccount.graphqlClient, scope.ownerOf(customerAccount), drafts));
      await waitForAddresses(
        scope,
        customerAccount.graphqlClient,
        drafts.map(({ description }) => description),
      );

      const page = await test.step("act: request one address", () =>
        scope.query(customerAccount.graphqlClient, { first: 1 }));

      await test.step("assert: one address is returned out of at least two", async () => {
        expect(page.items).toHaveLength(1);
        expect(page.totalCount).toBeGreaterThanOrEqual(2);
      });
    });

    test("page forward with after", async ({ customerAccount }) => {
      const drafts = ["a", "b", "c"].map((suffix) => newMemberAddress(`test-${scope.name}-${suffix}`));
      await test.step("arrange: three addresses", () =>
        saveMemberAddresses(customerAccount.graphqlClient, scope.ownerOf(customerAccount), drafts));
      const baseline = await waitForAddresses(
        scope,
        customerAccount.graphqlClient,
        drafts.map(({ description }) => description),
      );

      const pages = await test.step("act: read the first two pages of one address", async () => [
        await scope.query(customerAccount.graphqlClient, { first: 1, after: "0" }),
        await scope.query(customerAccount.graphqlClient, { first: 1, after: "1" }),
      ]);

      await test.step("assert: pages follow the unpaginated order", async () => {
        expect(pages.map((page) => page.items.map(({ id }) => id))).toEqual([
          [baseline.items[0]?.id],
          [baseline.items[1]?.id],
        ]);
      });
    });

    for (const { filter, draftOverrides, query } of FILTER_CASES) {
      test(`filter addresses by ${filter}`, async ({ customerAccount }) => {
        const draft = newMemberAddress(`test-${scope.name}-address`, draftOverrides);
        await test.step("arrange: matching address", () =>
          saveMemberAddresses(customerAccount.graphqlClient, scope.ownerOf(customerAccount), [draft]));
        await waitForAddresses(scope, customerAccount.graphqlClient, [draft.description]);

        const page = await test.step(`act: filter by ${filter}`, () =>
          scope.query(customerAccount.graphqlClient, query));

        await test.step("assert: the matching address is returned", async () => {
          expect(descriptionsOf(page)).toContain(draft.description);
        });
      });
    }

    test("filter addresses by city", async ({ customerAccount }) => {
      const city = uniqueId("City");
      const matching = newMemberAddress(`test-${scope.name}-address`, { city });
      const other = newMemberAddress(`test-${scope.name}-address`);
      await test.step("arrange: one address in the city and one elsewhere", () =>
        saveMemberAddresses(customerAccount.graphqlClient, scope.ownerOf(customerAccount), [matching, other]));
      await waitForAddresses(scope, customerAccount.graphqlClient, [matching.description, other.description]);

      const page = await test.step(`act: filter by city ${city}`, () =>
        scope.query(customerAccount.graphqlClient, { cities: [city] }));

      await test.step("assert: only the address in that city is returned", async () => {
        expect(descriptionsOf(page)).toEqual([matching.description]);
      });
    });

    test("search addresses by keyword", async ({ customerAccount }) => {
      const keyword = uniqueId("kw").replaceAll("-", "");
      const matching = newMemberAddress(`test-${scope.name}-address`, { line1: `1 ${keyword} Street` });
      const other = newMemberAddress(`test-${scope.name}-address`);
      await test.step("arrange: one address with the keyword and one without", () =>
        saveMemberAddresses(customerAccount.graphqlClient, scope.ownerOf(customerAccount), [matching, other]));
      await waitForAddresses(scope, customerAccount.graphqlClient, [matching.description, other.description]);

      const page = await test.step(`act: search "${keyword}"`, () =>
        scope.query(customerAccount.graphqlClient, { keyword }));

      await test.step("assert: only the address with the keyword is returned", async () => {
        expect(descriptionsOf(page)).toEqual([matching.description]);
      });
    });

    test("sort addresses by city ascending", async ({ customerAccount }) => {
      const suffix = uniqueId("sort");
      const citiesInSaveOrder = [`Zeta-${suffix}`, `Alpha-${suffix}`, `Mu-${suffix}`];
      const drafts = citiesInSaveOrder.map((city) => newMemberAddress(`test-${scope.name}-address`, { city }));
      await test.step("arrange: addresses saved out of city order", () =>
        saveMemberAddresses(customerAccount.graphqlClient, scope.ownerOf(customerAccount), drafts));
      await waitForAddresses(
        scope,
        customerAccount.graphqlClient,
        drafts.map(({ description }) => description),
      );

      const page = await test.step("act: list addresses sorted by city", () =>
        scope.query(customerAccount.graphqlClient, { sort: "city:asc", first: ALL_ADDRESSES_PAGE_SIZE }));

      await test.step("assert: addresses are in ascending city order", async () => {
        expect(page.items.map(({ city }) => city)).toEqual([...citiesInSaveOrder].sort());
      });
    });

    test(`only ${scope.name} addresses are returned`, async ({ customerAccount }) => {
      const own = newMemberAddress(`test-${scope.name}-address`);
      const other = newMemberAddress("test-other-address");
      await test.step(`arrange: an address on the ${scope.name} and one on the other member`, async () => {
        await saveMemberAddresses(customerAccount.graphqlClient, scope.ownerOf(customerAccount), [own]);
        await saveMemberAddresses(customerAccount.graphqlClient, scope.otherOwnerOf(customerAccount), [other]);
      });

      const page = await test.step("act: list addresses", () =>
        waitForAddresses(scope, customerAccount.graphqlClient, [own.description]));

      await test.step(`assert: only the ${scope.name} address is listed`, async () => {
        expect(descriptionsOf(page)).toContain(own.description);
        expect(descriptionsOf(page)).not.toContain(other.description);
      });
    });
  });

  test.describe(`current ${scope.name} addresses (anonymous)`, () => {
    test("deny anonymous access", async ({ graphqlClient }) => {
      const errors = await test.step("act: list addresses anonymously", () => scope.queryErrors(graphqlClient));

      await test.step("assert: access is denied", async () => {
        expect(errors.join(" ")).toMatch(/Forbidden|Access denied/);
      });
    });
  });
}

test.describe("current customer addresses (customer account)", () => {
  test("return every address field", async ({ customerAccount }) => {
    const draft = newMemberAddress("test-customer-address");
    await test.step("arrange: one address", () =>
      saveMemberAddresses(customerAccount.graphqlClient, customerAccount.contactId, [draft]));

    const page = await test.step("act: list addresses", () =>
      waitForAddresses(SCOPES[0] as AddressScope, customerAccount.graphqlClient, [draft.description]));

    await test.step("assert: the address has every saved field", async () => {
      expect(page.items.find(({ description }) => description === draft.description)).toMatchObject({
        id: expect.any(String),
        city: draft.city,
        countryCode: draft.countryCode,
        countryName: draft.countryName,
        regionId: draft.regionId,
        regionName: draft.regionName,
        line1: draft.line1,
        postalCode: draft.postalCode,
        firstName: draft.firstName,
        lastName: draft.lastName,
        addressType: draft.addressType,
      });
    });
  });
});

async function waitForAddresses(
  scope: AddressScope,
  graphqlClient: GraphqlClient,
  descriptions: readonly string[],
): Promise<AddressPage> {
  let page: AddressPage = { totalCount: 0, items: [] };
  await expect
    .poll(
      async () => {
        page = await scope.query(graphqlClient, { first: ALL_ADDRESSES_PAGE_SIZE });
        return descriptionsOf(page);
      },
      { timeout: INDEXING_TIMEOUT_MS },
    )
    .toEqual(expect.arrayContaining([...descriptions]));
  return page;
}

function descriptionsOf(page: AddressPage): (string | null)[] {
  return page.items.map(({ description }) => description);
}

function toPage(
  connection: { totalCount: number | null; items: readonly (MemberAddressFragment | null)[] | null } | null | undefined,
): AddressPage {
  return {
    totalCount: connection?.totalCount ?? 0,
    items: (connection?.items ?? []).flatMap((item) => (item === null ? [] : [item])),
  };
}
