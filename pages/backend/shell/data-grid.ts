import type { Locator } from "@playwright/test";

import { exactText } from "../../text-match";

const DATA_ROW = "[role='row']:has([role='cell'])";
const HEADER_ROW = "[role='row']:has([role='columnheader'])";
const PAGINATION = ".vc-data-table__pagination";
const RANGE = /(\d+)\s*\D\s*(\d+)\s+of\s+(\d+)/;
const STATUS_BADGE = ".vc-status__content";

export interface PaginationInfo {
  readonly first: number;
  readonly last: number;
  readonly total: number;
}

export class GridRow {
  readonly root: Locator;

  constructor(root: Locator) {
    this.root = root;
  }

  cell(columnId: string): Locator {
    return this.root.locator(`[data-column-id='${columnId}']`);
  }

  async value(columnId: string): Promise<string> {
    return (await this.cell(columnId).innerText()).trim();
  }

  async badges(columnId: string): Promise<string[]> {
    return (await this.cell(columnId).locator(STATUS_BADGE).allInnerTexts()).map((text) => text.trim());
  }
}

export class DataGrid {
  readonly root: Locator;
  readonly rows: Locator;
  readonly header: Locator;
  readonly pagination: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.rows = root.locator(DATA_ROW);
    this.header = root.locator(HEADER_ROW);
    this.pagination = root.locator(PAGINATION);
  }

  columnHeader(columnId: string): Locator {
    return this.header.locator(`[data-column-id='${columnId}']`);
  }

  rowsWhere(columnId: string, value: string): Locator {
    const cell = this.root.page().locator(`[data-column-id='${columnId}']`, { hasText: exactText(value) });
    return this.rows.filter({ has: cell });
  }

  rowWhere(columnId: string, value: string): GridRow {
    return new GridRow(this.rowsWhere(columnId, value));
  }

  async values(columnId: string): Promise<string[]> {
    return (await this.rows.locator(`[data-column-id='${columnId}']`).allInnerTexts()).map((text) => text.trim());
  }

  async paginationInfo(): Promise<PaginationInfo | undefined> {
    if ((await this.pagination.count()) === 0) {
      return undefined;
    }
    const match = RANGE.exec(await this.pagination.first().innerText());
    if (match === null) {
      return undefined;
    }
    const [, first, last, total] = match.map(Number);
    return first === undefined || last === undefined || total === undefined ? undefined : { first, last, total };
  }

  async totalCount(): Promise<number> {
    return (await this.paginationInfo())?.total ?? (await this.rows.count());
  }
}
