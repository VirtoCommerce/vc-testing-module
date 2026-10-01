import type { Locator, Page } from "@playwright/test";

import { MainLayout } from "../layouts/main-layout";

export class HomePage extends MainLayout {
  readonly path = "/";
}

export class ContentPage extends MainLayout {
  readonly path: string;

  constructor(page: Page, permalink: string) {
    super(page);
    this.path = permalink;
  }
}

export class SignInPage extends MainLayout {
  readonly path = "/sign-in";
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly forgotPasswordLink: Locator;
  readonly signInButton: Locator;
  readonly errorAlert: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput = page.locator("[data-test-id='email-input']");
    this.passwordInput = page.locator("[data-test-id='password-input']");
    this.forgotPasswordLink = page.locator("[data-test-id='forgot-password-link']");
    this.signInButton = page.locator("[data-test-id='login-button']");
    this.errorAlert = page.locator("[data-test-id='sign-in-error-alert']");
  }

  async signIn(email: string, password: string): Promise<void> {
    await this.navigate();
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.signInButton.click();
  }
}

export class CheckoutCompletedPage extends MainLayout {
  readonly path = "/checkout/completed";
  readonly createdOrderNumberLabel: Locator;

  constructor(page: Page) {
    super(page);
    this.createdOrderNumberLabel = page.locator("[data-order-number]");
  }
}
