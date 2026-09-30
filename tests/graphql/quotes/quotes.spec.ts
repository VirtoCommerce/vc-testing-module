import type { QuoteFragment } from "@api/graphql/generated/graphql";
import type { HttpClient } from "@api/http/http-client";
import type { CleanupStack } from "@core/cleanup-stack";
import type { SignedInCustomerAccount } from "@fixtures";

import * as allure from "allure-js-commons";

import {
  ChangeQuoteCommentDocument,
  ChangeQuoteItemQuantityDocument,
  CreateQuoteDocument,
  CreateQuoteFromCartDocument,
  GetQuoteDocument,
  RemoveQuoteItemDocument,
  SubmitQuoteRequestDocument,
  UpdateQuoteAddressesDocument,
} from "@api/graphql/generated/graphql";
import { QuotesClient } from "@api/rest/clients/quotes-client";
import { requireFields } from "@core/required-fields";
import { arrangeCart, cartScope, lineItemFor } from "@dataset/arrange/cart";
import { expect, test } from "@fixtures";

const PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black";
const SECOND_PRODUCT_ID = "sodimm-crucial-ddr4-2400-8gb";
const SHIPPING_ADDRESS_TYPE = 1;
const BILLING_ADDRESS_TYPE = 2;
const QUOTE_ADDRESS = {
  city: "Springfield",
  countryCode: "USA",
  countryName: "United States of America",
  line1: "742 Evergreen Terrace",
  postalCode: "62704",
  regionId: "IL",
  regionName: "Illinois",
};

test.beforeEach(async () => {
  await allure.feature("Quotes");
});

