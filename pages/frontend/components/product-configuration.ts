import type { Locator } from "@playwright/test";

const COLLAPSED_CLASS = "vc-widget--collapsed";

export class ProductConfigurationOption {
  readonly root: Locator;
  readonly radio: Locator;
  readonly price: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.radio = root.locator("input[type='radio']");
    this.price = root.locator(".vc-product-price__actual").first();
  }

  async select(): Promise<void> {
    await this.root.locator(".vc-radio-button__container").click();
  }
}

export class ProductConfigurationSection {
  readonly root: Locator;
  readonly header: Locator;
  readonly title: Locator;
  readonly selectedOptionLabel: Locator;
  readonly requiredMark: Locator;
  readonly options: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.header = root.locator(".vc-widget__header-container");
    this.title = root.locator("[data-test-id='section-title']");
    this.selectedOptionLabel = root.locator("[data-test-id='section-subtitle']");
    this.requiredMark = root.locator(".product-configuration__required");
    this.options = root.locator("[data-test-id='product-option']");
  }

  async isExpanded(): Promise<boolean> {
    const classes = (await this.root.getAttribute("class")) ?? "";
    return !classes.split(/\s+/).includes(COLLAPSED_CLASS);
  }

  async expand(): Promise<void> {
    if (!(await this.isExpanded())) {
      await this.header.click();
    }
  }

  option(name: string): ProductConfigurationOption {
    return new ProductConfigurationOption(
      this.options.filter({ has: this.root.page().locator("a", { hasText: name }) }).first(),
    );
  }

  async selectOption(name: string): Promise<ProductConfigurationOption> {
    await this.expand();
    const option = this.option(name);
    await option.select();
    return option;
  }
}

export class ProductConfigurationArea {
  readonly root: Locator;
  readonly sections: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.sections = root.locator("[data-test-id='section']");
  }

  section(name: string): ProductConfigurationSection {
    return new ProductConfigurationSection(
      this.sections
        .filter({ has: this.root.page().locator("[data-test-id='section-title']", { hasText: name }) })
        .first(),
    );
  }

  async selectOption(sectionName: string, optionName: string): Promise<ProductConfigurationOption> {
    return this.section(sectionName).selectOption(optionName);
  }
}
