import type { Locator } from "@playwright/test";

import { BladeToolbar } from "./blade-toolbar";
import { Card, DatePicker, Select } from "./controls";
import { DataGrid } from "./data-grid";

const LABEL = ".vc-label";
const FIELD = ".vc-input, .vc-select, .vc-date-picker";

export class Blade {
  readonly root: Locator;
  readonly title: Locator;
  readonly toolbar: BladeToolbar;
  readonly grid: DataGrid;

  constructor(root: Locator) {
    this.root = root;
    this.title = root.locator(".vc-blade-header__title");
    this.toolbar = new BladeToolbar(root.locator("[data-test-id='blade-toolbar']"));
    this.grid = new DataGrid(root);
  }

  card(title: string): Card {
    return new Card(this.root.locator(".vc-card__header").filter({ hasText: title }).locator("xpath=.."));
  }

  label(text: string): Locator {
    return this.root.locator(LABEL).filter({ hasText: text });
  }

  field(label: string): Locator {
    return this.root.locator(FIELD).filter({ has: this.root.page().locator(LABEL, { hasText: label }) });
  }

  textInput(label: string): Locator {
    return this.field(label).locator("input").first();
  }

  select(label: string): Select {
    return new Select(
      this.root.locator(".vc-select").filter({ has: this.root.page().locator(LABEL, { hasText: label }) }),
    );
  }

  datePicker(label: string): DatePicker {
    return new DatePicker(this.field(label));
  }
}
