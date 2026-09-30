import type { HttpClient } from "../../http/http-client";
import type {
  Coupon,
  CouponData,
  CouponSearchCriteria,
  CouponSearchResult,
  Promotion,
  PromotionData,
  PromotionSearchCriteria,
  PromotionSearchResult,
} from "../types/marketing";

import { requireFields } from "@core/required-fields";

import { COUPON_FIELDS, PROMOTION_FIELDS } from "../types/marketing";

const PROMOTIONS_PATH = "/api/marketing/promotions";
const COUPONS_PATH = `${PROMOTIONS_PATH}/coupons`;

export class PromotionsClient {
  readonly #httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.#httpClient = httpClient;
  }

  async get(id: string): Promise<Promotion> {
    return requireFields(await this.find(id), PROMOTION_FIELDS, `Promotion "${id}"`);
  }

  async find(id: string): Promise<Promotion | undefined> {
    const response = await this.#httpClient.get(`${PROMOTIONS_PATH}/${encodeURIComponent(id)}`);
    if (response.status === 404) {
      return undefined;
    }
    return requireFields(response.expectOk().json<PromotionData>(), PROMOTION_FIELDS, `Promotion "${id}"`);
  }

  async getNew(): Promise<PromotionData> {
    return (await this.#httpClient.get(`${PROMOTIONS_PATH}/new`)).expectOk().json<PromotionData>();
  }

  async create(promotion: PromotionData): Promise<Promotion> {
    const response = await this.#httpClient.post(PROMOTIONS_PATH, { json: promotion });
    return requireFields(response.expectOk().json<PromotionData>(), PROMOTION_FIELDS, "Created promotion");
  }

  async update(promotion: PromotionData): Promise<void> {
    (await this.#httpClient.put(PROMOTIONS_PATH, { json: promotion })).expectOk();
  }

  async search(criteria: PromotionSearchCriteria): Promise<Promotion[]> {
    const response = await this.#httpClient.post(`${PROMOTIONS_PATH}/search`, { json: criteria });
    const { results } = response.expectOk().json<PromotionSearchResult>();
    return (results ?? []).map((promotion) => requireFields(promotion, PROMOTION_FIELDS, "Found promotion"));
  }

  async delete(id: string): Promise<void> {
    (await this.#httpClient.delete(PROMOTIONS_PATH, { query: { ids: id } })).expectOk();
  }

  async saveCoupons(coupons: CouponData[]): Promise<void> {
    (await this.#httpClient.post(`${COUPONS_PATH}/add`, { json: coupons })).expectOk();
  }

  async getCoupon(id: string): Promise<Coupon> {
    return requireFields(await this.findCoupon(id), COUPON_FIELDS, `Coupon "${id}"`);
  }

  async findCoupon(id: string): Promise<Coupon | undefined> {
    const response = (await this.#httpClient.get(`${COUPONS_PATH}/${encodeURIComponent(id)}`)).expectOk();
    const coupon = response.json<CouponData | null>();
    return coupon === null ? undefined : requireFields(coupon, COUPON_FIELDS, `Coupon "${id}"`);
  }

  async getCouponByCode(promotionId: string, code: string): Promise<Coupon> {
    const found = (await this.searchCoupons({ promotionId, code })).find((coupon) => coupon.code === code);
    return requireFields(found, COUPON_FIELDS, `Coupon ${code} of promotion "${promotionId}"`);
  }

  async searchCoupons(criteria: CouponSearchCriteria): Promise<Coupon[]> {
    const response = await this.#httpClient.post(`${COUPONS_PATH}/search`, { json: criteria });
    const { results } = response.expectOk().json<CouponSearchResult>();
    return (results ?? []).map((coupon) => requireFields(coupon, COUPON_FIELDS, "Found coupon"));
  }

  async deleteCoupons(ids: readonly string[]): Promise<void> {
    (await this.#httpClient.delete(`${COUPONS_PATH}/delete`, { query: { ids } })).expectOk();
  }
}
