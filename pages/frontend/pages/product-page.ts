import type { Locator, Page } from "@playwright/test";

import { ProductConfigurationArea } from "../components/product-configuration";
import { MainLayout } from "../layouts/main-layout";

export class ProductPage extends MainLayout {
  readonly path: string;
  readonly addToListButton: Locator;
  readonly configuration: ProductConfigurationArea;
  readonly totalPrice: Locator;
  readonly addToCartButton: Locator;
  readonly updateCartButton: Locator;

  constructor(page: Page, productPath: string) {
    super(page);
    this.path = `/${productPath.replace(/^\//, "")}`;
    this.addToListButton = this.root.locator("[data-test-id='add-to-list-button']");
    this.configuration = new ProductConfigurationArea(this.root.locator(".product-configuration"));
    this.totalPrice = this.root.locator(".product-price__value .price__value");
    this.addToCartButton = this.root.locator(".product-price__actions button[title='Add to cart']");
    this.updateCartButton = this.root.locator(".product-price__actions button[title='Update cart']");
  }
}
