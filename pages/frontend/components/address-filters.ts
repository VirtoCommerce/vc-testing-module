import type { Locator } from "@playwright/test";

import { Chip } from "./chip";
import { DropdownFilter } from "./dropdown-filter";

export interface AddressFilter {
  readonly country: string;
  readonly region?: string;
  readonly city?: string;
}

export class AddressFilters {
  readonly root: Locator;
  readonly country: DropdownFilter;
  readonly region: DropdownFilter;
  readonly city: DropdownFilter;
  readonly appliedChips: Locator;
  readonly searchKeywordInput: Locator;
  readonly searchButton: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.country = new DropdownFilter(root.locator("[data-test-id='filter-country']"));
    this.region = new DropdownFilter(root.locator("[data-test-id='filter-region']"));
    this.city = new DropdownFilter(root.locator("[data-test-id='filter-city']"));
    this.appliedChips = root.locator(".vc-chip");
    this.searchKeywordInput = root.locator("[data-test-id='search-keyword-input']");
    this.searchButton = root.locator("[data-test-id='search-button']");
  }

  async apply(dropdown: DropdownFilter, name: string): Promise<void> {
    await dropdown.select(name);
    await dropdown.close();
  }

  appliedChip(name: string): Chip {
    return new Chip(this.appliedChips.filter({ hasText: name }));
  }

  async search(keyword: string): Promise<void> {
    await this.searchKeywordInput.fill(keyword);
    await this.searchButton.click();
  }
}
