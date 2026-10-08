import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { CleanupStack } from "@core/cleanup-stack";
import type { ArrangedCart } from "@dataset/arrange/cart";
import type { FrontendContext } from "@dataset/frontend-context";

import * as allure from "allure-js-commons";

import {
  AddItemsCartDocument,
  GetCartLineValidationDocument,
  GetCartValidationAliasedDocument,
  GetCartValidationDocument,
  RemoveCartItemDocument,
  UpdateCartQuantityDocument,
} from "@api/graphql/generated/graphql";
import { arrangeCart, cartScope, lineItemFor } from "@dataset/arrange/cart";
import { expect, test } from "@fixtures";

const PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black";
const SIBLING_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-sage";
const VALID_QUANTITY = 1;
const SIBLING_QUANTITY = 2;
const OVER_STOCK_QUANTITY = 500_000;
const QUANTITY_ERROR_CODES = ["PRODUCT_QTY_CHANGED", "PRODUCT_QTY_INSUFFICIENT"];

interface ValidationError {
  readonly errorCode?: string | null;
  readonly objectType?: string | null;
  readonly objectId?: string | null;
}

test.beforeEach(async () => {
  await allure.feature("Cart / Validation");
});

test.describe("cart validation (anonymous)", () => {
  test("an over-stock line stays invalid with a line quantity error", async ({
    graphqlClient,
    cleanupStack,
    frontendContext,
  }) => {
    const cart = await test.step("arrange: cart with an over-stock line", () =>
      arrangeOverStockCart(graphqlClient, cleanupStack, frontendContext));

    const lines = await test.step("act: read line validation", () => readLines(graphqlClient, frontendContext, cart));

    await test.step("assert: the line is invalid with a quantity error on that line", async () => {
      const line = lineItemFor(lines, PRODUCT_ID);
      expect(line.isValid).toBe(false);
      expectQuantityError(line.validationErrors);
      expectScopedToLine(line.validationErrors, line.id);
    });
  });

  test("line errors persist after another cart change", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("arrange: cart with an over-stock line", () =>
      arrangeOverStockCart(graphqlClient, cleanupStack, frontendContext));

    await test.step("act: add a valid sibling line", () =>
      graphqlClient.execute(AddItemsCartDocument, {
        command: {
          ...cartScope(frontendContext),
          cartId: cart.id,
          cartItems: [{ productId: SIBLING_PRODUCT_ID, quantity: SIBLING_QUANTITY }],
        },
      }));

    await test.step("assert: the over-stock line is still invalid", async () => {
      const line = lineItemFor(await readLines(graphqlClient, frontendContext, cart), PRODUCT_ID);
      expect(line.isValid).toBe(false);
      expectQuantityError(line.validationErrors);
      expectScopedToLine(line.validationErrors, line.id);
    });
  });

  test("a valid sibling line stays valid next to an over-stock line", async ({
    graphqlClient,
    cleanupStack,
    frontendContext,
  }) => {
    const cart = await test.step("arrange: cart with two valid lines", () =>
      arrangeCart(graphqlClient, cleanupStack, frontendContext, [
        { productId: PRODUCT_ID, quantity: VALID_QUANTITY },
        { productId: SIBLING_PRODUCT_ID, quantity: SIBLING_QUANTITY },
      ]));

    await test.step("act: push one line over stock", () =>
      setQuantity(graphqlClient, frontendContext, cart, OVER_STOCK_QUANTITY));

    await test.step("assert: only the over-stock line is invalid", async () => {
      const lines = await readLines(graphqlClient, frontendContext, cart);
      const overStock = lineItemFor(lines, PRODUCT_ID);
      expect(overStock.isValid).toBe(false);
      expectQuantityError(overStock.validationErrors);
      expectScopedToLine(overStock.validationErrors, overStock.id);
      expect(lineItemFor(lines, SIBLING_PRODUCT_ID)).toMatchObject({ isValid: true, validationErrors: [] });
    });
  });

  test("cart validation errors are scoped by rule set", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("arrange: cart with an over-stock line", () =>
      arrangeOverStockCart(graphqlClient, cleanupStack, frontendContext));

    for (const ruleSet of ["*", "items"]) {
      await test.step(`assert: rule set "${ruleSet}" reports the quantity error`, async () => {
        expectQuantityError((await readCartValidation(graphqlClient, frontendContext, cart, ruleSet)).validationErrors);
      });
    }
    for (const ruleSet of ["default", "shipments", "foo"]) {
      await test.step(`assert: rule set "${ruleSet}" has no quantity error but the line stays invalid`, async () => {
        const validation = await readCartValidation(graphqlClient, frontendContext, cart, ruleSet);
        expectNoQuantityError(validation.validationErrors);
        expect(lineItemFor(validation, PRODUCT_ID).isValid).toBe(false);
      });
    }
  });

  test("rule sets stay isolated within one request", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("arrange: cart with an over-stock line", () =>
      arrangeOverStockCart(graphqlClient, cleanupStack, frontendContext));

    await test.step('assert: "*" then "shipments" in one request — only "*" has the error', async () => {
      const aliased = await readAliasedValidation(graphqlClient, frontendContext, cart, "*", "shipments");
      expectQuantityError(aliased.errorsA);
      expectNoQuantityError(aliased.errorsB);
    });
    await test.step('assert: "foo" then "*" in one request — "foo" does not affect "*"', async () => {
      const aliased = await readAliasedValidation(graphqlClient, frontendContext, cart, "foo", "*");
      expect(aliased.errorsA).toEqual([]);
      expectQuantityError(aliased.errorsB);
    });
  });

  test("rule sets stay isolated across requests", async ({ graphqlClient, cleanupStack, frontendContext }) => {
    const cart = await test.step("arrange: cart with an over-stock line", () =>
      arrangeOverStockCart(graphqlClient, cleanupStack, frontendContext));

    await test.step('assert: "*" has the error, a following "shipments" request does not', async () => {
      expectQuantityError((await readCartValidation(graphqlClient, frontendContext, cart, "*")).validationErrors);
      expectNoQuantityError(
        (await readCartValidation(graphqlClient, frontendContext, cart, "shipments")).validationErrors,
      );
    });
    await test.step('assert: "foo" has no error, a following "*" request still does', async () => {
      expectNoQuantityError((await readCartValidation(graphqlClient, frontendContext, cart, "foo")).validationErrors);
      expectQuantityError((await readCartValidation(graphqlClient, frontendContext, cart, "*")).validationErrors);
    });
  });

  test("validation errors clear after the quantity is corrected", async ({
    graphqlClient,
    cleanupStack,
    frontendContext,
  }) => {
    const cart = await test.step("arrange: cart with an over-stock line", () =>
      arrangeOverStockCart(graphqlClient, cleanupStack, frontendContext));

    await test.step(`act: correct the quantity to ${VALID_QUANTITY}`, () =>
      setQuantity(graphqlClient, frontendContext, cart, VALID_QUANTITY));

    await test.step("assert: cart and line have no errors", async () => {
      const validation = await readCartValidation(graphqlClient, frontendContext, cart, "*");
      expectNoQuantityError(validation.validationErrors);
      expect(lineItemFor(validation, PRODUCT_ID)).toMatchObject({ isValid: true, validationErrors: [] });
    });
  });

  test("validation errors clear after the over-stock line is removed", async ({
    graphqlClient,
    cleanupStack,
    frontendContext,
  }) => {
    const cart = await test.step("arrange: cart with an over-stock line", () =>
      arrangeOverStockCart(graphqlClient, cleanupStack, frontendContext));
    const line = lineItemFor(await readLines(graphqlClient, frontendContext, cart), PRODUCT_ID);

    await test.step("act: remove the over-stock line", () =>
      graphqlClient.execute(RemoveCartItemDocument, {
        command: { ...cartScope(frontendContext), cartId: cart.id, lineItemId: line.id },
      }));

    await test.step("assert: the cart has no quantity error and no such line", async () => {
      const validation = await readCartValidation(graphqlClient, frontendContext, cart, "*");
      expectNoQuantityError(validation.validationErrors);
      expect(validation.items?.map((item) => item?.productId)).not.toContain(PRODUCT_ID);
    });
  });
});

