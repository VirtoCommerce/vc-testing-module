import * as allure from "allure-js-commons";

import { PageBuilderClient } from "@api/rest/clients/page-builder-client";
import { arrangePublishedPage } from "@dataset/arrange/page-builder";
import { newPage } from "@dataset/builders/page-builder";
import { expect, test } from "@fixtures";
import { ContentPage, HomePage, SignInPage } from "@pages/frontend/pages/simple-pages";

const PAGE_TEXT = "Welcome to the automated test page";

test.describe("content pages (anonymous)", () => {
  test.beforeEach(async () => {
    await allure.feature("Storefront / Content pages (E2E)");
  });

  test("a published page builder page is served on the frontend", async ({
    page,
    platformAdminHttpClient,
    cleanupStack,
    frontendContext,
  }) => {
    const published = await test.step("arrange: publish a page builder page", () =>
      arrangePublishedPage(
        new PageBuilderClient(platformAdminHttpClient),
        cleanupStack,
        newPage(frontendContext.storeId, { cultureName: frontendContext.cultureName, texts: [PAGE_TEXT] }),
      ));
    const contentPage = new ContentPage(page, published.permalink);

    const response = await test.step(`act: open ${published.permalink}`, () =>
      page.goto(contentPage.path, { waitUntil: "load" }));

    await test.step("assert: the page answers OK and renders its content", async () => {
      expect(response?.ok()).toBe(true);
      await expect(page).toHaveURL(new RegExp(`${published.permalink}$`));
      await expect(page.getByText(PAGE_TEXT)).toBeVisible();
    });
  });
});

test.describe("sign-in (anonymous)", () => {
  test.beforeEach(async () => {
    await allure.feature("Account / Sign-in (E2E)");
  });

  test("sign in with valid credentials", async ({ page, customerAccount }) => {
    const signInPage = new SignInPage(page);
    const homePage = new HomePage(page);

    await test.step("arrange: the sign-in form is complete", async () => {
      await signInPage.navigate();
      for (const control of [
        signInPage.emailInput,
        signInPage.passwordInput,
        signInPage.forgotPasswordLink,
        signInPage.signInButton,
      ]) {
        await expect(control).toBeVisible();
      }
    });

    await test.step(`act: sign in as ${customerAccount.credentials.username}`, () =>
      signInPage.signIn(customerAccount.credentials.username, customerAccount.credentials.password));

    await test.step("assert: the home page opens with the account button", async () => {
      await expect(page).toHaveURL(new RegExp(`${homePage.path}$`));
      await expect(homePage.topHeader.accountButton.root).toBeVisible();
    });
  });

  test("sign in with unknown credentials", async ({ page, env }) => {
    const signInPage = new SignInPage(page);

    await test.step("act: sign in as an unknown user", () =>
      signInPage.signIn("fake-username@test.com", env.usersPassword));

    await test.step("assert: an error alert is shown", async () => {
      await expect(signInPage.errorAlert).toBeVisible();
    });
  });
});
