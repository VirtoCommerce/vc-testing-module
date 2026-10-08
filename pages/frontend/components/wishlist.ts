import type { Locator, Page } from "@playwright/test";

export class AddToWishlistsModal {
  readonly root: Locator;
  readonly saveButton: Locator;

  constructor(page: Page) {
    this.root = page.locator("[data-test-id='add-to-wishlists-modal']");
    this.saveButton = this.root.locator("[data-test-id='wishlist-modal-save-button']");
  }

  listCheckbox(listId: string): Locator {
    return this.root.locator(`label:has([data-test-id='wishlist-modal-list-checkbox-${listId}'])`);
  }

  listWithProductCheckbox(listId: string): Locator {
    return this.root.locator(`label:has([data-test-id='wishlist-modal-list-with-product-checkbox-${listId}'])`);
  }
}

export class WishlistSettingsModal {
  readonly root: Locator;
  readonly nameInput: Locator;
  readonly descriptionInput: Locator;
  readonly sharingScopeSelect: Locator;
  readonly saveButton: Locator;

  constructor(page: Page) {
    this.root = page.locator("[data-test-id='add-or-update-wishlist-modal']");
    this.nameInput = this.root.locator("[data-test-id='wishlist-name-input']");
    this.descriptionInput = this.root.locator("[data-test-id='wishlist-description-input'] textarea");
    this.sharingScopeSelect = this.root.locator("[data-test-id='wishlist-sharing-scope-select']");
    this.saveButton = this.root.locator("[data-test-id='wishlist-settings-save-button']");
  }

  async selectScope(label: string): Promise<void> {
    await this.sharingScopeSelect.click();
    await this.root.page().getByRole("option", { name: label }).click();
  }
}

export class WishlistCard {
  readonly root: Locator;
  readonly menuButton: Locator;
  readonly editMenuItem: Locator;
  readonly removeMenuItem: Locator;

  constructor(root: Locator) {
    this.root = root;
    this.menuButton = root.locator("[data-test-id='wishlist-card-menu-button']");
    this.editMenuItem = root.page().locator("[data-test-id='wishlist-card-edit-menu-item'] button:visible");
    this.removeMenuItem = root.page().locator("[data-test-id='wishlist-card-remove-menu-item'] button:visible");
  }
}
