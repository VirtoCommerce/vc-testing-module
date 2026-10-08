import type { Credentials } from "@api/auth/credentials";
import type { TokenManager } from "@api/auth/token-manager";
import type { HttpClient } from "@api/http/http-client";
import type { OrganizationMembership } from "@api/rest/types/memberships";
import type { CleanupStack } from "@core/cleanup-stack";
import type { FrontendContext } from "../frontend-context";

import { authHeader, TokenAuthClient } from "@api/auth/token-auth-client";
import { GraphqlClient } from "@api/graphql/graphql-client";
import { CustomersClient } from "@api/rest/clients/customers-client";
import { OrganizationMembershipsClient } from "@api/rest/clients/organization-memberships-client";
import { UsersClient } from "@api/rest/clients/users-client";

import { newContact, newOrganization } from "../builders/customer";
import { credentialsOf, newUser } from "../builders/security";
import { arrangeUser } from "./security";

const ORGANIZATION_ROLE_NAMES = {
  "org-employee": "Organization employee",
  "org-maintainer": "Organization maintainer",
} as const;

export type OrganizationRole = keyof typeof ORGANIZATION_ROLE_NAMES;

export interface CustomerAccount {
  readonly credentials: Credentials;
  readonly userId: string;
  readonly contactId: string;
  readonly organizationId: string;
}

export interface CustomerAccountOptions {
  readonly storeId: string;
  readonly role: OrganizationRole;
  readonly organizationId?: string;
}

export async function arrangeCustomerAccount(
  platformAdminHttpClient: HttpClient,
  cleanupStack: CleanupStack,
  options: CustomerAccountOptions,
): Promise<CustomerAccount> {
  const customersClient = new CustomersClient(platformAdminHttpClient);
  const organizationId = options.organizationId ?? (await arrangeOrganizationWith(customersClient, cleanupStack));
  const contact = { ...newContact([organizationId]), defaultOrganizationId: organizationId };
  cleanupStack.push(`delete contact ${contact.id}`, () => customersClient.contacts.delete([contact.id]));
  await customersClient.contacts.create(contact);
  const draft = newUser(options.storeId, {
    userType: "Customer",
    memberId: contact.id,
    roles: [{ id: options.role, name: ORGANIZATION_ROLE_NAMES[options.role] }],
  });
  const user = await arrangeUser(new UsersClient(platformAdminHttpClient), cleanupStack, draft);
  const membershipsClient = new OrganizationMembershipsClient(platformAdminHttpClient);
  const membership =
    (await membershipsClient.find(user.id, organizationId)) ??
    (await membershipsClient.create({ userId: user.id, organizationId, roles: [{ roleId: options.role }] }));
  cleanupStack.push(`delete membership ${membership.id}`, () => membershipsClient.delete([membership.id]));
  return { credentials: credentialsOf(draft), userId: user.id, contactId: contact.id, organizationId };
}

export async function signInGraphqlClient(
  tokenManager: TokenManager,
  anonymousHttpClient: HttpClient,
  credentials: Credentials,
  storeId: string,
): Promise<GraphqlClient> {
  return new GraphqlClient(await tokenManager.authorize(anonymousHttpClient, credentials, storeId));
}

export async function signInWithoutCache(
  anonymousHttpClient: HttpClient,
  credentials: Credentials,
  storeId: string,
): Promise<GraphqlClient> {
  const token = await new TokenAuthClient(anonymousHttpClient).requestToken(credentials, storeId);
  return new GraphqlClient(anonymousHttpClient.withHeaders(authHeader(token)));
}

export async function addOrganizationMembership(
  platformAdminHttpClient: HttpClient,
  cleanupStack: CleanupStack,
  account: CustomerAccount,
  organizationId: string,
): Promise<OrganizationMembership> {
  const { contacts } = new CustomersClient(platformAdminHttpClient);
  const contact = await contacts.get(account.contactId);
  await contacts.update({ ...contact, organizations: [...(contact.organizations ?? []), organizationId] });
  const membershipsClient = new OrganizationMembershipsClient(platformAdminHttpClient);
  const membership = await membershipsClient.create({ userId: account.userId, organizationId });
  cleanupStack.push(`delete membership ${membership.id}`, () => membershipsClient.delete([membership.id]));
  return membership;
}

export async function arrangeOrganization(
  platformAdminHttpClient: HttpClient,
  cleanupStack: CleanupStack,
  name?: string,
): Promise<string> {
  return arrangeOrganizationWith(new CustomersClient(platformAdminHttpClient), cleanupStack, name);
}

export function customerAccountContext(context: FrontendContext, account: CustomerAccount): FrontendContext {
  return {
    ...context,
    userId: account.userId,
    userName: account.credentials.username,
    contactId: account.contactId,
    organizationId: account.organizationId,
  };
}

async function arrangeOrganizationWith(
  customersClient: CustomersClient,
  cleanupStack: CleanupStack,
  name?: string,
): Promise<string> {
  const organization = newOrganization(name);
  cleanupStack.push(`delete organization ${organization.id}`, () =>
    customersClient.organizations.delete([organization.id]),
  );
  await customersClient.organizations.create(organization);
  return organization.id;
}
