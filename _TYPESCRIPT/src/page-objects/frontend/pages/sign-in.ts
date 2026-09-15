import { DefaultLayout } from "@page-objects/frontend/layouts/default";
import type { Locator } from "@playwright/test";

export class SignInPage extends DefaultLayout {
  readonly path: string = "/sign-in";

  get emailInput(): Locator {
    return this.page.getByTestId("email-input");
  }

  get passwordInput(): Locator {
    return this.page.getByTestId("password-input");
  }

  get signInButton(): Locator {
    return this.page.getByTestId("login-button");
  }

  get signInErrorAlert(): Locator {
    return this.page.getByTestId("sign-in-error-alert");
  }

  async signIn(email: string, password: string): Promise<void> {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.signInButton.click();
  }
}
