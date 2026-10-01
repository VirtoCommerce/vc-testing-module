import type { Locator, Page } from "@playwright/test";

import { AddressForm } from "./address-form";

export class EditAddressModal {
  readonly root: Locator;
  readonly addressForm: AddressForm;
  readonly submitButton: Locator;
  readonly cancelButton: Locator;

  constructor(page: Page) {
    this.root = page.locator("[data-test-id='edit-address-modal']");
    this.addressForm = new AddressForm(this.root.locator("[data-test-id='address-form']"));
    this.submitButton = this.root.locator("[data-test-id='submit-button']");
    this.cancelButton = this.root.locator("[data-test-id='cancel-button']");
  }
}
