import type { HttpClient } from "@api/http/http-client";
import type { Logger } from "@core/logger";
import type { Dataset, DatasetItem } from "./dataset";
import type { ManifestEntry, ManifestItemName } from "./manifest";

import { ModulesClient } from "@api/rest/clients/modules-client";

import { seedRequests } from "./seed-requests";
import { resolveSeedScope } from "./seed-scope";

export interface SeedOptions {
  readonly only?: readonly ManifestItemName[] | undefined;
}

export async function seedDataset(
  httpClient: HttpClient,
  dataset: Dataset,
  logger: Logger,
  options: SeedOptions = {},
): Promise<void> {
  const installedModuleIds = await new ModulesClient(httpClient).getInstalledIds();
  const { entities, skipped } = resolveSeedScope(installedModuleIds, options.only);
  const startedAt = Date.now();
  let requestCount = 0;
  let warningCount = 0;

  for (const entity of skipped) {
    const message = `${entity.name}: module ${entity.moduleId} is not installed, skipped`;
    if (options.only === undefined) {
      logger.info(message);
    } else {
      logger.warn(message);
      warningCount++;
    }
  }
  logger.info(`seeding ${entities.length} entities: ${entities.map((entity) => entity.name).join(", ")}`);

  for (const entity of entities) {
    const items = dataset[entity.name];
    if (items.length === 0) {
      logger.warn(`${entity.name}: no items in ${entity.dir}, skipped`);
      warningCount++;
    }
    const entityStarted = Date.now();
    try {
      const { requests, failures } = await seedEntity(httpClient, entity, items);
      requestCount += requests;
      for (const failure of failures) {
        logger.warn(`${entity.name} (optional): ${firstLine(failure)}`);
      }
      warningCount += failures.length;
      logger.success(`${entity.name}: ${items.length} items, ${requests} requests in ${seconds(entityStarted)}`);
    } catch (error) {
      logger.error(`${entity.name}: ${firstLine(error)}`);
      throw error;
    }
  }

  const summary = `${entities.length} entities, ${requestCount} requests in ${seconds(startedAt)}`;
  if (warningCount > 0) {
    logger.warn(`seeded with ${warningCount} warning(s): ${summary}`);
  } else {
    logger.success(`seeded ${summary}`);
  }
}

async function seedEntity(
  httpClient: HttpClient,
  entry: ManifestEntry,
  items: readonly DatasetItem[],
): Promise<{ requests: number; failures: readonly unknown[] }> {
  const requests = seedRequests(entry, items);
  const failures: unknown[] = [];
  for (const { path, body } of requests) {
    try {
      (await httpClient.send(entry.method, path, { json: body })).expectOk();
    } catch (error) {
      if (!entry.optional) {
        throw error;
      }
      failures.push(error);
    }
  }
  return { requests: requests.length, failures };
}

function firstLine(error: unknown): string {
  const message = error instanceof Error ? error.message : String(error);
  return message.split("\n")[0] ?? message;
}

function seconds(since: number): string {
  return `${((Date.now() - since) / 1000).toFixed(1)}s`;
}
