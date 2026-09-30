import type { Locator } from "@playwright/test";

export class DropdownFilter {
  readonly root: Locator;
  readonly dropdownButton: Locator;
  readonly dropdownList: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.dropdownButton = root.locator(".vc-popover__trigger");
    this.dropdownList = root.locator(".vc-popover__content");
  }

  async close(): Promise<void> {
    if (await this.dropdownList.isVisible()) {
      await this.dropdownButton.click();
    }
    await this.dropdownList.waitFor({ state: "hidden" });
  }

  async select(name: string): Promise<void> {
    await this.dropdownButton.click();
    await this.dropdownList.locator(`[title=${JSON.stringify(name)}]`).click();
  }
}
