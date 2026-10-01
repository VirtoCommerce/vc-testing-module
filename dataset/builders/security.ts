import type { Credentials } from "@api/auth/credentials";
import type { ApplicationUserData, RoleData } from "@api/rest/types/security";
import type { WithRequired } from "@core/required-fields";

import { uniqueId } from "@core/unique-id";

export type UserDraft = WithRequired<ApplicationUserData, "userName" | "email" | "password">;

export function newPassword(): string {
  return `Test-${crypto.randomUUID().slice(0, 8)}!aA1`;
}

export function newUser(
  storeId: string,
  overrides: Omit<Partial<ApplicationUserData>, "userName" | "email" | "password"> = {},
): UserDraft {
  const userName = `${uniqueId("test-user")}@example.com`;
  return {
    userName,
    email: userName,
    password: newPassword(),
    userType: "Manager",
    storeId,
    status: "Approved",
    emailConfirmed: true,
    roles: [],
    ...overrides,
  };
}

export function credentialsOf(user: UserDraft): Credentials {
  return { username: user.userName, password: user.password };
}

export function newRole(permissionNames: readonly string[] = []): WithRequired<RoleData, "name"> {
  return {
    name: uniqueId("test-role"),
    description: "",
    permissions: permissionNames.map((name) => ({ name })),
  };
}
