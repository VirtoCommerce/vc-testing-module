import type { Locator } from "@playwright/test";

export class ConfirmationModal {
  readonly root: Locator;
  readonly confirmButton: Locator;
  readonly cancelButton: Locator;

  constructor(root: Locator, confirmButtonId: string, cancelButtonId: string) {
    this.root = root;
    this.confirmButton = root.locator(`[data-test-id='${confirmButtonId}']`);
    this.cancelButton = root.locator(`[data-test-id='${cancelButtonId}']`);
  }
}
