import type { Locator, Page } from "@playwright/test";

import { ConfirmationModal } from "../components/confirmation-modal";
import { LineItem } from "../components/line-item";
import { WishlistCard, WishlistSettingsModal } from "../components/wishlist";
import { MainLayout } from "../layouts/main-layout";

export class AccountListsPage extends MainLayout {
  readonly path = "/account/lists";
  readonly createListButton: Locator;
  readonly cards: Locator;
  readonly settingsModal: WishlistSettingsModal;
  readonly deleteModal: ConfirmationModal;

  constructor(page: Page) {
    super(page);
    this.createListButton = this.root.locator("[data-test-id='create-wishlist-button']");
    this.cards = page.locator("[data-test-id='wishlist-card']");
    this.settingsModal = new WishlistSettingsModal(page);
    this.deleteModal = new ConfirmationModal(
      page.locator("[data-test-id='delete-wishlist-modal']"),
      "delete-button",
      "cancel-button",
    );
  }

  card(name: string): WishlistCard {
    return new WishlistCard(this.cards.filter({ hasText: name }).first());
  }
}

export class AccountListDetailsPage extends MainLayout {
  readonly path: string;
  readonly lineItems: Locator;
  readonly addAllToCartButton: Locator;

  constructor(page: Page, listId: string) {
    super(page);
    this.path = `/account/lists/${listId}`;
    this.lineItems = page.locator("[data-product-sku]");
    this.addAllToCartButton = page.locator("[data-test-id='add-all-to-cart-button']");
  }

  lineItem(sku: string): LineItem {
    return new LineItem(this.page.locator(`[data-product-sku='${sku}']`));
  }
}

export class AccountSavedForLaterPage extends MainLayout {
  readonly path = "/account/saved-for-later";
  readonly lineItems: Locator;
  readonly removeItemModal: ConfirmationModal;

  constructor(page: Page) {
    super(page);
    this.lineItems = page.locator("[data-product-sku]");
    this.removeItemModal = new ConfirmationModal(
      page.locator("[data-test-id='delete-wishlist-product-modal']"),
      "delete-button",
      "cancel-button",
    );
  }

  lineItem(sku: string): LineItem {
    return new LineItem(this.page.locator(`[data-product-sku='${sku}']`));
  }
}

export class SharedListPage extends MainLayout {
  readonly path: string;
  readonly listTitle: Locator;
  readonly lineItems: Locator;
  readonly addToCartControls: Locator;
  readonly notFound: Locator;

  constructor(page: Page, sharingKey: string) {
    super(page);
    this.path = `/shared-list/${sharingKey}`;
    this.listTitle = page.locator(".shared-list__name");
    this.lineItems = page.locator("[data-product-sku]");
    this.addToCartControls = page.locator("[data-test-id='add-to-cart-component']");
    this.notFound = page.getByRole("heading", { name: "404" });
  }
}
