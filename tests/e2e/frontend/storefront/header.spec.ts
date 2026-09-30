import * as allure from "allure-js-commons";

import { saveMemberAddress } from "@dataset/arrange/contact";
import { newMemberAddress, TEST_ADDRESS } from "@dataset/builders/address";
import { expect, test } from "@fixtures";
import { EditAddressModal } from "@pages/frontend/components/edit-address-modal";
import { HomePage } from "@pages/frontend/pages/simple-pages";

const TARGET_CURRENCY = "EUR";
const TARGET_CULTURE = "de-DE";
const TARGET_LANGUAGE_LABEL = "de";

test.beforeEach(async () => {
  await allure.feature("Storefront / Header (E2E)");
});

test.describe("top header (anonymous)", () => {
  test("switch the currency", async ({ page }) => {
    const { currencySelector } = new HomePage(page).topHeader;

    await test.step("arrange: open the home page", () => new HomePage(page).navigate());
    await test.step(`act: select ${TARGET_CURRENCY}`, () => currencySelector.select(TARGET_CURRENCY));

    await test.step(`assert: the current currency is ${TARGET_CURRENCY}`, async () => {
      await expect(currencySelector.currentLabel).toHaveText(TARGET_CURRENCY);
    });
  });

  test("switch the language", async ({ page }) => {
    const { languageSelector } = new HomePage(page).topHeader;

    await test.step("arrange: open the home page", () => new HomePage(page).navigate());
    await test.step(`act: select ${TARGET_CULTURE}`, () => languageSelector.select(TARGET_CULTURE));

    await test.step(`assert: the current language is ${TARGET_LANGUAGE_LABEL}`, async () => {
      await expect(languageSelector.currentLabel).toHaveText(TARGET_LANGUAGE_LABEL);
    });
  });

  test("add a shipping address from the ship-to selector", async ({ page }) => {
    const homePage = new HomePage(page);
    const { topHeader } = homePage;
    const editAddressModal = new EditAddressModal(page);

    await test.step("arrange: open the home page", () => homePage.navigate());

    await test.step("act: add a new address", async () => {
      await topHeader.addShippingAddressButton.click();
      await editAddressModal.addressForm.fill(TEST_ADDRESS);
      await editAddressModal.submitButton.click();
    });

    await test.step("assert: the ship-to selector shows the new address", async () => {
      await expect(topHeader.addShippingAddressButton).toBeHidden();
      for (const part of [
        TEST_ADDRESS.city,
        TEST_ADDRESS.countryName,
        TEST_ADDRESS.regionName,
        TEST_ADDRESS.postalCode,
        TEST_ADDRESS.line1,
      ]) {
        await expect(topHeader.shipToSelector.selectedAddressLabel).toContainText(part);
      }
    });
  });
});

test.describe("top header (customer account)", () => {
  test.use({ shopperAccount: "customer-account" });

  test("pick a saved address from the ship-to selector", async ({ page, customerAccount }) => {
    const address = await test.step("arrange: a saved organization address", () =>
      saveMemberAddress(
        customerAccount.graphqlClient,
        customerAccount.organizationId,
        newMemberAddress("test-ship-to"),
      ));
    const homePage = new HomePage(page);
    const { shipToSelector } = homePage.topHeader;

    await test.step("arrange: open the ship-to selector", async () => {
      await homePage.navigate();
      await shipToSelector.root.click();
      await expect(shipToSelector.addressesList).toBeVisible();
    });

    await test.step(`act: pick ${address.line1}`, () => shipToSelector.address({ line1: address.line1 }).click());

    await test.step("assert: the saved address is selected", async () => {
      await expect(shipToSelector.selectedAddressLabel).toContainText(address.line1);
    });
  });
});
