import * as allure from "allure-js-commons";

import { PlatformClient } from "@api/rest/clients/platform-client";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Platform / Notifications");
});

test.describe("push notifications (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("search push notifications", async ({ httpClient }) => {
    const platformClient = new PlatformClient(httpClient);

    const result = await test.step("act: search notifications", () =>
      platformClient.searchPushNotifications({ take: 20 }));

    await test.step("assert: result reports counts and events", async () => {
      expect(result).toMatchObject({ totalCount: expect.any(Number), newCount: expect.any(Number) });
      expect(Array.isArray(result.notifyEvents)).toBe(true);
    });
  });

  test("mark all push notifications as read", async ({ httpClient }) => {
    const platformClient = new PlatformClient(httpClient);

    await test.step("act: mark all notifications as read", () => platformClient.markAllPushNotificationsAsRead());

    await test.step("assert: no notification is new", async () => {
      expect((await platformClient.searchPushNotifications({ take: 1 })).newCount).toBe(0);
    });
  });
});
