import type { Locator, Page } from "@playwright/test";
import type { PageBuilderRoute } from "./constants";

import { AppMenu, ConfirmationPopup, Notifications } from "../shell/controls";
import { MenuItem, Route } from "./constants";
import { PageDetailsBlade } from "./page-details-blade";
import { PagesListBlade } from "./pages-list-blade";

const LIST_REFRESH_ATTEMPTS = 15;
const LIST_REFRESH_INTERVAL_MS = 2_000;

export const MENU_ITEM_FOR_ROUTE: Readonly<Record<PageBuilderRoute, string>> = {
  [Route.all]: MenuItem.all,
  [Route.draft]: MenuItem.draft,
  [Route.pending]: MenuItem.pending,
  [Route.active]: MenuItem.active,
  [Route.archived]: MenuItem.archived,
};

export interface PageBuilderShellOptions {
  readonly path: string;
  readonly storeId: string;
}

export class PageBuilderShell {
  readonly page: Page;
  readonly menu: AppMenu;
  readonly blades: Locator;
  readonly popup: ConfirmationPopup;
  readonly notifications: Notifications;
  readonly listBlade: PagesListBlade;
  readonly detailsBlade: PageDetailsBlade;
  readonly logo: Locator;
  readonly userName: Locator;
  readonly userRole: Locator;
  readonly #options: PageBuilderShellOptions;

  constructor(page: Page, options: PageBuilderShellOptions) {
    this.page = page;
    this.#options = options;
    this.menu = new AppMenu(page);
    this.blades = page.locator(".vc-blade");
    this.popup = new ConfirmationPopup(page);
    this.notifications = new Notifications(page);
    this.listBlade = new PagesListBlade(this.blades.first());
    this.detailsBlade = new PageDetailsBlade(this.blades.last());
    this.logo = page.locator(".sidebar-header__logo-image");
    this.userName = page.locator(".vc-user-info__name");
    this.userRole = page.locator(".vc-user-info__role");
  }

  url(route: PageBuilderRoute = Route.all): string {
    const path = this.#options.path.endsWith("/") ? this.#options.path : `${this.#options.path}/`;
    return `${path}?storeId=${encodeURIComponent(this.#options.storeId)}#/${route}`;
  }

  async open(route: PageBuilderRoute = Route.all): Promise<void> {
    const insideShell = this.page.url().includes(this.#options.path);
    await this.page.goto(this.url(route));
    if (insideShell) {
      await this.page.reload();
    }
    await this.page.waitForLoadState("networkidle");
    await this.blades.first().waitFor({ state: "visible" });
  }

  async openPage(name: string): Promise<PageDetailsBlade> {
    await this.listBlade.openPage(name);
    await this.detailsBlade.nameInput.waitFor({ state: "visible" });
    return this.detailsBlade;
  }

  async addPage(): Promise<PageDetailsBlade> {
    await this.listBlade.add();
    await this.detailsBlade.nameInput.waitFor({ state: "visible" });
    return this.detailsBlade;
  }

  async waitUntilListed(route: PageBuilderRoute, name: string, listed = true): Promise<PagesListBlade> {
    for (let attempt = 1; ; attempt++) {
      await this.open(route);
      if ((await this.listBlade.reveal(name)) === listed || attempt === LIST_REFRESH_ATTEMPTS) {
        return this.listBlade;
      }
      await this.page.waitForTimeout(LIST_REFRESH_INTERVAL_MS);
    }
  }

  async waitUntilCounterMatchesList(route: PageBuilderRoute): Promise<{ counter: number; total: number }> {
    const menuItem = MENU_ITEM_FOR_ROUTE[route];
    for (let attempt = 1; ; attempt++) {
      await this.open(route);
      const counter = await this.menu.counter(menuItem);
      const total = await this.listBlade.grid.totalCount();
      if (counter === total || attempt === LIST_REFRESH_ATTEMPTS) {
        return { counter, total };
      }
      await this.page.waitForTimeout(LIST_REFRESH_INTERVAL_MS);
    }
  }
}