async function arrangeOverStockCart(
  graphqlClient: GraphqlClient,
  cleanupStack: CleanupStack,
  context: FrontendContext,
): Promise<ArrangedCart> {
  const cart = await arrangeCart(graphqlClient, cleanupStack, context, [
    { productId: PRODUCT_ID, quantity: VALID_QUANTITY },
  ]);
  await setQuantity(graphqlClient, context, cart, OVER_STOCK_QUANTITY);
  return cart;
}

async function setQuantity(
  graphqlClient: GraphqlClient,
  context: FrontendContext,
  cart: ArrangedCart,
  quantity: number,
): Promise<void> {
  await graphqlClient.execute(UpdateCartQuantityDocument, {
    command: { ...cartScope(context), cartId: cart.id, items: [{ productId: PRODUCT_ID, quantity }] },
  });
}

async function readLines(graphqlClient: GraphqlClient, context: FrontendContext, cart: ArrangedCart) {
  const { cart: lines } = await graphqlClient.execute(GetCartLineValidationDocument, {
    ...cartScope(context),
    cartId: cart.id,
  });
  return lines;
}

async function readCartValidation(
  graphqlClient: GraphqlClient,
  context: FrontendContext,
  cart: ArrangedCart,
  ruleSet: string,
) {
  const { cart: validation } = await graphqlClient.execute(GetCartValidationDocument, {
    ...cartScope(context),
    cartId: cart.id,
    ruleSet,
  });
  return { validationErrors: validation?.validationErrors, items: validation?.items };
}

