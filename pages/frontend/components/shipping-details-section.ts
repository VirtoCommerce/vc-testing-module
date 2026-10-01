import type { Locator } from "@playwright/test";

export class ShippingDetailsSection {
  readonly root: Locator;
  readonly pickupSwitcher: Locator;
  readonly shippingSwitcher: Locator;
  readonly shippingAddressSection: Locator;
  readonly shippingAddressButton: Locator;
  readonly shippingAddressLabel: Locator;
  readonly pickupLocationSection: Locator;
  readonly pickupLocationButton: Locator;
  readonly shippingMethodSelector: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.pickupSwitcher = root.locator("[data-test-id='pickup-switcher']");
    this.shippingSwitcher = root.locator("[data-test-id='shipping-switcher']");
    this.shippingAddressSection = root.locator("[data-test-id='shipping-address-section']");
    this.shippingAddressButton = this.shippingAddressSection.locator("[data-test-id='select-address-button']");
    this.shippingAddressLabel = this.shippingAddressSection.locator("[data-test-id='selected-address-label']");
    this.pickupLocationSection = root.locator("[data-test-id='pickup-location-section']");
    this.pickupLocationButton = this.pickupLocationSection.locator("[data-test-id='select-address-button']");
    this.shippingMethodSelector = root.locator("[data-test-id='shipping-method-selector']");
  }

  selectedShippingMethod(code: string): Locator {
    return this.root.locator(`[data-selected-shipping-method-id='${code}']`);
  }

  async selectShippingMethod(code: string): Promise<void> {
    await this.shippingMethodSelector.click();
    await this.root.locator(`[data-shipping-method-id='${code}']`).click();
  }
}
