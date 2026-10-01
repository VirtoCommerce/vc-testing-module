import type { Locator, Page } from "@playwright/test";

import { expect } from "@playwright/test";

import { exactText } from "../../text-match";

const SELECT_TRANSITION = /select-dropdown-(enter|leave)-active/;
const SELECT_OPEN_ATTEMPT_TIMEOUT_MS = 5_000;
const DATE_NAVIGATION_STEPS = 24;

export class Card {
  readonly root: Locator;
  readonly header: Locator;
  readonly title: Locator;
  readonly body: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.header = root.locator("> .vc-card__header").first();
    this.title = root.locator("> .vc-card__header .vc-card__title").first();
    this.body = root.locator("> .vc-card__body").first();
  }

  async isCollapsible(): Promise<boolean> {
    return ((await this.root.getAttribute("class")) ?? "").split(/\s+/).includes("vc-card--collapsable");
  }

  async isExpanded(): Promise<boolean> {
    return !(await this.isCollapsible()) || (await this.header.getAttribute("aria-expanded")) === "true";
  }

  async expand(): Promise<void> {
    if (!(await this.isExpanded())) {
      await this.header.click();
      await expect(this.header).toHaveAttribute("aria-expanded", "true");
    }
  }
}

export class Select {
  readonly root: Locator;
  readonly toggle: Locator;
  readonly options: Locator;
  readonly dropdown: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.toggle = root.locator("[data-test-id='dropdown-toggle']");
    this.options = root.page().locator("[data-test-id='option']");
    this.dropdown = root.page().locator("[data-test-id='dropdown']").first();
  }

  async value(): Promise<string> {
    return (await this.toggle.innerText()).trim();
  }

  async open(): Promise<void> {
    await expect(async () => {
      if (!(await this.dropdown.isVisible())) {
        await this.toggle.click();
      }
      await expect(this.dropdown).toBeVisible({ timeout: SELECT_OPEN_ATTEMPT_TIMEOUT_MS });
    }).toPass();
    await expect(this.dropdown).not.toHaveClass(SELECT_TRANSITION);
  }

  async close(): Promise<void> {
    await this.root.page().keyboard.press("Escape");
    await this.dropdown.waitFor({ state: "hidden" });
  }

  async optionTexts(): Promise<string[]> {
    await this.open();
    const texts = (await this.options.allInnerTexts()).map((text) => text.trim());
    await this.close();
    return texts;
  }

  async select(option: string): Promise<void> {
    await this.open();
    await this.options
      .filter({ hasText: exactText(option) })
      .first()
      .click();
  }
}

export class DatePicker {
  readonly root: Locator;
  readonly input: Locator;
  readonly menu: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.input = root.locator("[data-test-id='dp-input']").first();
    this.menu = root.page().locator(".dp__menu").first();
  }

  day(date: Date): Locator {
    return this.root.page().locator(`[data-test-id='dp-${isoDate(date)}']`);
  }

  async select(date: Date): Promise<void> {
    await this.input.click();
    await this.menu.waitFor({ state: "visible" });
    for (let step = 0; step < DATE_NAVIGATION_STEPS; step++) {
      const cell = this.day(date);
      if ((await cell.count()) > 0) {
        await cell.first().click();
        await this.close();
        return;
      }
      await this.menu.locator(".dp--arrow-btn-nav").last().click();
    }
    throw new Error(`Date ${isoDate(date)} is not reachable in the date picker`);
  }

  async close(): Promise<void> {
    if (await this.menu.isVisible()) {
      await this.root.page().locator(".vc-blade-header__title").last().click();
      await this.menu.waitFor({ state: "hidden" });
    }
  }
}

export class ConfirmationPopup {
  readonly root: Locator;
  readonly panel: Locator;
  readonly title: Locator;
  readonly content: Locator;
  readonly confirmButton: Locator;
  readonly cancelButton: Locator;

  constructor(page: Page) {
    this.root = page.locator(".vc-popup");
    this.panel = this.root.locator(".vc-popup__panel");
    this.title = this.root.locator(".vc-popup__title");
    this.content = this.root.locator(".vc-popup__content");
    this.confirmButton = this.root.locator(".vc-popup__footer button", { hasText: "Confirm" });
    this.cancelButton = this.root.locator(".vc-popup__footer button", { hasText: "Cancel" });
  }

  async confirm(): Promise<void> {
    await this.panel.waitFor({ state: "visible" });
    await this.confirmButton.click();
    await this.root.waitFor({ state: "detached" });
  }

  async cancel(): Promise<void> {
    await this.panel.waitFor({ state: "visible" });
    await this.cancelButton.click();
    await this.root.waitFor({ state: "detached" });
  }
}

export class Notifications {
  readonly all: Locator;
  readonly success: Locator;
  readonly error: Locator;

  constructor(page: Page) {
    this.all = page.locator(".vc-notification");
    this.success = page.locator(".vc-notification--success");
    this.error = page.locator(".vc-notification--error");
  }

  successWith(text: string): Locator {
    return this.success.filter({ hasText: text }).first();
  }
}

export class AppMenu {
  readonly items: Locator;

  constructor(page: Page) {
    this.items = page.locator(".vc-menu-item");
  }

  item(routeId: string): Locator {
    return this.items.and(this.items.page().locator(`[data-test-id='${routeId}']`));
  }

  async counter(routeId: string): Promise<number> {
    const badge = this.item(routeId).locator(".vc-badge__text");
    if ((await badge.count()) === 0) {
      return 0;
    }
    const text = (await badge.first().innerText()).trim();
    return /^\d+$/.test(text) ? Number(text) : 0;
  }
}

function isoDate(date: Date): string {
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${date.getFullYear()}-${month}-${day}`;
}
