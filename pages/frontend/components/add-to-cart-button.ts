import type { Locator } from "@playwright/test";

export class AddToCartButton {
  readonly root: Locator;
  readonly quantityInput: Locator;
  readonly textButton: Locator;
  readonly iconButton: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.quantityInput = root.locator(".vc-input__input");
    this.textButton = root.locator(".vc-add-to-cart__text-button");
    this.iconButton = root.locator(".vc-add-to-cart__icon-button");
  }
}
