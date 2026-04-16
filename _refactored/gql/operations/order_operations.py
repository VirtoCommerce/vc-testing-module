from gql.types.order import Order

from .base_operations import BaseOperations, gql


class OrderOperations(BaseOperations):
    def get_orders(
        self,
        user_id: str | None = None,
        filter: str | None = None,
        sort: str | None = None,
        culture_name: str | None = None,
        first: int | None = None,
        after: str | None = None,
    ) -> list[Order]:
        # fmt: off
        query = gql("""
            query Orders(
                $userId: String,
                $filter: String,
                $sort: String,
                $cultureName: String,
                $first: Int,
                $after: String,
            ) {
              orders(
                userId: $userId,
                filter: $filter,
                sort: $sort,
                cultureName: $cultureName,
                first: $first,
                after: $after,
              ) {
                items {
                  ...OrderFragment
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={
                "userId": user_id,
                "filter": filter,
                "sort": sort,
                "cultureName": culture_name,
                "first": first,
                "after": after,
            },
        )
        items = result["data"]["orders"]["items"] or []
        return [Order.model_validate(item) for item in items]

    def get_order(
        self,
        number: str,
        culture_name: str | None = None,
    ) -> Order | None:
        # fmt: off
        query = gql("""
            query Order($number: String, $cultureName: String) {
              order(number: $number, cultureName: $cultureName) {
                ...OrderFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={"number": number, "cultureName": culture_name},
        )
        data = result["data"]["order"]
        return Order.model_validate(data) if data else None

    def get_organization_orders(
        self,
        organization_id: str | None = None,
        filter: str | None = None,
        sort: str | None = None,
        culture_name: str | None = None,
        first: int | None = None,
        after: str | None = None,
    ) -> list[Order]:
        # fmt: off
        query = gql("""
            query OrganizationOrders(
                $organizationId: String,
                $filter: String,
                $sort: String,
                $cultureName: String,
                $first: Int,
                $after: String,
            ) {
              organizationOrders(
                organizationId: $organizationId,
                filter: $filter,
                sort: $sort,
                cultureName: $cultureName,
                first: $first,
                after: $after,
              ) {
                items {
                  ...OrderFragment
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={
                "organizationId": organization_id,
                "filter": filter,
                "sort": sort,
                "cultureName": culture_name,
                "first": first,
                "after": after,
            },
        )
        items = result["data"]["organizationOrders"]["items"] or []
        return [Order.model_validate(item) for item in items]
