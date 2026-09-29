import { env } from "@config/env";
import { test as base } from "@playwright/test";

export interface WorkerUser {
  readonly username: string;
  readonly password: string;
}

export interface Auth {
  workerUser: WorkerUser;
}

const USER_POOL_SIZE = 9;

export const auth = base.extend<object, Auth>({
  workerUser: [
    async ({}, use, workerInfo): Promise<void> => {
      const index = (workerInfo.parallelIndex % USER_POOL_SIZE) + 1;
      await use({
        username: `acme_store_employee_${String(index)}@acme.com`,
        password: env.usersPassword,
      });
    },
    { scope: "worker" },
  ],
});
