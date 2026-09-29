import { Component } from "@page-objects/component";
import type { Locator } from "@playwright/test";

export class TopHeaderComponent extends Component {
  get signInLink(): Locator {
    return this.root.getByTestId("sign-in-link");
  }

  get signUpLink(): Locator {
    return this.root.getByTestId("sign-up-link");
  }
}
