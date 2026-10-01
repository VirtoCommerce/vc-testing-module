import * as allure from "allure-js-commons";

import { CustomersClient } from "@api/rest/clients/customers-client";
import { newOrganization } from "@dataset/builders/customer";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Contacts / Organizations");
});

test.describe("organizations (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create an organization", async ({ httpClient, cleanupStack }) => {
    const { organizations } = new CustomersClient(httpClient);
    const draft = newOrganization();

    const organization = await test.step("act: create organization", () => organizations.create(draft));
    cleanupStack.push(`delete organization ${organization.id}`, () => organizations.delete([organization.id]));

    await test.step("assert: organization has its name", async () => {
      expect(organization).toMatchObject({ memberType: "Organization", name: draft.name });
    });
  });

  test("create organizations in bulk", async ({ httpClient, cleanupStack }) => {
    const { organizations } = new CustomersClient(httpClient);
    const drafts = [newOrganization(), newOrganization()];
    const ids = drafts.map(({ id }) => id);
    cleanupStack.push(`delete organizations ${ids.join(", ")}`, () => organizations.delete(ids));

    await test.step("act: create two organizations", () => organizations.createMany(drafts));

    await test.step("assert: both organizations exist", async () => {
      expect((await organizations.getMany(ids)).map(({ name }) => name).sort()).toEqual(
        drafts.map(({ name }) => name).sort(),
      );
    });
  });

  test("get an organization by id", async ({ httpClient, cleanupStack }) => {
    const { organizations } = new CustomersClient(httpClient);
    const organization = await test.step("arrange: organization", () => organizations.create(newOrganization()));
    cleanupStack.push(`delete organization ${organization.id}`, () => organizations.delete([organization.id]));

    const reloaded = await test.step("act: get organization", () => organizations.get(organization.id));

    await test.step("assert: fields match the created organization", async () => {
      expect(reloaded).toMatchObject({ id: organization.id, name: organization.name });
    });
  });

  test("get organizations by ids", async ({ httpClient, cleanupStack }) => {
    const { organizations } = new CustomersClient(httpClient);
    const created = await test.step("arrange: two organizations", () =>
      Promise.all([organizations.create(newOrganization()), organizations.create(newOrganization())]));
    const ids = created.map(({ id }) => id);
    cleanupStack.push(`delete organizations ${ids.join(", ")}`, () => organizations.delete(ids));

    const found = await test.step("act: get organizations by ids", () => organizations.getMany(ids));

    await test.step("assert: both organizations are returned", async () => {
      expect(found.map(({ id }) => id).sort()).toEqual([...ids].sort());
    });
  });

  test("search organizations by id", async ({ httpClient, cleanupStack }) => {
    const { organizations } = new CustomersClient(httpClient);
    const organization = await test.step("arrange: organization", () => organizations.create(newOrganization()));
    cleanupStack.push(`delete organization ${organization.id}`, () => organizations.delete([organization.id]));

    const found = await test.step("act: search by organization id", () =>
      organizations.search({ objectIds: [organization.id] }));

    await test.step("assert: organization is found", async () => {
      expect(found.map(({ id }) => id)).toEqual([organization.id]);
    });
  });

  test("rename an organization", async ({ httpClient, cleanupStack }) => {
    const { organizations } = new CustomersClient(httpClient);
    const organization = await test.step("arrange: organization", () => organizations.create(newOrganization()));
    cleanupStack.push(`delete organization ${organization.id}`, () => organizations.delete([organization.id]));
    const newName = `${organization.name}-renamed`;

    await test.step("act: rename organization", () => organizations.update({ ...organization, name: newName }));

    await test.step("assert: organization has the new name", async () => {
      expect((await organizations.get(organization.id)).name).toBe(newName);
    });
  });

  test("rename organizations in bulk", async ({ httpClient, cleanupStack }) => {
    const { organizations } = new CustomersClient(httpClient);
    const created = await test.step("arrange: two organizations", () =>
      Promise.all([organizations.create(newOrganization()), organizations.create(newOrganization())]));
    const ids = created.map(({ id }) => id);
    cleanupStack.push(`delete organizations ${ids.join(", ")}`, () => organizations.delete(ids));
    const renamed = created.map((organization) => ({ ...organization, name: `${organization.name}-renamed` }));

    await test.step("act: rename both organizations", () => organizations.updateMany(renamed));

    await test.step("assert: both organizations have new names", async () => {
      const reloaded = await organizations.getMany(ids);
      expect(reloaded.map(({ name }) => name).sort()).toEqual(renamed.map(({ name }) => name).sort());
    });
  });

  test("create, rename and delete an organization", async ({ httpClient, cleanupStack }) => {
    const { organizations } = new CustomersClient(httpClient);
    const draft = newOrganization();
    const newName = `${draft.name}-renamed`;

    const organization = await test.step("act: create organization", () => organizations.create(draft));
    cleanupStack.push(`delete organization ${organization.id}`, () => organizations.delete([organization.id]));
    await test.step("assert: organization is readable", async () => {
      expect((await organizations.get(organization.id)).name).toBe(draft.name);
    });

    await test.step("act: rename organization", () => organizations.update({ ...organization, name: newName }));
    await test.step("assert: organization has the new name", async () => {
      expect((await organizations.get(organization.id)).name).toBe(newName);
    });

    await test.step("act: delete organization", () => organizations.delete([organization.id]));
    await test.step("assert: organization is not found", async () => {
      expect(await organizations.search({ objectIds: [organization.id] })).toEqual([]);
    });
  });

  test("create, rename and delete organizations in bulk", async ({ httpClient, cleanupStack }) => {
    const { organizations } = new CustomersClient(httpClient);
    const drafts = [newOrganization(), newOrganization()];
    const ids = drafts.map(({ id }) => id);
    cleanupStack.push(`delete organizations ${ids.join(", ")}`, () => organizations.delete(ids));

    await test.step("act: create two organizations", () => organizations.createMany(drafts));
    const created = await test.step("assert: both organizations exist", async () => {
      const found = await organizations.getMany(ids);
      expect(found).toHaveLength(2);
      return found;
    });

    await test.step("act: rename both organizations", () =>
      organizations.updateMany(
        created.map((organization) => ({ ...organization, name: `${organization.name}-renamed` })),
      ));
    await test.step("assert: both organizations have new names", async () => {
      expect((await organizations.getMany(ids)).every(({ name }) => name.endsWith("-renamed"))).toBe(true);
    });

    await test.step("act: delete both organizations", () => organizations.delete(ids));
    await test.step("assert: neither organization is found", async () => {
      expect(await organizations.search({ objectIds: ids })).toEqual([]);
    });
  });

  test("delete organizations in bulk", async ({ httpClient, cleanupStack }) => {
    const { organizations } = new CustomersClient(httpClient);
    const created = await test.step("arrange: two organizations", () =>
      Promise.all([organizations.create(newOrganization()), organizations.create(newOrganization())]));
    const ids = created.map(({ id }) => id);
    cleanupStack.push(`delete organizations ${ids.join(", ")}`, () => organizations.delete(ids));

    await test.step("act: delete both organizations", () => organizations.delete(ids));

    await test.step("assert: neither organization is found", async () => {
      expect(await organizations.search({ objectIds: ids })).toEqual([]);
    });
  });
});
