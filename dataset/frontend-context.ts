import type { StoreData } from "@api/rest/types/store";
import type { Dataset } from "./dataset";

import { requireFields } from "@core/required-fields";

import { getUser } from "./dataset";

const STORE_CONTEXT_FIELDS = ["id", "catalog", "defaultCurrency", "defaultLanguage"] as const;

export interface FrontendContext {
  readonly storeId: string;
  readonly catalogId: string;
  readonly currencyCode: string;
  readonly cultureName: string;
  readonly userId: string;
  readonly userName: string | undefined;
  readonly contactId: string | undefined;
  readonly organizationId: string | undefined;
}

export function getFrontendContext(
  dataset: Dataset,
  storeId: string,
  username: string | undefined,
  anonymousUserId: string,
): FrontendContext {
  const store = requireFields(
    dataset.stores.find((item) => item["id"] === storeId) as StoreData | undefined,
    STORE_CONTEXT_FIELDS,
    `Dataset store "${storeId}"`,
  );
  const storeContext = {
    storeId,
    catalogId: store.catalog,
    currencyCode: store.defaultCurrency,
    cultureName: store.defaultLanguage,
  };
  if (username === undefined) {
    return {
      ...storeContext,
      userId: anonymousUserId,
      userName: undefined,
      contactId: undefined,
      organizationId: undefined,
    };
  }
  const user = getUser(dataset, username);
  const contactId = user.memberId ?? undefined;
  const contact = dataset.contacts.find((item) => item["id"] === contactId);
  const organizationId = contact?.["defaultOrganizationId"];
  return {
    ...storeContext,
    userId: user.id,
    userName: username,
    contactId,
    organizationId: typeof organizationId === "string" ? organizationId : undefined,
  };
}