async function readAliasedValidation(
  graphqlClient: GraphqlClient,
  context: FrontendContext,
  cart: ArrangedCart,
  ruleSetA: string,
  ruleSetB: string,
) {
  const { cart: validation } = await graphqlClient.execute(GetCartValidationAliasedDocument, {
    ...cartScope(context),
    cartId: cart.id,
    ruleSetA,
    ruleSetB,
  });
  return { errorsA: validation?.errorsA, errorsB: validation?.errorsB };
}

function quantityErrorCodes(errors: readonly (ValidationError | null)[] | null | undefined): string[] {
  return (errors ?? []).map((error) => error?.errorCode ?? "").filter((code) => QUANTITY_ERROR_CODES.includes(code));
}

function expectQuantityError(errors: readonly (ValidationError | null)[] | null | undefined): void {
  expect(quantityErrorCodes(errors), `expected one of ${QUANTITY_ERROR_CODES.join(", ")}`).not.toEqual([]);
}

function expectNoQuantityError(errors: readonly (ValidationError | null)[] | null | undefined): void {
  expect(quantityErrorCodes(errors)).toEqual([]);
}

function expectScopedToLine(errors: readonly (ValidationError | null)[] | null | undefined, lineItemId: string): void {
  const scoped = (errors ?? []).filter((error) => error?.objectType != null || error?.objectId != null);
  if (scoped.length === 0) {
    test.info().annotations.push({
      type: "not asserted",
      description: "validation errors carry no objectType/objectId, so line scoping was not checked",
    });
    return;
  }
  const linkedToLine = scoped.some(
    (error) => error?.objectId === lineItemId || /lineitem/i.test(error?.objectType ?? ""),
  );
  expect(linkedToLine, `expected an error scoped to line item ${lineItemId}`).toBe(true);
}
