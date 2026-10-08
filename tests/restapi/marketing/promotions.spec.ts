import * as allure from "allure-js-commons";

import { PromotionsClient } from "@api/rest/clients/promotions-client";
import { newCoupon, newPromotion } from "@dataset/builders/marketing";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";

test.beforeEach(async () => {
  await allure.feature("Marketing / Promotions");
});

test.describe("promotions (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("create a promotion", async ({ httpClient, cleanupStack }) => {
    const promotionsClient = new PromotionsClient(httpClient);
    const draft = newPromotion();

    const promotion = await test.step("act: create promotion", () => promotionsClient.create(draft));
    cleanupStack.push(`delete promotion ${promotion.id}`, () => promotionsClient.delete(promotion.id));

    await test.step("assert: promotion is inactive", async () => {
      expect(promotion).toMatchObject({ name: draft.name, isActive: false });
    });
  });

  test("get a new promotion template", async ({ httpClient }) => {
    const promotionsClient = new PromotionsClient(httpClient);

    const template = await test.step("act: get new promotion", () => promotionsClient.getNew());

    await test.step("assert: template is unsaved and has a condition and reward tree", async () => {
      expect(template.id ?? null).toBeNull();
      expect(template.dynamicExpression).toMatchObject({ id: "PromotionConditionAndRewardTree" });
    });
  });

  test("get a promotion by id", async ({ httpClient, cleanupStack }) => {
    const promotionsClient = new PromotionsClient(httpClient);
    const promotion = await test.step("arrange: promotion", () => promotionsClient.create(newPromotion()));
    cleanupStack.push(`delete promotion ${promotion.id}`, () => promotionsClient.delete(promotion.id));

    const reloaded = await test.step("act: get promotion", () => promotionsClient.get(promotion.id));

    await test.step("assert: fields match the created promotion", async () => {
      expect(reloaded).toMatchObject({ id: promotion.id, name: promotion.name });
    });
  });

  test("search promotions by keyword", async ({ httpClient, cleanupStack }) => {
    const promotionsClient = new PromotionsClient(httpClient);
    const promotion = await test.step("arrange: promotion", () => promotionsClient.create(newPromotion()));
    cleanupStack.push(`delete promotion ${promotion.id}`, () => promotionsClient.delete(promotion.id));

    const found = await test.step("act: search by promotion name", () =>
      promotionsClient.search({ keyword: promotion.name }));

    await test.step("assert: promotion is in the results", async () => {
      expect(found.map(({ id }) => id)).toContain(promotion.id);
    });
  });

  test("rename a promotion", async ({ httpClient, cleanupStack }) => {
    const promotionsClient = new PromotionsClient(httpClient);
    const promotion = await test.step("arrange: promotion", () => promotionsClient.create(newPromotion()));
    cleanupStack.push(`delete promotion ${promotion.id}`, () => promotionsClient.delete(promotion.id));
    const newName = `${promotion.name}-renamed`;

    await test.step("act: rename promotion", () => promotionsClient.update({ ...promotion, name: newName }));

    await test.step("assert: promotion has the new name", async () => {
      expect((await promotionsClient.get(promotion.id)).name).toBe(newName);
    });
  });

  test("describe a promotion", async ({ httpClient, cleanupStack }) => {
    const promotionsClient = new PromotionsClient(httpClient);
    const promotion = await test.step("arrange: promotion", () => promotionsClient.create(newPromotion()));
    cleanupStack.push(`delete promotion ${promotion.id}`, () => promotionsClient.delete(promotion.id));
    const description = `Description of ${promotion.name}`;

    await test.step("act: set promotion description", () => promotionsClient.update({ ...promotion, description }));

    await test.step("assert: promotion has the description", async () => {
      expect((await promotionsClient.get(promotion.id)).description).toBe(description);
    });
  });

  test("delete a promotion", async ({ httpClient, cleanupStack }) => {
    const promotionsClient = new PromotionsClient(httpClient);
    const promotion = await test.step("arrange: promotion", () => promotionsClient.create(newPromotion()));
    cleanupStack.push(`delete promotion ${promotion.id}`, () => promotionsClient.delete(promotion.id));

    await test.step("act: delete promotion", () => promotionsClient.delete(promotion.id));

    await test.step("assert: promotion is not found", async () => {
      expect(await promotionsClient.find(promotion.id)).toBeUndefined();
    });
  });

  test("create, update and delete a coupon", async ({ httpClient, cleanupStack }) => {
    const promotionsClient = new PromotionsClient(httpClient);
    const promotion = await test.step("arrange: promotion", () => promotionsClient.create(newPromotion()));
    cleanupStack.push(`delete promotion ${promotion.id}`, () => promotionsClient.delete(promotion.id));
    const draft = newCoupon(promotion.id, 15, 10);

    await test.step("act: create coupon", () => promotionsClient.saveCoupons([draft]));
    const coupon = await test.step("assert: coupon is found with its limits", async () => {
      const found = await promotionsClient.getCouponByCode(promotion.id, draft.code);
      expect(found).toMatchObject({ maxUsesNumber: 15, maxUsesPerUser: 10 });
      return found;
    });
    const couponId = coupon.id;
    cleanupStack.push(`delete coupon ${draft.code}`, () => promotionsClient.deleteCoupons([couponId]));
    const updatedCode = `${draft.code}-UPDATED`;

    await test.step("act: update coupon code and limits", () =>
      promotionsClient.saveCoupons([
        { id: couponId, promotionId: promotion.id, code: updatedCode, maxUsesNumber: 17, maxUsesPerUser: 12 },
      ]));
    await test.step("assert: coupon has the new code and limits", async () => {
      expect(await promotionsClient.getCoupon(couponId)).toMatchObject({
        code: updatedCode,
        maxUsesNumber: 17,
        maxUsesPerUser: 12,
      });
    });

    await test.step("act: delete coupon", () => promotionsClient.deleteCoupons([couponId]));
    await test.step("assert: coupon is not found", async () => {
      expect(await promotionsClient.findCoupon(couponId)).toBeUndefined();
      expect((await promotionsClient.searchCoupons({ promotionId: promotion.id })).map(({ id }) => id)).not.toContain(
        couponId,
      );
    });
  });

  test("search and delete a coupon", async ({ httpClient, cleanupStack }) => {
    const promotionsClient = new PromotionsClient(httpClient);
    const promotion = await test.step("arrange: promotion", () => promotionsClient.create(newPromotion()));
    cleanupStack.push(`delete promotion ${promotion.id}`, () => promotionsClient.delete(promotion.id));
    const draft = newCoupon(promotion.id, 10, 1);
    await test.step("arrange: coupon", () => promotionsClient.saveCoupons([draft]));

    const coupon = await test.step("act: find coupon by code", () =>
      promotionsClient.getCouponByCode(promotion.id, draft.code));
    cleanupStack.push(`delete coupon ${draft.code}`, () => promotionsClient.deleteCoupons([coupon.id]));

    await test.step("act: delete coupon", () => promotionsClient.deleteCoupons([coupon.id]));

    await test.step("assert: coupon is not found", async () => {
      expect(await promotionsClient.findCoupon(coupon.id)).toBeUndefined();
    });
  });

  test("add a coupon to a promotion", async ({ httpClient, cleanupStack }) => {
    const promotionsClient = new PromotionsClient(httpClient);
    const promotion = await test.step("arrange: promotion", () => promotionsClient.create(newPromotion()));
    cleanupStack.push(`delete promotion ${promotion.id}`, () => promotionsClient.delete(promotion.id));
    const draft = newCoupon(promotion.id, 5, 1);

    await test.step("act: add coupon", () => promotionsClient.saveCoupons([draft]));

    await test.step("assert: promotion has the coupon", async () => {
      const coupons = await promotionsClient.searchCoupons({ promotionId: promotion.id });
      cleanupStack.push(`delete coupons of promotion ${promotion.id}`, () =>
        promotionsClient.deleteCoupons(coupons.map(({ id }) => id)),
      );
      expect(coupons.map(({ code }) => code)).toEqual([draft.code]);
    });
  });
});