test.describe("quotes (customer account)", () => {
  test("create an empty quote", async ({ customerAccount, platformAdminHttpClient, cleanupStack }) => {
    const { createQuote } = await test.step("act: create a quote", () =>
      customerAccount.graphqlClient.execute(CreateQuoteDocument, { command: cartScope(customerAccount.context) }));
    const quote = registerQuoteRemoval(platformAdminHttpClient, cleanupStack, createQuote);

    await test.step("assert: the quote is empty and belongs to the store", async () => {
      expect(quote).toMatchObject({ storeId: customerAccount.context.storeId, items: [] });
    });
  });

  test("create a quote from a cart", async ({ customerAccount, platformAdminHttpClient, cleanupStack }) => {
    const cart = await test.step("arrange: cart with a product ×2", () =>
      arrangeCart(customerAccount.graphqlClient, cleanupStack, customerAccount.context, [
        { productId: PRODUCT_ID, quantity: 2 },
      ]));

    const quote = await test.step("act: create a quote from the cart", () =>
      quoteFromCart(customerAccount, platformAdminHttpClient, cleanupStack, cart.id));

    await test.step("assert: the quote carries the cart item", async () => {
      expect(quote.storeId).toBe(customerAccount.context.storeId);
      expect(quote.items).toEqual([expect.objectContaining({ productId: PRODUCT_ID, quantity: 2 })]);
    });
  });

  test("change the quantity of a quote item", async ({ customerAccount, platformAdminHttpClient, cleanupStack }) => {
    const cart = await test.step("arrange: cart with a product", () =>
      arrangeCart(customerAccount.graphqlClient, cleanupStack, customerAccount.context, [
        { productId: PRODUCT_ID, quantity: 1 },
      ]));
    const quote = await test.step("arrange: quote from the cart", () =>
      quoteFromCart(customerAccount, platformAdminHttpClient, cleanupStack, cart.id));
    const quoteItem = lineItemFor(quote, PRODUCT_ID);

    const { changeQuoteItemQuantity } = await test.step("act: change the item quantity to 5", () =>
      customerAccount.graphqlClient.execute(ChangeQuoteItemQuantityDocument, {
        command: { quoteId: quote.id, lineItemId: quoteItem.id, quantity: 5 },
      }));

    await test.step("assert: the item has a proposal price for 5 units", async () => {
      const changedItem = lineItemFor(changeQuoteItemQuantity, PRODUCT_ID);
      expect(changedItem.proposalPrices?.map((price) => price?.quantity)).toContain(5);
    });
  });

  test("change the comment of a quote", async ({ customerAccount, platformAdminHttpClient, cleanupStack }) => {
    const cart = await test.step("arrange: cart with a product", () =>
      arrangeCart(customerAccount.graphqlClient, cleanupStack, customerAccount.context, [
        { productId: PRODUCT_ID, quantity: 1 },
      ]));
    const quote = await test.step("arrange: quote from the cart", () =>
      quoteFromCart(customerAccount, platformAdminHttpClient, cleanupStack, cart.id));

    const { changeQuoteComment } = await test.step("act: change the comment", () =>
      customerAccount.graphqlClient.execute(ChangeQuoteCommentDocument, {
        command: { quoteId: quote.id, comment: "Updated comment" },
      }));

    await test.step("assert: the quote has the new comment", async () => {
      expect(changeQuoteComment?.comment).toBe("Updated comment");
    });
  });

  test("set the shipping and billing addresses of a quote", async ({
    customerAccount,
    platformAdminHttpClient,
    cleanupStack,
  }) => {
    const cart = await test.step("arrange: cart with a product", () =>
      arrangeCart(customerAccount.graphqlClient, cleanupStack, customerAccount.context, [
        { productId: PRODUCT_ID, quantity: 1 },
      ]));
    const quote = await test.step("arrange: quote from the cart", () =>
      quoteFromCart(customerAccount, platformAdminHttpClient, cleanupStack, cart.id));
    const addresses = [SHIPPING_ADDRESS_TYPE, BILLING_ADDRESS_TYPE].map((addressType) => ({
      ...QUOTE_ADDRESS,
      addressType,
    }));

    await test.step("act: set a shipping and a billing address", () =>
      customerAccount.graphqlClient.execute(UpdateQuoteAddressesDocument, {
        command: { quoteId: quote.id, addresses },
      }));

    await test.step("assert: the stored quote has exactly those two addresses", async () => {
      const { quote: stored } = await customerAccount.graphqlClient.execute(GetQuoteDocument, {
        id: quote.id,
        storeId: customerAccount.context.storeId,
        userId: customerAccount.userId,
        cultureName: customerAccount.context.cultureName,
        currencyCode: customerAccount.context.currencyCode,
      });
      expect(stored?.addresses).toEqual(
        expect.arrayContaining(addresses.map((address) => expect.objectContaining(address))),
      );
      expect(stored?.addresses).toHaveLength(addresses.length);
    });
  });

  test("remove an item from a draft quote", async ({ customerAccount, platformAdminHttpClient, cleanupStack }) => {
    const cart = await test.step("arrange: cart with two products", () =>
      arrangeCart(customerAccount.graphqlClient, cleanupStack, customerAccount.context, [
        { productId: PRODUCT_ID, quantity: 1 },
        { productId: SECOND_PRODUCT_ID, quantity: 1 },
      ]));
    const quote = await test.step("arrange: quote from the cart", () =>
      quoteFromCart(customerAccount, platformAdminHttpClient, cleanupStack, cart.id));

    const { removeQuoteItem } = await test.step(`act: remove ${PRODUCT_ID}`, () =>
      customerAccount.graphqlClient.execute(RemoveQuoteItemDocument, {
        command: { quoteId: quote.id, lineItemId: lineItemFor(quote, PRODUCT_ID).id },
      }));

    await test.step("assert: only the other product is left in the draft", async () => {
      expect(removeQuoteItem?.status).toBe("Draft");
      expect(removeQuoteItem?.items).toEqual([expect.objectContaining({ productId: SECOND_PRODUCT_ID })]);
    });
  });

  test("submit a quote request", async ({ customerAccount, platformAdminHttpClient, cleanupStack }) => {
    const cart = await test.step("arrange: cart with a product", () =>
      arrangeCart(customerAccount.graphqlClient, cleanupStack, customerAccount.context, [
        { productId: PRODUCT_ID, quantity: 1 },
      ]));
    const quote = await test.step("arrange: quote from the cart", () =>
      quoteFromCart(customerAccount, platformAdminHttpClient, cleanupStack, cart.id));

    const { submitQuoteRequest } = await test.step("act: submit the quote", () =>
      customerAccount.graphqlClient.execute(SubmitQuoteRequestDocument, {
        command: { quoteId: quote.id, comment: "Submitted by an automated test" },
      }));

    await test.step("assert: the quote moved from draft to processing", async () => {
      expect(quote.status).toBe("Draft");
      expect(submitQuoteRequest).toMatchObject({ id: quote.id, status: "Processing" });
    });
  });
});

async function quoteFromCart(
  customerAccount: SignedInCustomerAccount,
  platformAdminHttpClient: HttpClient,
  cleanupStack: CleanupStack,
  cartId: string,
): Promise<QuoteFragment & { id: string }> {
  const { createQuoteFromCart } = await customerAccount.graphqlClient.execute(CreateQuoteFromCartDocument, {
    command: { cartId, comment: "Quote requested by an automated test" },
  });
  return registerQuoteRemoval(platformAdminHttpClient, cleanupStack, createQuoteFromCart);
}

function registerQuoteRemoval(
  platformAdminHttpClient: HttpClient,
  cleanupStack: CleanupStack,
  quote: QuoteFragment | null | undefined,
): QuoteFragment & { id: string } {
  const created = requireFields(quote ?? undefined, ["id"], "Created quote");
  cleanupStack.push(`delete quote ${created.number}`, () =>
    new QuotesClient(platformAdminHttpClient).delete([created.id]),
  );
  return created;
}
