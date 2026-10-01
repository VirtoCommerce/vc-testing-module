import type { TokenManager } from "@api/auth/token-manager";
import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { HttpClient } from "@api/http/http-client";
import type { CleanupStack } from "@core/cleanup-stack";
import type { Env } from "@core/env";
import type { CustomerAccount, OrganizationRole } from "@dataset/arrange/customer-account";
import type { Dataset } from "@dataset/dataset";
import type { FrontendContext } from "@dataset/frontend-context";

import { mergeTests } from "@playwright/test";

import { arrangeCustomerAccount, customerAccountContext, signInGraphqlClient } from "@dataset/arrange/customer-account";
import { getFrontendContext } from "@dataset/frontend-context";

import { test as cleanupTest } from "./cleanup.fixture";
import { test as datasetTest } from "./dataset.fixture";

export interface SignedInCustomerAccount extends CustomerAccount {
  readonly graphqlClient: GraphqlClient;
  readonly context: FrontendContext;
}

export type ShopperAccount = "user" | "customer-account";

export interface CustomerAccountOptions {
  readonly customerAccountRole: OrganizationRole;
  readonly customerAccountOrganizationId: string | undefined;
  readonly shopperAccount: ShopperAccount;
}

export interface CustomerAccountFixtures {
  readonly browserCustomerAccount: SignedInCustomerAccount | undefined;
  readonly customerAccount: SignedInCustomerAccount;
}

interface CustomerAccountDependencies {
  readonly platformAdminHttpClient: HttpClient;
  readonly anonymousHttpClient: HttpClient;
  readonly tokenManager: TokenManager;
  readonly cleanupStack: CleanupStack;
  readonly dataset: Dataset;
  readonly env: Env;
  readonly anonymousUserId: string;
  readonly customerAccountRole: OrganizationRole;
  readonly customerAccountOrganizationId: string | undefined;
}

export const test = mergeTests(cleanupTest, datasetTest).extend<CustomerAccountOptions & CustomerAccountFixtures>({
  customerAccountRole: ["org-employee", { option: true }],
  customerAccountOrganizationId: [undefined, { option: true }],
  shopperAccount: ["user", { option: true }],

  browserCustomerAccount: async (
    {
      shopperAccount,
      platformAdminHttpClient,
      anonymousHttpClient,
      tokenManager,
      cleanupStack,
      dataset,
      env,
      anonymousUserId,
      customerAccountRole,
      customerAccountOrganizationId,
    },
    use,
  ) => {
    await use(
      shopperAccount === "customer-account"
        ? await openCustomerAccount({
            platformAdminHttpClient,
            anonymousHttpClient,
            tokenManager,
            cleanupStack,
            dataset,
            env,
            anonymousUserId,
            customerAccountRole,
            customerAccountOrganizationId,
          })
        : undefined,
    );
  },

  customerAccount: async (
    {
      browserCustomerAccount,
      platformAdminHttpClient,
      anonymousHttpClient,
      tokenManager,
      cleanupStack,
      dataset,
      env,
      anonymousUserId,
      customerAccountRole,
      customerAccountOrganizationId,
    },
    use,
  ) => {
    await use(
      browserCustomerAccount ??
        (await openCustomerAccount({
          platformAdminHttpClient,
          anonymousHttpClient,
          tokenManager,
          cleanupStack,
          dataset,
          env,
          anonymousUserId,
          customerAccountRole,
          customerAccountOrganizationId,
        })),
    );
  },
});

async function openCustomerAccount(dependencies: CustomerAccountDependencies): Promise<SignedInCustomerAccount> {
  const { env, customerAccountOrganizationId } = dependencies;
  const account = await arrangeCustomerAccount(dependencies.platformAdminHttpClient, dependencies.cleanupStack, {
    storeId: env.storeId,
    role: dependencies.customerAccountRole,
    ...(customerAccountOrganizationId === undefined ? {} : { organizationId: customerAccountOrganizationId }),
  });
  const graphqlClient = await signInGraphqlClient(
    dependencies.tokenManager,
    dependencies.anonymousHttpClient,
    account.credentials,
    env.storeId,
  );
  const storeContext = getFrontendContext(dependencies.dataset, env.storeId, undefined, dependencies.anonymousUserId);
  return { ...account, graphqlClient, context: customerAccountContext(storeContext, account) };
}
