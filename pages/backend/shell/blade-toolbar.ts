import type { Locator } from "@playwright/test";

export const DISABLED_TOOLBAR_BUTTON = /(^|\s)vc-blade-toolbar-base-button--disabled(\s|$)/;

export class BladeToolbar {
  readonly root: Locator;

  constructor(root: Locator) {
    this.root = root;
  }

  button(itemId: string): Locator {
    return this.root.locator(`[data-test-id='${itemId}']`);
  }

  async click(itemId: string): Promise<void> {
    await this.button(itemId).click();
  }

  async itemIds(): Promise<string[]> {
    const ids = await this.root
      .locator("button[data-test-id]")
      .evaluateAll((nodes) => nodes.map((node) => node.getAttribute("data-test-id")));
    return ids.filter((id): id is string => id !== null);
  }
}
