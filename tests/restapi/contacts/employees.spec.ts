import * as allure from "allure-js-commons";

import { CustomersClient } from "@api/rest/clients/customers-client";
import { newEmployee } from "@dataset/builders/customer";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Contacts / Employees");
});

test.describe("employees (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create an employee", async ({ httpClient, cleanupStack }) => {
    const customersClient = new CustomersClient(httpClient);
    const draft = newEmployee();

    const employee = await test.step("act: create employee", () => customersClient.createEmployee(draft));
    cleanupStack.push(`delete employee ${employee.id}`, () => customersClient.members.delete([employee.id]));

    await test.step("assert: employee has its names", async () => {
      expect(employee).toMatchObject({ memberType: "Employee", firstName: draft.firstName, lastName: draft.lastName });
    });
  });

  test("get an employee by id", async ({ httpClient, cleanupStack }) => {
    const customersClient = new CustomersClient(httpClient);
    const employee = await test.step("arrange: employee", () => customersClient.createEmployee(newEmployee()));
    cleanupStack.push(`delete employee ${employee.id}`, () => customersClient.members.delete([employee.id]));

    const found = await test.step("act: get employee", () => customersClient.getEmployees([employee.id]));

    await test.step("assert: employee is returned", async () => {
      expect(found.map(({ id }) => id)).toEqual([employee.id]);
    });
  });

  test("search employees by id", async ({ httpClient, cleanupStack }) => {
    const customersClient = new CustomersClient(httpClient);
    const employee = await test.step("arrange: employee", () => customersClient.createEmployee(newEmployee()));
    cleanupStack.push(`delete employee ${employee.id}`, () => customersClient.members.delete([employee.id]));

    const found = await test.step("act: search employees by id", () =>
      customersClient.members.search({ memberType: "Employee", objectIds: [employee.id] }));

    await test.step("assert: employee is found", async () => {
      expect(found.map(({ id }) => id)).toEqual([employee.id]);
    });
  });

  test("rename employees in bulk", async ({ httpClient, cleanupStack }) => {
    const customersClient = new CustomersClient(httpClient);
    const created = await test.step("arrange: two employees", () =>
      Promise.all([customersClient.createEmployee(newEmployee()), customersClient.createEmployee(newEmployee())]));
    const ids = created.map(({ id }) => id);
    cleanupStack.push(`delete employees ${ids.join(", ")}`, () => customersClient.members.delete(ids));
    const renamed = created.map((employee) => ({ ...employee, firstName: `${employee.firstName}-renamed` }));

    await test.step("act: save both employees", () => customersClient.saveEmployees(renamed));

    await test.step("assert: both employees have new first names", async () => {
      const reloaded = await customersClient.getEmployees(ids);
      expect(reloaded.map(({ firstName }) => firstName).sort()).toEqual(
        renamed.map(({ firstName }) => firstName).sort(),
      );
    });
  });

  test("delete employees in bulk", async ({ httpClient, cleanupStack }) => {
    const customersClient = new CustomersClient(httpClient);
    const created = await test.step("arrange: two employees", () =>
      Promise.all([customersClient.createEmployee(newEmployee()), customersClient.createEmployee(newEmployee())]));
    const ids = created.map(({ id }) => id);
    cleanupStack.push(`delete employees ${ids.join(", ")}`, () => customersClient.members.delete(ids));

    await test.step("act: delete both employees", () => customersClient.members.delete(ids));

    await test.step("assert: neither employee is found", async () => {
      expect(await customersClient.members.search({ memberType: "Employee", objectIds: ids })).toEqual([]);
    });
  });
});
