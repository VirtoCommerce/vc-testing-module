import type { Locator, Page } from "@playwright/test";

import { TopHeader } from "../components/top-header";

export abstract class MainLayout {
  readonly page: Page;
  readonly root: Locator;
  readonly topHeader: TopHeader;
  readonly cartQuantityLabel: Locator;
  abstract readonly path: string;

  constructor(page: Page) {
    this.page = page;
    this.root = page.locator(".main-layout");
    this.topHeader = new TopHeader(page.locator("[data-test-id='top-header']"));
    this.cartQuantityLabel = page.locator("[data-test-id='desktop-main-menu-cart-link'] .vc-badge__content");
  }

  async navigate(): Promise<void> {
    await this.page.goto(this.path, { waitUntil: "load" });
  }

  async clickOutside(): Promise<void> {
    await this.page.locator("body").click({ position: { x: 1, y: 1 } });
  }
}
