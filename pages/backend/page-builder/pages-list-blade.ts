import type { Locator } from "@playwright/test";
import type { GridRow } from "../shell/data-grid";

import { Blade } from "../shell/blade";
import { Column, ListToolbar } from "./constants";

const SEARCH_ENDPOINT = "page-builder-pages/search";

export class PagesListBlade extends Blade {
  readonly searchInput: Locator;

  constructor(root: Locator) {
    super(root);
    this.searchInput = root.locator(".vc-input input[placeholder='Search...']");
  }

  pageRows(name: string): Locator {
    return this.grid.rowsWhere(Column.name, name);
  }

  pageRow(name: string): GridRow {
    return this.grid.rowWhere(Column.name, name);
  }

  async names(): Promise<string[]> {
    return this.grid.values(Column.name);
  }

  async statuses(): Promise<string[]> {
    return this.grid.values(Column.status);
  }

  async search(term: string): Promise<void> {
    if ((await this.searchInput.inputValue()) === term) {
      return;
    }
    const page = this.root.page();
    const [response] = await Promise.all([
      page.waitForResponse((candidate) => candidate.url().includes(SEARCH_ENDPOINT)),
      this.searchInput.fill(term),
    ]);
    const { totalCount } = (await response.json()) as { readonly totalCount?: number };
    await this.waitForRows(totalCount ?? 0);
  }

  async clearSearch(): Promise<void> {
    await this.search("");
  }

  async hasPage(name: string): Promise<boolean> {
    return (await this.pageRows(name).count()) > 0;
  }

  async reveal(name: string): Promise<boolean> {
    if (await this.hasPage(name)) {
      return true;
    }
    await this.search(name);
    return this.hasPage(name);
  }

  async add(): Promise<void> {
    await this.toolbar.click(ListToolbar.add);
  }

  async openPage(name: string): Promise<void> {
    await this.reveal(name);
    await this.pageRows(name).click();
  }

  async #matchesTotal(expected: number): Promise<boolean> {
    const count = await this.grid.rows.count();
    if (expected === 0) {
      return count === 0;
    }
    const pagination = await this.grid.paginationInfo();
    return pagination === undefined
      ? count === expected
      : pagination.total === expected && count === pagination.last - pagination.first + 1;
  }

  async waitForRows(expected: number): Promise<void> {
    const page = this.root.page();
    for (let attempt = 0; attempt < 40 && !(await this.#matchesTotal(expected)); attempt++) {
      await page.waitForTimeout(200);
    }
  }
}
