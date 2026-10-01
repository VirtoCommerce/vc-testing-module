import type { TokenManager } from "@api/auth/token-manager";
import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { HttpClient } from "@api/http/http-client";
import type { Dataset } from "@dataset/dataset";

import * as allure from "allure-js-commons";

import {
  GetMeDocument,
  GetOrganizationContactsDocument,
  GetUserDocument,
  InviteUserDocument,
  RegisterByInvitationDocument,
  ResetPasswordByTokenDocument,
  SendPasswordResetEmailDocument,
} from "@api/graphql/generated/graphql";
import { CustomersClient } from "@api/rest/clients/customers-client";
import { NotificationsClient } from "@api/rest/clients/notifications-client";
import { UsersClient } from "@api/rest/clients/users-client";
import { uniqueId } from "@core/unique-id";
import { signInGraphqlClient, signInWithoutCache } from "@dataset/arrange/customer-account";
import { registerAccountRemoval } from "@dataset/arrange/security";
import { newPassword } from "@dataset/builders/security";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const INVITED_STATUS = "Invited";
const INVITATION_TIMEOUT_MS = 30_000;
const NOTIFICATION_TIMEOUT_MS = 30_000;
const EMPLOYEE_ROLE_ID = "org-employee";
const STORE_ADMINISTRATOR_USERNAME = "acme_store_administrator@acme.com";
const OTHER_USERNAME = "acme_store_employee_1@acme.com";
const RESET_PASSWORD_NOTIFICATION = "ResetPasswordEmailNotification";
const RESET_PASSWORD_SUBJECT = "Reset password link";

test.beforeEach(async () => {
  await allure.feature("Contacts / Users");
});

test.describe("current user (anonymous)", () => {
  test("get the anonymous user", async ({ graphqlClient }) => {
    const { me } = await test.step("act: get current user", () => graphqlClient.execute(GetMeDocument));

    await test.step("assert: current user is anonymous", async () => {
      expect(me).toMatchObject({ id: expect.any(String), userName: "Anonymous" });
    });
  });
});

test.describe("current user (customer account)", () => {
  test("get the signed-in user", async ({ customerAccount }) => {
    const { me } = await test.step("act: get current user", () => customerAccount.graphqlClient.execute(GetMeDocument));

    await test.step("assert: current user is the customer account", async () => {
      expect(me).toMatchObject({ id: customerAccount.userId, userName: customerAccount.credentials.username });
    });
  });

  test("get the own account by user name", async ({ customerAccount }) => {
    const { username } = customerAccount.credentials;

    const { user } = await test.step(`act: get user ${username}`, () =>
      customerAccount.graphqlClient.execute(GetUserDocument, { userName: username }));

    await test.step("assert: the account is returned", async () => {
      expect(user).toMatchObject({ id: customerAccount.userId, userName: username });
    });
  });

  test("another user's account is forbidden", async ({ customerAccount }) => {
    const response = await test.step(`act: get user ${OTHER_USERNAME}`, () =>
      customerAccount.graphqlClient.executeRaw(GetUserDocument, { userName: OTHER_USERNAME }));

    await test.step("assert: access is denied and no user is returned", async () => {
      expect(response.data?.user).toBeNull();
      expect(response.errors).toEqual([
        expect.objectContaining({ extensions: expect.objectContaining({ code: "Forbidden" }) }),
      ]);
    });
  });
});

test.describe("password reset (customer account)", () => {
  test("reset a password with the token from the reset e-mail", async ({
    customerAccount,
    graphqlClient,
    platformAdminHttpClient,
    anonymousHttpClient,
    frontendContext,
  }) => {
    const { username } = customerAccount.credentials;

    const { sendPasswordResetEmail } = await test.step(`act: request a reset e-mail for ${username}`, () =>
      graphqlClient.execute(SendPasswordResetEmailDocument, {
        command: {
          storeId: frontendContext.storeId,
          cultureName: frontendContext.cultureName,
          loginOrEmail: username,
          urlSuffix: "/reset-password",
        },
      }));
    await test.step("assert: the request is accepted", async () => {
      expect(sendPasswordResetEmail).toBe(true);
    });

    const token = await test.step("assert: a reset e-mail with a token reaches the journal", () =>
      waitForResetToken(new NotificationsClient(platformAdminHttpClient), username));

    const password = newPassword();
    const { resetPasswordByToken } = await test.step("act: reset the password with the e-mailed token", () =>
      graphqlClient.execute(ResetPasswordByTokenDocument, {
        command: { userId: customerAccount.userId, token, newPassword: password },
      }));

    await test.step("assert: the reset succeeded and the new password signs in", async () => {
      expect(resetPasswordByToken).toMatchObject({ succeeded: true, errors: [] });
      const signedIn = await signInWithoutCache(anonymousHttpClient, { username, password }, frontendContext.storeId);
      expect((await signedIn.execute(GetMeDocument)).me?.userName).toBe(username);
    });
  });
});

