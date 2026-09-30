import * as allure from "allure-js-commons";

import { SettingsClient } from "@api/rest/clients/settings-client";
import { uniqueId } from "@core/unique-id";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const BOOLEAN_SETTING = "VirtoCommerce.Search.IndexingJobs.Enable";
const BLACKLIST_SETTING = "VirtoCommerce.Platform.Security.FileExtensionsBlackList";
const CATALOG_MODULE_ID = "VirtoCommerce.Catalog";

test.beforeEach(async () => {
  await allure.feature("Platform / Settings");
});

test.describe("platform settings (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("list all settings", async ({ httpClient }) => {
    const settingsClient = new SettingsClient(httpClient);

    const settings = await test.step("act: list settings", () => settingsClient.list());

    await test.step("assert: known setting is listed", async () => {
      expect(settings.map(({ name }) => name)).toContain(BOOLEAN_SETTING);
    });
  });

  test("get a setting by name", async ({ httpClient }) => {
    const settingsClient = new SettingsClient(httpClient);

    const setting = await test.step("act: get setting", () => settingsClient.get(BOOLEAN_SETTING));

    await test.step("assert: setting is a boolean", async () => {
      expect(setting).toMatchObject({ name: BOOLEAN_SETTING, valueType: "Boolean" });
    });
  });

  test("list the settings of a module", async ({ httpClient }) => {
    const settingsClient = new SettingsClient(httpClient);

    const settings = await test.step("act: list catalog settings", () =>
      settingsClient.listByModule(CATALOG_MODULE_ID));

    await test.step("assert: only catalog settings are listed", async () => {
      expect(settings.length).toBeGreaterThan(0);
      expect(new Set(settings.map(({ moduleId }) => moduleId))).toEqual(new Set([CATALOG_MODULE_ID]));
    });
  });

  test("get the UI customization setting", async ({ httpClient }) => {
    const settingsClient = new SettingsClient(httpClient);

    const setting = await test.step("act: get UI customization", () => settingsClient.getUiCustomization());

    await test.step("assert: setting belongs to the platform", async () => {
      expect(setting.moduleId).toBe("Platform");
    });
  });

  test.describe("changing global settings", () => {
    test.describe.configure({ mode: "default" });

    test("toggle a boolean setting", async ({ httpClient, cleanupStack }) => {
      const settingsClient = new SettingsClient(httpClient);
      const original = await test.step("arrange: current value", () => settingsClient.get(BOOLEAN_SETTING));
      cleanupStack.push(`restore setting ${BOOLEAN_SETTING}`, () => settingsClient.save([original]));
      const toggled = !(original.value ?? original.defaultValue);

      await test.step(`act: set ${BOOLEAN_SETTING} to ${toggled}`, () =>
        settingsClient.save([{ ...original, value: toggled }]));

      await test.step("assert: setting has the new value", async () => {
        expect((await settingsClient.get(BOOLEAN_SETTING)).value).toBe(toggled);
      });
    });

    test("add a file extension to the blacklist", async ({ httpClient, cleanupStack }) => {
      const settingsClient = new SettingsClient(httpClient);
      const original = await test.step("arrange: current blacklist", () => settingsClient.get(BLACKLIST_SETTING));
      cleanupStack.push(`restore setting ${BLACKLIST_SETTING}`, () => settingsClient.save([original]));
      const extension = `.${uniqueId("qa")}`;

      await test.step(`act: blacklist ${extension}`, () =>
        settingsClient.save([{ ...original, allowedValues: [...(original.allowedValues ?? []), extension] }]));

      await test.step("assert: extension is blacklisted", async () => {
        expect((await settingsClient.get(BLACKLIST_SETTING)).allowedValues).toContain(extension);
      });
    });
  });
});
