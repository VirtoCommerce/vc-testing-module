import type { Locator } from "@playwright/test";

export interface FormAddress {
  readonly firstName?: string | null;
  readonly lastName?: string | null;
  readonly email?: string | null;
  readonly phone?: string | null;
  readonly countryName?: string | null;
  readonly postalCode?: string | null;
  readonly regionName?: string | null;
  readonly city?: string | null;
  readonly line1?: string | null;
  readonly line2?: string | null;
}

export class AddressForm {
  readonly root: Locator;
  readonly firstNameInput: Locator;
  readonly lastNameInput: Locator;
  readonly emailInput: Locator;
  readonly phoneInput: Locator;
  readonly descriptionInput: Locator;
  readonly countrySelect: Locator;
  readonly postalCodeInput: Locator;
  readonly regionSelect: Locator;
  readonly cityInput: Locator;
  readonly line1Input: Locator;
  readonly line2Input: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.firstNameInput = root.locator("[data-test-id='first-name-input']");
    this.lastNameInput = root.locator("[data-test-id='last-name-input']");
    this.emailInput = root.locator("[data-test-id='email-input']");
    this.phoneInput = root.locator("[data-test-id='phone-input']");
    this.descriptionInput = root.locator("[data-test-id='description-input']");
    this.countrySelect = root.locator("[data-test-id='country-select']");
    this.postalCodeInput = root.locator("[data-test-id='postal-code-input']");
    this.regionSelect = root.locator("[data-test-id='region-select']");
    this.cityInput = root.locator("[data-test-id='city-input']");
    this.line1Input = root.locator("[data-test-id='line-1-input']");
    this.line2Input = root.locator("[data-test-id='line-2-input']");
  }

  async selectCountry(country: string): Promise<void> {
    await this.countrySelect.click();
    await this.countrySelect.locator("button").filter({ hasText: country }).click();
  }

  async selectRegion(region: string): Promise<void> {
    await this.regionSelect.click();
    await this.regionSelect.locator("button").filter({ hasText: region }).click();
  }

  async fill(address: FormAddress): Promise<void> {
    await fillIfGiven(this.firstNameInput, address.firstName);
    await fillIfGiven(this.lastNameInput, address.lastName);
    await fillIfGiven(this.phoneInput, address.phone);
    if (address.countryName) {
      await this.selectCountry(address.countryName);
    }
    await fillIfGiven(this.postalCodeInput, address.postalCode);
    if (address.regionName) {
      await this.selectRegion(address.regionName);
    }
    await fillIfGiven(this.cityInput, address.city);
    await fillIfGiven(this.line1Input, address.line1);
    await fillIfGiven(this.line2Input, address.line2);
    await fillIfGiven(this.emailInput, address.email);
  }
}

async function fillIfGiven(input: Locator, value: string | null | undefined): Promise<void> {
  if (value) {
    await input.fill(value);
  }
}
