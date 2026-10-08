import * as allure from "allure-js-commons";

import {
  AddOrUpdateCartPaymentDocument,
  AddOrUpdateCartShipmentDocument,
  CreateOrderFromCartDocument,
} from "@api/graphql/generated/graphql";
import { OrdersClient } from "@api/rest/clients/orders-client";
import { requireFields } from "@core/required-fields";
import { arrangeCart, cartScope } from "@dataset/arrange/cart";
import { comparableAddress, TEST_ADDRESS } from "@dataset/builders/address";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black";
const REGISTERED_USERNAME = "acme_store_employee_1@acme.com";
const ADMIN_USERNAME = "acme_store_administrator@acme.com";
const MANUAL_PAYMENT_METHOD = "DefaultManualPaymentMethod";
const AUTHORIZE_NET_PAYMENT_METHOD = "AuthorizeNetPaymentMethod";
const FIXED_RATE_METHOD = "FixedRate";
const SHIPMENT_COST_CASES = [
  { method: "BuyOnlinePickupInStore", option: "Pickup", price: 0 },
  { method: FIXED_RATE_METHOD, option: "Ground", price: 15 },
  { method: FIXED_RATE_METHOD, option: "Air", price: 25 },
] as const;
const CHANGED_ADDRESS = { ...TEST_ADDRESS, line1: "Change St 123" };

test.beforeEach(async () => {
  await allure.feature("Cart / Checkout");
});

