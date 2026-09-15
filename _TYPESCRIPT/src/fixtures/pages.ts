import { SignInPage } from "@page-objects/frontend/pages/sign-in";
import { test as base } from "@playwright/test";

export interface Pages {
  signInPage: SignInPage;
}

export const pages = base.extend<Pages>({
  signInPage: async ({ page }, use) => {
    await use(new SignInPage(page));
  },
});
