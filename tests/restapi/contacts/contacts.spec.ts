import * as allure from "allure-js-commons";

import { CustomersClient } from "@api/rest/clients/customers-client";
import { newAddress, newContact } from "@dataset/builders/customer";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Contacts / Contacts");
});

test.describe("contacts (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create a contact", async ({ httpClient, cleanupStack }) => {
    const { contacts } = new CustomersClient(httpClient);
    const draft = newContact();

    const contact = await test.step("act: create contact", () => contacts.create(draft));
    cleanupStack.push(`delete contact ${contact.id}`, () => contacts.delete([contact.id]));

    await test.step("assert: contact has its names", async () => {
      expect(contact).toMatchObject({ memberType: "Contact", firstName: draft.firstName, lastName: draft.lastName });
    });
  });

  test("get a contact by id", async ({ httpClient, cleanupStack }) => {
    const { contacts } = new CustomersClient(httpClient);
    const contact = await test.step("arrange: contact", () => contacts.create(newContact()));
    cleanupStack.push(`delete contact ${contact.id}`, () => contacts.delete([contact.id]));

    const reloaded = await test.step("act: get contact", () => contacts.get(contact.id));

    await test.step("assert: fields match the created contact", async () => {
      expect(reloaded).toMatchObject({ id: contact.id, firstName: contact.firstName, lastName: contact.lastName });
    });
  });

  test("rename a contact", async ({ httpClient, cleanupStack }) => {
    const { contacts } = new CustomersClient(httpClient);
    const contact = await test.step("arrange: contact", () => contacts.create(newContact()));
    cleanupStack.push(`delete contact ${contact.id}`, () => contacts.delete([contact.id]));
    const firstName = `${contact.firstName}-renamed`;

    await test.step("act: change first name", () => contacts.update({ ...contact, firstName }));

    await test.step("assert: contact has the new first name", async () => {
      expect((await contacts.get(contact.id)).firstName).toBe(firstName);
    });
  });

  test("search contacts by id", async ({ httpClient, cleanupStack }) => {
    const { contacts } = new CustomersClient(httpClient);
    const contact = await test.step("arrange: contact", () => contacts.create(newContact()));
    cleanupStack.push(`delete contact ${contact.id}`, () => contacts.delete([contact.id]));

    const found = await test.step("act: search by contact id", () =>
      contacts.search({ objectIds: [contact.id], deepSearch: true }));

    await test.step("assert: contact is found", async () => {
      expect(found.map(({ id }) => id)).toEqual([contact.id]);
    });
  });

  test("delete a contact", async ({ httpClient, cleanupStack }) => {
    const { contacts } = new CustomersClient(httpClient);
    const contact = await test.step("arrange: contact", () => contacts.create(newContact()));
    cleanupStack.push(`delete contact ${contact.id}`, () => contacts.delete([contact.id]));

    await test.step("act: delete contact", () => contacts.delete([contact.id]));

    await test.step("assert: contact is not found", async () => {
      expect(await contacts.find(contact.id)).toBeUndefined();
      expect(await contacts.search({ objectIds: [contact.id] })).toEqual([]);
    });
  });

  test("create contacts in bulk", async ({ httpClient, cleanupStack }) => {
    const { contacts } = new CustomersClient(httpClient);
    const drafts = [newContact(), newContact()];
    const ids = drafts.map(({ id }) => id);
    cleanupStack.push(`delete contacts ${ids.join(", ")}`, () => contacts.delete(ids));

    await test.step("act: create two contacts", () => contacts.createMany(drafts));

    await test.step("assert: both contacts exist", async () => {
      expect((await contacts.getMany(ids)).map(({ name }) => name).sort()).toEqual(
        drafts.map(({ name }) => name).sort(),
      );
    });
  });

  test("get contacts by ids", async ({ httpClient, cleanupStack }) => {
    const { contacts } = new CustomersClient(httpClient);
    const created = await test.step("arrange: two contacts", () =>
      Promise.all([contacts.create(newContact()), contacts.create(newContact())]));
    const ids = created.map(({ id }) => id);
    cleanupStack.push(`delete contacts ${ids.join(", ")}`, () => contacts.delete(ids));

    const found = await test.step("act: get contacts by ids", () => contacts.getMany(ids));

    await test.step("assert: both contacts are returned", async () => {
      expect(found.map(({ id }) => id).sort()).toEqual([...ids].sort());
    });
  });

  test("rename contacts in bulk", async ({ httpClient, cleanupStack }) => {
    const { contacts } = new CustomersClient(httpClient);
    const created = await test.step("arrange: two contacts", () =>
      Promise.all([contacts.create(newContact()), contacts.create(newContact())]));
    const ids = created.map(({ id }) => id);
    cleanupStack.push(`delete contacts ${ids.join(", ")}`, () => contacts.delete(ids));
    const renamed = created.map((contact) => ({ ...contact, firstName: `${contact.firstName}-renamed` }));

    await test.step("act: rename both contacts", () => contacts.updateMany(renamed));

    await test.step("assert: both contacts have new first names", async () => {
      const reloaded = await contacts.getMany(ids);
      expect(reloaded.map(({ firstName }) => firstName).sort()).toEqual(
        renamed.map(({ firstName }) => firstName).sort(),
      );
    });
  });

  test("delete contacts in bulk", async ({ httpClient, cleanupStack }) => {
    const { contacts } = new CustomersClient(httpClient);
    const created = await test.step("arrange: two contacts", () =>
      Promise.all([contacts.create(newContact()), contacts.create(newContact())]));
    const ids = created.map(({ id }) => id);
    cleanupStack.push(`delete contacts ${ids.join(", ")}`, () => contacts.delete(ids));

    await test.step("act: delete both contacts", () => contacts.delete(ids));

    await test.step("assert: neither contact is found", async () => {
      expect(await contacts.search({ objectIds: ids })).toEqual([]);
    });
  });

  test("add an address to a contact", async ({ httpClient, cleanupStack }) => {
    const customersClient = new CustomersClient(httpClient);
    const contact = await test.step("arrange: contact", () => customersClient.contacts.create(newContact()));
    cleanupStack.push(`delete contact ${contact.id}`, () => customersClient.contacts.delete([contact.id]));
    const address = newAddress();

    await test.step("act: save contact address", () => customersClient.saveAddresses(contact.id, [address]));

    await test.step("assert: contact has the address", async () => {
      expect((await customersClient.contacts.get(contact.id)).addresses).toEqual([
        expect.objectContaining({ line1: address.line1, city: address.city, countryCode: address.countryCode }),
      ]);
    });
  });

  test("get a missing contact", async ({ httpClient }) => {
    const { contacts } = new CustomersClient(httpClient);

    const contact = await test.step("act: get contact by a missing id", () => contacts.find(crypto.randomUUID()));

    await test.step("assert: contact is not found", async () => {
      expect(contact).toBeUndefined();
    });
  });
});
