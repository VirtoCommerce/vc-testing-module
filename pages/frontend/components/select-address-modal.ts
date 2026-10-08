import type { Locator, Page } from "@playwright/test";

import { AddressFilters } from "./address-filters";

export class SelectAddressModal {
  readonly root: Locator;
  readonly okButton: Locator;
  readonly cancelButton: Locator;
  readonly filters: AddressFilters;
  readonly addresses: Locator;

  constructor(page: Page) {
    this.root = page.locator("[data-test-id='select-address-modal']");
    this.okButton = this.root.locator("[data-test-id='confirm-button']");
    this.cancelButton = this.root.locator("[data-test-id='close-button']");
    this.filters = new AddressFilters(this.root);
    this.addresses = this.root.locator("[data-test-id^='customer-address-']");
  }

  address(text: string): Locator {
    return this.addresses.filter({ hasText: text });
  }
}
