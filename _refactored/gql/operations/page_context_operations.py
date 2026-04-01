from gql.types.page_context import PageContext

from .base_operations import BaseOperations, gql


class PageContextOperations(BaseOperations):
    def get_page_context(
        self,
        store_id: str | None = None,
        user_id: str | None = None,
        culture_name: str | None = None,
        permalink: str | None = None,
        organization_id: str | None = None,
    ) -> PageContext | None:
        # fmt: off
        query = gql("""
            query PageContext(
                $storeId: String,
                $userId: String,
                $cultureName: String,
                $permalink: String,
                $organizationId: String,
            ) {
              pageContext(
                storeId: $storeId,
                userId: $userId,
                cultureName: $cultureName,
                permalink: $permalink,
                organizationId: $organizationId,
              ) {
                ...PageContextFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={
                "storeId": store_id,
                "userId": user_id,
                "cultureName": culture_name,
                "permalink": permalink,
                "organizationId": organization_id,
            },
        )
        data = result["data"]["pageContext"]
        return PageContext.model_validate(data) if data else None
