import type { Locator } from "@playwright/test";

export class CategoryViewSwitcher {
  readonly root: Locator;
  readonly gridViewTab: Locator;
  readonly listViewTab: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.gridViewTab = root.locator("[data-test-id='grid-view-tab']");
    this.listViewTab = root.locator("[data-test-id='list-view-tab']");
  }
}
