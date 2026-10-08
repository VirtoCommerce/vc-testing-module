import type { Locator, Page } from "@playwright/test";
import type { CheckoutMode } from "@core/env";
import type { PaymentDetailsSection } from "./components/payment-details-section";
import type { ShippingDetailsSection } from "./components/shipping-details-section";

import { CartPage } from "./pages/cart-page";
import { CheckoutPaymentPage, CheckoutReviewOrderPage, CheckoutShippingPage } from "./pages/checkout-pages";
import { CheckoutCompletedPage } from "./pages/simple-pages";

export class CheckoutFlow {
  readonly mode: CheckoutMode;
  readonly cartPage: CartPage;
  readonly shippingDetails: ShippingDetailsSection;
  readonly paymentDetails: PaymentDetailsSection;
  readonly shippingCostLabel: Locator;
  readonly completedPage: CheckoutCompletedPage;
  readonly #shippingPage: CheckoutShippingPage;
  readonly #paymentPage: CheckoutPaymentPage;
  readonly #reviewPage: CheckoutReviewOrderPage;

  constructor(page: Page, mode: CheckoutMode) {
    this.mode = mode;
    this.cartPage = new CartPage(page);
    this.#shippingPage = new CheckoutShippingPage(page);
    this.#paymentPage = new CheckoutPaymentPage(page);
    this.#reviewPage = new CheckoutReviewOrderPage(page);
    this.completedPage = new CheckoutCompletedPage(page);
    const singlePage = mode === "single-page";
    this.shippingDetails = singlePage ? this.cartPage.shippingDetails : this.#shippingPage.shippingDetails;
    this.paymentDetails = singlePage ? this.cartPage.paymentDetails : this.#paymentPage.paymentDetails;
    this.shippingCostLabel = singlePage ? this.cartPage.shippingCostLabel : this.#shippingPage.shippingCostLabel;
  }

  async start(): Promise<void> {
    await this.cartPage.navigate();
    if (this.mode === "multi-step") {
      await this.cartPage.checkoutButton.click();
    }
    await this.shippingDetails.root.waitFor();
  }

  async continueToPayment(): Promise<void> {
    if (this.mode === "multi-step") {
      await this.#shippingPage.billingButton.click();
    }
    await this.paymentDetails.root.waitFor();
  }

  async placeOrder(): Promise<void> {
    if (this.mode === "multi-step") {
      await this.#paymentPage.reviewOrderButton.click();
      await this.#reviewPage.placeOrderButton.click();
      return;
    }
    await this.cartPage.placeOrderButton.click();
  }

  async clickOutside(): Promise<void> {
    await this.cartPage.clickOutside();
  }
}
