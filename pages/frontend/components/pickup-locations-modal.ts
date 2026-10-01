import type { Locator, Page } from "@playwright/test";

import { attributeSelector } from "../../attribute-selector";
import { AddressFilters } from "./address-filters";

export interface PickupLocationCardFilter {
  readonly country?: string;
  readonly region?: string;
  readonly city?: string;
  readonly name?: string;
}

const CARD = ".select-address-map-list__item";

export class PickupLocationsModal {
  readonly root: Locator;
  readonly filters: AddressFilters;
  readonly cards: Locator;

  constructor(page: Page) {
    this.root = page.locator("[data-test-id='pickup-locations-modal']");
    this.filters = new AddressFilters(this.root);
    this.cards = this.root.locator(CARD);
  }

  cardsWhere(filter: PickupLocationCardFilter): Locator {
    const attributes = attributeSelector({
      "data-country": filter.country,
      "data-region": filter.region,
      "data-city": filter.city,
      "data-pickup-point-name": filter.name,
    });
    return this.root.locator(`${CARD}${attributes}`);
  }
}
