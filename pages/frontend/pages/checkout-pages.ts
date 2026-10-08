import type { Locator, Page } from "@playwright/test";

import { PaymentDetailsSection } from "../components/payment-details-section";
import { ShippingDetailsSection } from "../components/shipping-details-section";
import { CheckoutLayout } from "../layouts/checkout-layout";

export class CheckoutShippingPage extends CheckoutLayout {
  readonly path = "/checkout/shipping";
  readonly shippingDetails: ShippingDetailsSection;
  readonly billingButton: Locator;

  constructor(page: Page) {
    super(page);
    this.shippingDetails = new ShippingDetailsSection(page.locator("[data-test-id='shipping-details-section']"));
    this.billingButton = page.locator("[data-test-id='billing-button']");
  }
}

export class CheckoutPaymentPage extends CheckoutLayout {
  readonly path = "/checkout/billing";
  readonly paymentDetails: PaymentDetailsSection;
  readonly reviewOrderButton: Locator;

  constructor(page: Page) {
    super(page);
    this.paymentDetails = new PaymentDetailsSection(page.locator("[data-test-id='payment-details-section']"));
    this.reviewOrderButton = page.locator("[data-test-id='review-order-button']");
  }
}

export class CheckoutReviewOrderPage extends CheckoutLayout {
  readonly path = "/checkout/review";
  readonly lineItems: Locator;
  readonly placeOrderButton: Locator;

  constructor(page: Page) {
    super(page);
    this.lineItems = page.locator("[data-product-sku]");
    this.placeOrderButton = page.locator("[data-test-id='place-order-button']");
  }
}