test.describe("cart checkout (anonymous)", () => {
  test("add and change the payment of a cart", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("arrange: cart with a product", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: PRODUCT_ID, quantity: 3 }]));
    const command = { ...cartScope(frontendContext), cartId: cart.id };

    const { addOrUpdateCartPayment: withPayment } = await test.step(`act: add ${MANUAL_PAYMENT_METHOD} payment`, () =>
      graphqlClient.execute(AddOrUpdateCartPaymentDocument, {
        command: { ...command, payment: { paymentGatewayCode: MANUAL_PAYMENT_METHOD, billingAddress: TEST_ADDRESS } },
      }));
    const payment = requireFields(withPayment?.payments?.[0] ?? undefined, ["id"], "Cart payment");
    await test.step("assert: payment has the method and billing address", async () => {
      expect(withPayment?.payments).toHaveLength(1);
      expect(payment).toMatchObject({
        paymentGatewayCode: MANUAL_PAYMENT_METHOD,
        billingAddress: comparableAddress(TEST_ADDRESS),
      });
    });

    const { addOrUpdateCartPayment: changed } =
      await test.step(`act: change payment to ${AUTHORIZE_NET_PAYMENT_METHOD}`, () =>
        graphqlClient.execute(AddOrUpdateCartPaymentDocument, {
          command: {
            ...command,
            payment: {
              id: payment.id,
              paymentGatewayCode: AUTHORIZE_NET_PAYMENT_METHOD,
              billingAddress: CHANGED_ADDRESS,
            },
          },
        }));
    await test.step("assert: the same payment has the new method and address", async () => {
      expect(changed?.payments).toEqual([
        expect.objectContaining({
          id: payment.id,
          paymentGatewayCode: AUTHORIZE_NET_PAYMENT_METHOD,
          billingAddress: expect.objectContaining(comparableAddress(CHANGED_ADDRESS)),
        }),
      ]);
    });
  });

  test("add and change the shipment of a cart", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("arrange: cart with a product", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: PRODUCT_ID, quantity: 3 }]));
    const command = { ...cartScope(frontendContext), cartId: cart.id };

    const { addOrUpdateCartShipment: withShipment } = await test.step("act: add a Ground shipment", () =>
      graphqlClient.execute(AddOrUpdateCartShipmentDocument, {
        command: {
          ...command,
          shipment: {
            shipmentMethodCode: FIXED_RATE_METHOD,
            shipmentMethodOption: "Ground",
            price: 15,
            deliveryAddress: TEST_ADDRESS,
          },
        },
      }));
    const shipment = requireFields(withShipment?.shipments?.[0] ?? undefined, ["id"], "Cart shipment");
    await test.step("assert: shipment has the method, price and delivery address", async () => {
      expect(withShipment?.shipments).toHaveLength(1);
      expect(shipment).toMatchObject({
        shipmentMethodCode: FIXED_RATE_METHOD,
        shipmentMethodOption: "Ground",
        price: { amount: 15 },
        deliveryAddress: comparableAddress(TEST_ADDRESS),
      });
    });

    const { addOrUpdateCartShipment: changed } = await test.step("act: change the shipment to Air", () =>
      graphqlClient.execute(AddOrUpdateCartShipmentDocument, {
        command: {
          ...command,
          shipment: {
            id: shipment.id,
            shipmentMethodCode: FIXED_RATE_METHOD,
            shipmentMethodOption: "Air",
            price: 25,
            deliveryAddress: CHANGED_ADDRESS,
          },
        },
      }));
    await test.step("assert: the same shipment has the new option, price and address", async () => {
      expect(changed?.shipments).toEqual([
        expect.objectContaining({
          id: shipment.id,
          shipmentMethodOption: "Air",
          price: expect.objectContaining({ amount: 25 }),
          deliveryAddress: expect.objectContaining(comparableAddress(CHANGED_ADDRESS)),
        }),
      ]);
    });
  });

  test("create an order from a cart", async ({
    graphqlClient,
    anonymousHttpClient,
    tokenManager,
    cleanupStack,
    frontendContext,
    dataset,
    env,
  }) => {
    const cart = await test.step("arrange: cart with a product", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: PRODUCT_ID, quantity: 2 }]));
    const command = { ...cartScope(frontendContext), cartId: cart.id };
    await test.step("arrange: manual payment", () =>
      graphqlClient.execute(AddOrUpdateCartPaymentDocument, {
        command: {
          ...command,
          payment: { paymentGatewayCode: MANUAL_PAYMENT_METHOD, billingAddress: TEST_ADDRESS, price: 0 },
        },
      }));
    await test.step("arrange: Ground shipment", () =>
      graphqlClient.execute(AddOrUpdateCartShipmentDocument, {
        command: {
          ...command,
          shipment: {
            shipmentMethodCode: FIXED_RATE_METHOD,
            shipmentMethodOption: "Ground",
            price: 15,
            deliveryAddress: TEST_ADDRESS,
          },
        },
      }));
    const ordersClient = new OrdersClient(
      await tokenManager.authorize(anonymousHttpClient, getCredentials(dataset, ADMIN_USERNAME), env.storeId),
    );

    const { createOrderFromCart } = await test.step("act: create order from cart", () =>
      graphqlClient.execute(CreateOrderFromCartDocument, { command: { cartId: cart.id } }));
    const order = requireFields(createOrderFromCart ?? undefined, ["id", "number"], "Created order");
    cleanupStack.push(`delete order ${order.number}`, () => ordersClient.delete(order.id));

    await test.step("assert: order has the cart item, payment and shipment", async () => {
      expect(order.number).toEqual(expect.any(String));
      expect(order.items).toEqual([expect.objectContaining({ productId: PRODUCT_ID, quantity: 2 })]);
      expect(order.inPayments).toEqual([expect.objectContaining({ gatewayCode: MANUAL_PAYMENT_METHOD })]);
      expect(order.shipments).toEqual([
        expect.objectContaining({ shipmentMethodCode: FIXED_RATE_METHOD, shipmentMethodOption: "Ground" }),
      ]);
    });
  });
});

test.describe("cart checkout (registered user)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, REGISTERED_USERNAME)) });

  for (const { method, option, price } of SHIPMENT_COST_CASES) {
    test(`shipping total follows the ${method} ${option} price`, async ({
      graphqlClient,
      cleanupStack,
      frontendContext,
    }) => {
      const cart = await test.step("arrange: cart with a product", () =>
        arrangeCart(graphqlClient, cleanupStack, frontendContext, [{ productId: PRODUCT_ID, quantity: 1 }]));
      await test.step("assert: cart has no shipping cost yet", async () => {
        expect(cart.shippingTotal?.amount).toBe(0);
      });

      const { addOrUpdateCartShipment } = await test.step(`act: select ${method} ${option}`, () =>
        graphqlClient.execute(AddOrUpdateCartShipmentDocument, {
          command: {
            ...cartScope(frontendContext),
            cartId: cart.id,
            shipment: { shipmentMethodCode: method, shipmentMethodOption: option, price },
          },
        }));

      await test.step(`assert: shipping total is ${price}`, async () => {
        expect(addOrUpdateCartShipment?.shippingTotal?.amount).toBe(price);
      });
    });
  }
});
