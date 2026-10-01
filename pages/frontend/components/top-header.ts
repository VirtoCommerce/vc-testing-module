import type { Locator } from "@playwright/test";

import { attributeSelector } from "../../attribute-selector";

export interface ShipToAddressFilter {
  readonly postalCode?: string;
  readonly countryName?: string;
  readonly regionName?: string;
  readonly city?: string;
  readonly line1?: string;
}

export class HeaderSelector {
  readonly root: Locator;
  readonly button: Locator;
  readonly currentLabel: Locator;
  readonly #itemAttribute: string;

  constructor(root: Locator, name: "currency" | "language", itemAttribute: string) {
    this.root = root;
    this.button = root.locator(`[data-test-id='${name}-selector-button']`);
    this.currentLabel = root.locator(`[data-test-id='current-${name}-label']`);
    this.#itemAttribute = itemAttribute;
  }

  item(value: string): Locator {
    return this.root.locator(attributeSelector({ [this.#itemAttribute]: value }));
  }

  async select(value: string): Promise<void> {
    await this.button.click();
    await this.item(value).click();
  }
}

export class ShipToSelector {
  readonly root: Locator;
  readonly selectedAddressLabel: Locator;
  readonly addressesList: Locator;
  readonly addresses: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.selectedAddressLabel = root.locator("[data-test-id='selected-address-label']");
    this.addressesList = root.locator("[data-test-id='shipping-addresses-list']");
    this.addresses = this.addressesList.locator("button");
  }

  address(filter: ShipToAddressFilter): Locator {
    return this.addressesList.locator(
      `button${attributeSelector({
        "data-postal-code": filter.postalCode,
        "data-country": filter.countryName,
        "data-region": filter.regionName,
        "data-city": filter.city,
        "data-line-1": filter.line1,
      })}`,
    );
  }
}

export class AccountButton {
  readonly root: Locator;
  readonly organizationNameLabel: Locator;
  readonly customerNameLabel: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.organizationNameLabel = root.locator("[data-test-id='organization-name-label']");
    this.customerNameLabel = root.locator("[data-test-id='customer-name-label']");
  }
}

export class AccountMenu {
  readonly root: Locator;
  readonly dashboardLink: Locator;
  readonly signOutButton: Locator;
  readonly searchOrganizationsInput: Locator;
  readonly searchOrganizationsButton: Locator;
  readonly organizationsEmptyList: Locator;
  readonly organizations: Locator;
  readonly organizationOptions: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.dashboardLink = root.locator("[data-test-id='dashboard-link']");
    this.signOutButton = root.locator("[data-test-id='sign-out-button']");
    this.searchOrganizationsInput = root.locator("[data-test-id='organizations-search'] input");
    this.searchOrganizationsButton = root.locator("[data-test-id='organizations-search-button']");
    this.organizationsEmptyList = root.locator("[data-test-id='organizations-empty-list']");
    this.organizations = root.locator("[data-organization-name]");
    this.organizationOptions = root.locator("[data-vc-organization-option] [role='option']");
  }

  organization(name: string): Locator {
    return this.root.locator(attributeSelector({ "data-organization-name": name }));
  }

  organizationOption(name: string): Locator {
    return this.root.locator(`[role='option']:has(${attributeSelector({ "data-organization-name": name })})`);
  }

  async organizationNames(): Promise<string[]> {
    const names = await this.organizations.evaluateAll((nodes) =>
      nodes.map((node) => node.getAttribute("data-organization-name")),
    );
    return names.filter((name): name is string => name !== null);
  }

  async searchOrganizations(term: string): Promise<void> {
    await this.searchOrganizationsInput.fill(term);
    await this.searchOrganizationsButton.click();
  }

  async selectOrganization(name: string): Promise<void> {
    await this.organization(name).click();
  }
}

export class TopHeader {
  readonly root: Locator;
  readonly languageSelector: HeaderSelector;
  readonly currencySelector: HeaderSelector;
  readonly signInLink: Locator;
  readonly signUpLink: Locator;
  readonly accountButton: AccountButton;
  readonly accountMenu: AccountMenu;
  readonly addShippingAddressButton: Locator;
  readonly shipToSelector: ShipToSelector;

  constructor(root: Locator) {
    this.root = root;
    this.languageSelector = new HeaderSelector(
      root.locator("[data-test-id='language-selector']"),
      "language",
      "data-culture-name",
    );
    this.currencySelector = new HeaderSelector(
      root.locator("[data-test-id='currency-selector']"),
      "currency",
      "data-currency-code",
    );
    this.signInLink = root.locator("[data-test-id='sign-in-link']");
    this.signUpLink = root.locator("[data-test-id='sign-up-link']");
    this.accountButton = new AccountButton(root.locator("[data-test-id='account-button']"));
    this.accountMenu = new AccountMenu(root.locator("[data-test-id='account-menu']"));
    this.addShippingAddressButton = root.locator("[data-test-id='add-shipping-address-button']");
    this.shipToSelector = new ShipToSelector(root.locator("[data-test-id='ship-to-selector']"));
  }
}
