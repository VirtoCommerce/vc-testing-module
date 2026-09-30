import type { Locator, Page } from "@playwright/test";

import { CategoryViewSwitcher } from "../components/category-view-switcher";
import { PriceFilter } from "../components/price-filter";
import { ProductCard } from "../components/product-card";
import { MainLayout } from "../layouts/main-layout";

const FIRST_CARDS_TIMEOUT_MS = 30_000;
const NEXT_CARDS_TIMEOUT_MS = 3_000;

export class CategoryPage extends MainLayout {
  readonly path: string;
  readonly productsCountLabel: Locator;
  readonly viewSwitcher: CategoryViewSwitcher;
  readonly gridView: Locator;
  readonly listView: Locator;
  readonly priceFilter: PriceFilter;
  readonly productCards: Locator;

  constructor(page: Page, categoryPath: string, sort = "price-ascending") {
    super(page);
    this.path = `/${categoryPath}?sort=${sort}`;
    this.productsCountLabel = page.locator("[data-test-id='products-count-label']");
    this.viewSwitcher = new CategoryViewSwitcher(page.locator("[data-test-id='view-switcher']"));
    this.gridView = page.locator("[data-test-id='products-grid-view']");
    this.listView = page.locator("[data-test-id='products-list-view']");
    this.priceFilter = new PriceFilter(page.locator("[data-test-id='filter-price']"));
    this.productCards = page.locator("[data-product-sku]");
  }

  async scrollToProduct(sku: string): Promise<ProductCard> {
    const card = this.page.locator(`[data-product-sku='${sku}']`).first();
    await this.productCards.first().waitFor({ timeout: FIRST_CARDS_TIMEOUT_MS });
    for (;;) {
      if ((await card.count()) > 0) {
        await card.scrollIntoViewIfNeeded();
        return new ProductCard(card, sku);
      }
      const loaded = await this.productCards.count();
      await this.page.evaluate("window.scrollTo(0, document.body.scrollHeight)");
      const more = await this.productCards
        .nth(loaded)
        .waitFor({ timeout: NEXT_CARDS_TIMEOUT_MS })
        .then(() => true)
        .catch(() => false);
      if (!more) {
        throw new Error(`Product with SKU "${sku}" is not on category page ${this.path}`);
      }
    }
  }
}
