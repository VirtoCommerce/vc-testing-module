import type { Locator } from "@playwright/test";

export class Chip {
  readonly root: Locator;
  readonly textLabel: Locator;
  readonly closeButton: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.textLabel = root.locator(".vc-chip__content");
    this.closeButton = root.locator(".vc-chip__close-button");
  }
}