test.describe("user invitation (store administrator)", () => {
  test.use({ customerAccountRole: "org-maintainer" });

  test("invite a user to the organization", async ({
    customerAccount,
    platformAdminHttpClient,
    anonymousHttpClient,
    tokenManager,
    cleanupStack,
    dataset,
    env,
  }) => {
    const email = `${uniqueId("test-invite")}@example.com`;
    registerAccountRemoval(
      new UsersClient(platformAdminHttpClient),
      new CustomersClient(platformAdminHttpClient),
      cleanupStack,
      email,
    );
    const storeAdministrator = await test.step("arrange: sign in the store administrator", () =>
      signInStoreAdministrator(tokenManager, anonymousHttpClient, dataset, env.storeId));

    const { inviteUser } = await test.step(`act: invite ${email} as an employee`, () =>
      storeAdministrator.execute(InviteUserDocument, {
        command: {
          storeId: env.storeId,
          emails: [email],
          organizationId: customerAccount.organizationId,
          roleIds: [EMPLOYEE_ROLE_ID],
        },
      }));

    await test.step("assert: an invited contact with that account joins the organization", async () => {
      expect(inviteUser?.succeeded).toBe(true);
      await expect
        .poll(
          async () => {
            const { organization } = await customerAccount.graphqlClient.execute(GetOrganizationContactsDocument, {
              organizationId: customerAccount.organizationId,
              searchPhrase: email,
            });
            return (organization?.contacts?.items ?? []).map((contact) => ({
              status: contact?.status,
              userNames: contact?.securityAccounts?.map((account) => account?.userName),
            }));
          },
          { timeout: INVITATION_TIMEOUT_MS },
        )
        .toContainEqual({ status: INVITED_STATUS, userNames: [email] });
    });
  });

  test("register by invitation", async ({
    customerAccount,
    graphqlClient,
    platformAdminHttpClient,
    anonymousHttpClient,
    tokenManager,
    cleanupStack,
    dataset,
    env,
  }) => {
    const email = `${uniqueId("test-invite")}@example.com`;
    const usersClient = new UsersClient(platformAdminHttpClient);
    registerAccountRemoval(usersClient, new CustomersClient(platformAdminHttpClient), cleanupStack, email);
    await test.step(`arrange: invite ${email} as an employee`, async () => {
      const storeAdministrator = await signInStoreAdministrator(
        tokenManager,
        anonymousHttpClient,
        dataset,
        env.storeId,
      );
      const { inviteUser } = await storeAdministrator.execute(InviteUserDocument, {
        command: {
          storeId: env.storeId,
          emails: [email],
          organizationId: customerAccount.organizationId,
          roleIds: [EMPLOYEE_ROLE_ID],
        },
      });
      expect(inviteUser?.succeeded).toBe(true);
    });
    const invited = await test.step("arrange: the invited account and its invitation token", async () => {
      const user = await usersClient.get(email);
      return { user, token: await usersClient.generatePasswordResetToken(user.id) };
    });
    const password = newPassword();

    const { registerByInvitation } = await test.step("act: accept the invitation", () =>
      graphqlClient.execute(RegisterByInvitationDocument, {
        command: {
          userId: invited.user.id,
          username: email,
          password,
          token: invited.token,
          firstName: "Invited",
          lastName: "Employee",
          organizationId: customerAccount.organizationId,
        },
      }));

    await test.step("assert: the registration succeeded and the invited user signs in", async () => {
      expect(registerByInvitation).toMatchObject({ succeeded: true, errors: [] });
      const signedIn = await signInWithoutCache(anonymousHttpClient, { username: email, password }, env.storeId);
      expect((await signedIn.execute(GetMeDocument)).me?.userName).toBe(email);
    });
  });
});

function signInStoreAdministrator(
  tokenManager: TokenManager,
  anonymousHttpClient: HttpClient,
  dataset: Dataset,
  storeId: string,
): Promise<GraphqlClient> {
  return signInGraphqlClient(
    tokenManager,
    anonymousHttpClient,
    getCredentials(dataset, STORE_ADMINISTRATOR_USERNAME),
    storeId,
  );
}

async function waitForResetToken(notificationsClient: NotificationsClient, username: string): Promise<string> {
  async function readToken(): Promise<string | null> {
    const [message] = await notificationsClient.searchJournal({
      notificationType: RESET_PASSWORD_NOTIFICATION,
      keyword: username,
      take: 1,
    });
    return message?.subject?.startsWith(RESET_PASSWORD_SUBJECT) ? resetTokenOf(message.body) : null;
  }

  await expect.poll(readToken, { timeout: NOTIFICATION_TIMEOUT_MS }).not.toBeNull();
  const token = await readToken();
  if (token === null) {
    throw new Error(`No password reset token was e-mailed to ${username}`);
  }
  return token;
}

function resetTokenOf(body: string | null | undefined): string | null {
  const link = body === null || body === undefined ? undefined : /href="([^"]+)"/.exec(body)?.[1];
  return link === undefined ? null : new URL(link).searchParams.get("token");
}
