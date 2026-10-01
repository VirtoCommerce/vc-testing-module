import type { ShippingMethodsClient } from "@api/rest/clients/shipping-methods-client";
import type { ShippingMethodData } from "@api/rest/types/shipping";
import type { Logger } from "@core/logger";
import type { Dataset } from "./dataset";

import { array, boolean, object, string, unknown } from "zod";

const SeededShippingMethodSchema = object({
  storeId: string().min(1),
  code: string().min(1),
  isActive: boolean(),
  settings: array(object({ name: string().min(1), value: unknown() }).loose()).default([]),
}).loose();

type SeededShippingMethod = ReturnType<typeof SeededShippingMethodSchema.parse>;

const SEARCH_TAKE = 20;

export async function ensureShippingMethods(
  shippingMethodsClient: ShippingMethodsClient,
  dataset: Dataset,
  logger: Logger,
): Promise<void> {
  for (const item of dataset.shippingMethods) {
    const seeded = SeededShippingMethodSchema.parse(item);
    const label = `${seeded.storeId} / ${seeded.code}`;
    const stored = await findStored(shippingMethodsClient, seeded);
    const problems = mismatches(seeded, stored);
    if (problems.length === 0) {
      logger.info(`${label}: as seeded`);
      continue;
    }
    logger.warn(`${label}: ${problems.join("; ")}; platform holds ${summarize(stored)}; re-applying the dataset`);
    await reapply(shippingMethodsClient, seeded, stored);
    const restored = await findStored(shippingMethodsClient, seeded);
    const remaining = mismatches(seeded, restored);
    if (remaining.length > 0) {
      throw new Error(
        `${label} does not match the dataset: ${remaining.join("; ")}; platform holds ${summarize(restored)}`,
      );
    }
    logger.success(`${label}: re-applied`);
  }
}

function findStored(
  shippingMethodsClient: ShippingMethodsClient,
  seeded: SeededShippingMethod,
): Promise<ShippingMethodData[]> {
  return shippingMethodsClient.search({
    storeId: seeded.storeId,
    codes: [seeded.code],
    withoutTransient: true,
    take: SEARCH_TAKE,
  });
}

function mismatches(seeded: SeededShippingMethod, stored: readonly ShippingMethodData[]): string[] {
  const active = stored.filter((method) => method.isActive);
  if (seeded.isActive && active.length !== 1) {
    return [`${active.length} active stored methods instead of 1`];
  }
  const method = seeded.isActive ? active[0] : stored[0];
  if (method === undefined) {
    return ["not stored"];
  }
  const problems: string[] = [];
  if (method.isActive !== seeded.isActive) {
    problems.push(`isActive is ${String(method.isActive)}`);
  }
  for (const setting of seeded.settings) {
    const actual = method.settings?.find((entry) => entry.name === setting.name)?.value;
    if (!sameValue(actual, setting.value)) {
      problems.push(`${setting.name} is ${JSON.stringify(actual)} instead of ${JSON.stringify(setting.value)}`);
    }
  }
  return problems;
}

async function reapply(
  shippingMethodsClient: ShippingMethodsClient,
  seeded: SeededShippingMethod,
  stored: readonly ShippingMethodData[],
): Promise<void> {
  const active = stored.filter((method) => method.isActive);
  const kept = active[0] ?? stored[0];
  await shippingMethodsClient.update({ ...seeded, ...(kept?.id ? { id: kept.id } : {}) } as ShippingMethodData);
  for (const duplicate of active.filter((method) => method !== kept)) {
    await shippingMethodsClient.update({ ...duplicate, isActive: false });
  }
}

function sameValue(actual: unknown, expected: unknown): boolean {
  if (typeof expected === "number") {
    return Number(actual) === expected;
  }
  return JSON.stringify(actual) === JSON.stringify(expected);
}

function summarize(stored: readonly ShippingMethodData[]): string {
  return JSON.stringify(
    stored.map((method) => ({
      id: method.id,
      isActive: method.isActive,
      settings: Object.fromEntries((method.settings ?? []).map((entry) => [entry.name, entry.value])),
    })),
  );
}
