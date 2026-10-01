import type { CustomersClient } from "@api/rest/clients/customers-client";
import type { UsersClient } from "@api/rest/clients/users-client";
import type { ApplicationUser, UserApiKey } from "@api/rest/types/security";
import type { CleanupStack } from "@core/cleanup-stack";
import type { UserDraft } from "../builders/security";

import { USER_API_KEY_FIELDS } from "@api/rest/types/security";
import { requireFields } from "@core/required-fields";

export async function arrangeUser(
  usersClient: UsersClient,
  cleanupStack: CleanupStack,
  draft: UserDraft,
): Promise<ApplicationUser> {
  cleanupStack.push(`delete user ${draft.userName}`, () => usersClient.delete([draft.userName]));
  const result = await usersClient.create(draft);
  if (result.succeeded !== true) {
    throw new Error(`Cannot create user ${draft.userName}: ${JSON.stringify(result.errors)}`);
  }
  return usersClient.get(draft.userName);
}

export async function arrangeApiKey(
  usersClient: UsersClient,
  cleanupStack: CleanupStack,
  user: ApplicationUser,
  apiKey: string,
): Promise<UserApiKey & { apiKey: string }> {
  await usersClient.createApiKey({ userId: user.id, userName: user.userName, apiKey, isActive: true });
  const created = (await usersClient.listApiKeys(user.id)).find((key) => key.apiKey === apiKey);
  const key = requireFields(created, [...USER_API_KEY_FIELDS, "apiKey"], `API key of ${user.userName}`);
  cleanupStack.push(`delete API key ${key.id}`, async () => {
    if ((await usersClient.listApiKeys(user.id)).some(({ id }) => id === key.id)) {
      await usersClient.deleteApiKeys([key.id]);
    }
  });
  return key;
}

export function registerAccountRemoval(
  usersClient: UsersClient,
  customersClient: CustomersClient,
  cleanupStack: CleanupStack,
  userName: string,
): void {
  cleanupStack.push(`delete account ${userName} and its contact`, async () => {
    const user = await usersClient.find(userName);
    await usersClient.delete([userName]);
    if (user?.memberId) {
      await customersClient.contacts.delete([user.memberId]);
    }
  });
}
