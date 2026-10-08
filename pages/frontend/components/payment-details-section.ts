import type { Locator } from "@playwright/test";

export class PaymentDetailsSection {
  readonly root: Locator;
  readonly billingEqualsShippingCheckbox: Locator;
  readonly selectAddressButton: Locator;
  readonly selectedAddressLabel: Locator;
  readonly paymentMethodSelector: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.billingEqualsShippingCheckbox = root.locator("[data-test-id='billing-address-equals-shipping-checkbox']");
    this.selectAddressButton = root.locator("[data-test-id='select-address-button']");
    this.selectedAddressLabel = root.locator("[data-test-id='selected-address-label']");
    this.paymentMethodSelector = root.locator("[data-test-id='payment-method-selector']");
  }

  async useSeparateBillingAddress(): Promise<void> {
    await this.billingEqualsShippingCheckbox.locator("input").uncheck({ force: true });
  }

  selectedPaymentMethod(code: string): Locator {
    return this.root.locator(`[data-selected-payment-method-id='${code}']`);
  }

  async selectPaymentMethod(code: string): Promise<void> {
    await this.paymentMethodSelector.click();
    await this.root.locator(`[data-payment-method-id='${code}']`).click();
  }
}
