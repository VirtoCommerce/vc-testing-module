import type { Locator } from "@playwright/test";

import { AddToCartButton } from "./add-to-cart-button";
import { QuantityStepper } from "./quantity-stepper";

export class LineItem {
  readonly root: Locator;
  readonly quantityStepper: QuantityStepper;
  readonly addToCartButton: AddToCartButton;
  readonly removeButton: Locator;
  readonly saveForLaterButton: Locator;
  readonly componentsListToggle: Locator;
  readonly editConfigurationLink: Locator;
  readonly collapsedComponentsList: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.quantityStepper = new QuantityStepper(root.locator("[data-test-id='quantity-stepper']"));
    this.addToCartButton = new AddToCartButton(root.locator("[data-test-id='add-to-cart-button']"));
    this.removeButton = root.locator("[data-test-id='remove-item-button']");
    this.saveForLaterButton = root.locator(
      "[data-test-id='cart-item-actions-after-title'] [data-test-id='save-for-later-button']",
    );
    this.componentsListToggle = root.locator("button.configuration-items__toggle");
    this.editConfigurationLink = root.locator(".configuration-items__edit");
    this.collapsedComponentsList = root.locator(".configuration-items--collapsed");
  }

  async expandComponents(): Promise<void> {
    await this.componentsListToggle.waitFor();
    if ((await this.collapsedComponentsList.count()) > 0) {
      await this.componentsListToggle.click();
      await this.collapsedComponentsList.waitFor({ state: "detached" });
    }
  }
}
