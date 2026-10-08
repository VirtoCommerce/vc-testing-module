import type { HttpClient } from "../../http/http-client";
import type {
  ContactData,
  CustomerAddress,
  EmployeeData,
  Member,
  MemberBaseData,
  MemberData,
  MembersSearchCriteria,
  OrganizationData,
  VendorData,
  VendorSearchResult,
} from "../types/customers";

import { requireFields } from "@core/required-fields";

import { MEMBER_FIELDS } from "../types/customers";

export class MemberResource<Data extends MemberBaseData> {
  readonly #httpClient: HttpClient;
  readonly #path: string;
  readonly #label: string;

  constructor(httpClient: HttpClient, path: string, label: string) {
    this.#httpClient = httpClient;
    this.#path = path;
    this.#label = label;
  }

  async get(id: string): Promise<Member<Data>> {
    return requireFields(await this.find(id), MEMBER_FIELDS, `${this.#label} "${id}"`);
  }

  async find(id: string): Promise<Member<Data> | undefined> {
    const response = (await this.#httpClient.get(`${this.#path}/${encodeURIComponent(id)}`)).expectOk();
    const member = response.text === "" ? null : response.json<Data | null>();
    return member === null ? undefined : requireFields(member, MEMBER_FIELDS, `${this.#label} "${id}"`);
  }

  async getMany(ids: readonly string[]): Promise<Member<Data>[]> {
    const response = await this.#httpClient.get(this.#path, { query: { ids } });
    return response
      .expectOk()
      .json<Data[]>()
      .map((member) => requireFields(member, MEMBER_FIELDS, this.#label));
  }

  async create(member: Data): Promise<Member<Data>> {
    const response = await this.#httpClient.post(this.#path, { json: member });
    return requireFields(response.expectOk().json<Data>(), MEMBER_FIELDS, `Created ${this.#label}`);
  }

  async createMany(members: Data[]): Promise<void> {
    (await this.#httpClient.post(`${this.#path}/bulk`, { json: members })).expectOk();
  }

  async update(member: Data): Promise<void> {
    (await this.#httpClient.put(this.#path, { json: member })).expectOk();
  }

  async updateMany(members: Data[]): Promise<void> {
    (await this.#httpClient.put(`${this.#path}/bulk`, { json: members })).expectOk();
  }

  async search(criteria: MembersSearchCriteria): Promise<Member<Data>[]> {
    const response = await this.#httpClient.post(`${this.#path}/search`, { json: criteria });
    const { results } = response.expectOk().json<{ results?: Data[] | null }>();
    return (results ?? []).map((member) => requireFields(member, MEMBER_FIELDS, `Found ${this.#label}`));
  }

  async delete(ids: readonly string[]): Promise<void> {
    (await this.#httpClient.delete(this.#path, { query: { ids } })).expectOk();
  }
}

export class CustomersClient {
  readonly contacts: MemberResource<ContactData>;
  readonly organizations: MemberResource<OrganizationData>;
  readonly members: MemberResource<MemberData>;
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
    this.contacts = new MemberResource(httpClient, "/api/contacts", "Contact");
    this.organizations = new MemberResource(httpClient, "/api/organizations", "Organization");
    this.members = new MemberResource(httpClient, "/api/members", "Member");
  }

  async deleteMatchingMembers(criteria: MembersSearchCriteria): Promise<void> {
    (await this.#httpClient.post("/api/members/delete", { json: criteria })).expectOk();
  }

  async getOrganizationsOf(memberId: string): Promise<Member<OrganizationData>[]> {
    const response = await this.#httpClient.get(`/api/members/${encodeURIComponent(memberId)}/organizations`);
    return response
      .expectOk()
      .json<OrganizationData[]>()
      .map((organization) => requireFields(organization, MEMBER_FIELDS, `Organization of "${memberId}"`));
  }

  async listOrganizations(): Promise<Member<OrganizationData>[]> {
    const response = await this.#httpClient.get("/api/members/organizations");
    return response
      .expectOk()
      .json<OrganizationData[]>()
      .map((organization) => requireFields(organization, MEMBER_FIELDS, "Organization"));
  }

  async createEmployee(employee: EmployeeData): Promise<Member<EmployeeData>> {
    const response = await this.#httpClient.post("/api/employees", { json: employee });
    return requireFields(response.expectOk().json<EmployeeData>(), MEMBER_FIELDS, "Created employee");
  }

  async getEmployees(ids: readonly string[]): Promise<Member<EmployeeData>[]> {
    const response = await this.#httpClient.get("/api/employees", { query: { ids } });
    return response
      .expectOk()
      .json<EmployeeData[]>()
      .map((employee) => requireFields(employee, MEMBER_FIELDS, "Employee"));
  }

  async saveEmployees(employees: EmployeeData[]): Promise<void> {
    (await this.#httpClient.post("/api/employees/bulk", { json: employees })).expectOk();
  }

  async searchVendors(criteria: MembersSearchCriteria): Promise<Member<VendorData>[]> {
    const response = await this.#httpClient.post("/api/vendors/search", { json: criteria });
    const { results } = response.expectOk().json<VendorSearchResult>();
    return (results ?? []).map((vendor) => requireFields(vendor, MEMBER_FIELDS, "Found vendor"));
  }

  async saveAddresses(memberId: string, addresses: CustomerAddress[]): Promise<void> {
    (await this.#httpClient.put("/api/addresses", { query: { memberId }, json: addresses })).expectOk();
  }
}
