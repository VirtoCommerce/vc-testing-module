import { expect, test } from "@fixtures/base";

test.describe("Sign-in page", () => {
  const USERNAME = "acme_store_employee_1@acme.com";

  test("renders the sign-in form", async ({ page, signInPage }) => {
    await signInPage.open();

    await expect(page).toHaveURL(signInPage.path);
    await expect(signInPage.emailInput).toBeVisible();
    await expect(signInPage.passwordInput).toBeVisible();
    await expect(signInPage.signInButton).toBeVisible();
    await expect(signInPage.signInErrorAlert).toBeHidden();
  });

  test("signs in with valid credentials", async ({ env, signInPage }) => {
    await signInPage.open();
    await signInPage.signIn(USERNAME, env.usersPassword);

    await expect(signInPage.topHeader.signInLink).toBeHidden();
    await expect(signInPage.topHeader.signUpLink).toBeHidden();
  });

  test("signs in with invalid credentials", async ({ page, signInPage }) => {
    await signInPage.open();
    await signInPage.signIn(USERNAME, "SomeFakePassword!");

    await expect(signInPage.signInErrorAlert).toBeVisible();
    await expect(page).toHaveURL(signInPage.path);
  });
});
