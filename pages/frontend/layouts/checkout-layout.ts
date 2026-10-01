import type { Locator, Page } from "@playwright/test";

export abstract class CheckoutLayout {
  readonly page: Page;
  readonly shippingCostLabel: Locator;
  abstract readonly path: string;

  constructor(page: Page) {
    this.page = page;
    this.shippingCostLabel = page.locator("[data-test-id='shipping-cost-label']");
  }

  async navigate(): Promise<void> {
    await this.page.goto(this.path, { waitUntil: "load" });
  }

  async clickOutside(): Promise<void> {
    await this.page.locator("body").click({ position: { x: 1, y: 1 } });
  }
}
