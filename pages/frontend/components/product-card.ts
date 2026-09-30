import type { Locator, Page } from "@playwright/test";

import { AddToCartButton } from "./add-to-cart-button";
import { LineItem } from "./line-item";
import { QuantityStepper } from "./quantity-stepper";

export class ProductCard {
  readonly root: Locator;
  readonly sku: string;
  readonly quantityStepper: QuantityStepper;
  readonly addToCartButton: AddToCartButton;
  readonly addToListButton: Locator;
  readonly configurationsButton: Locator;
  readonly variationsButton: Locator;

  constructor(root: Locator, sku: string) {
    this.root = root;
    this.sku = sku;
    this.quantityStepper = new QuantityStepper(root.locator("[data-test-id='quantity-stepper']"));
    this.addToCartButton = new AddToCartButton(root.locator("[data-test-id='add-to-cart-button']"));
    this.addToListButton = root.locator("[data-test-id='add-to-list-button']");
    this.configurationsButton = root.locator("[data-test-id='product-card-configurations-button']");
    this.variationsButton = root.locator(`[data-test-id='variations-${sku}-button']`).first();
  }

  async openConfigurations(): Promise<Page> {
    const page = this.root.page();
    if ((await this.configurationsButton.getAttribute("target")) !== "_blank") {
      await this.configurationsButton.click();
      return page;
    }
    const [tab] = await Promise.all([page.waitForEvent("popup"), this.configurationsButton.click()]);
    return tab;
  }

  variation(sku: string): LineItem {
    return new LineItem(this.root.locator(`[data-item-sku='${sku}']`));
  }
}
