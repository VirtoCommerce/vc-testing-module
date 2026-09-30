import type { Locator } from "@playwright/test";

export class PriceFilter {
  readonly root: Locator;
  readonly header: Locator;
  readonly content: Locator;
  readonly startInput: Locator;
  readonly endInput: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.header = root.locator(".vc-widget__header-container");
    this.content = root.locator(".vc-widget__slot-container");
    this.startInput = root.locator("[data-test-id='slider-input-start']");
    this.endInput = root.locator("[data-test-id='slider-input-end']");
  }

  facet(facetId: string): Locator {
    return this.root.locator(`[data-test-id='${facetId}']`);
  }
}
