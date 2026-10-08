import type { ProductsQueryVariables } from "@api/graphql/generated/graphql";
import type { GraphqlClient } from "@api/graphql/graphql-client";
import type { FrontendContext } from "../frontend-context";

import { ProductsDocument } from "@api/graphql/generated/graphql";

export const SEARCH_PAGE_SIZE = 100;

export type ProductSearch = Pick<ProductsQueryVariables, "query" | "filter" | "sort">;

export async function searchProducts(graphqlClient: GraphqlClient, context: FrontendContext, search: ProductSearch) {
  const { products } = await graphqlClient.execute(ProductsDocument, {
    storeId: context.storeId,
    userId: context.userId,
    cultureName: context.cultureName,
    currencyCode: context.currencyCode,
    first: SEARCH_PAGE_SIZE,
    ...search,
  });
  return (products?.items ?? []).flatMap((item) => (item === null ? [] : [item]));
}
