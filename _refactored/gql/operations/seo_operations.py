from gql.types.slug_info import SlugInfo

from .base_operations import BaseOperations, gql


class SeoOperations(BaseOperations):
    def get_slug_info(
        self,
        store_id: str | None = None,
        slug: str | None = None,
        permalink: str | None = None,
        user_id: str | None = None,
        culture_name: str | None = None,
    ) -> SlugInfo | None:
        # fmt: off
        query = gql("""
            query SlugInfo(
                $storeId: String,
                $slug: String,
                $permalink: String,
                $userId: String,
                $cultureName: String,
            ) {
              slugInfo(
                storeId: $storeId,
                slug: $slug,
                permalink: $permalink,
                userId: $userId,
                cultureName: $cultureName,
              ) {
                ...SlugInfoFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={
                "storeId": store_id,
                "slug": slug,
                "permalink": permalink,
                "userId": user_id,
                "cultureName": culture_name,
            },
        )
        data = result["data"]["slugInfo"]
        return SlugInfo.model_validate(data) if data else None
