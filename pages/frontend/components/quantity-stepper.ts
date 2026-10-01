import type { Locator } from "@playwright/test";

export class QuantityStepper {
  readonly root: Locator;
  readonly incrementButton: Locator;
  readonly decrementButton: Locator;
  readonly quantityInput: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.incrementButton = root.locator(".vc-quantity-stepper__increment");
    this.decrementButton = root.locator(".vc-quantity-stepper__decrement");
    this.quantityInput = root.locator(".vc-input__input");
  }
}
