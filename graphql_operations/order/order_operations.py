from gql import Client

from graphql_client.mutations.change_order_status import ChangeOrderStatusMutation
from graphql_client.queries.order import OrderQuery
from graphql_client.queries.orders import OrdersQuery
from graphql_client.types.customer_order_connection import CustomerOrderConnection
from graphql_client.types.customer_order_type import CustomerOrderType
from graphql_client.types.input_change_order_status_type import (
    InputChangeOrderStatusType,
)
from graphql_operations.order.fragments.order_fragment import ORDER_FRAGMENT


class OrderOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def get_orders(
        self,
        user_id: str,
        culture_name: str,
        filter: str = None,
        sort: str = "createdDate:desc",
        facet: str = None,
        first: int = 10,
        after: str = "0",
    ) -> CustomerOrderConnection:
        orders_query = OrdersQuery(self.graphql_client)

        variables = {
            "userId": user_id,
            "filter": filter,
            "sort": sort,
            "facet": facet,
            "first": first,
            "after": after,
            "cultureName": culture_name,
        }

        return_fields = f"""
            items {{
                {ORDER_FRAGMENT}
            }}
            totalCount
        """

        result = orders_query.execute(variables=variables, return_fields=return_fields)

        return result

    def get_organization_orders(
        self,
        culture_name: str,
        filter: str = None,
        sort: str = "createdDate:desc",
        facet: str = None,
        first: int = 10,
        after: str = "0",
        organization_id: str = None,
    ) -> CustomerOrderConnection:
        orders_query = OrdersQuery(self.graphql_client)

        variables = {
            "organizationId": organization_id,
            "filter": filter,
            "sort": sort,
            "facet": facet,
            "first": first,
            "after": after,
            "cultureName": culture_name,
        }

        return_fields = f"""
            items {{
                {ORDER_FRAGMENT}
            }}
            totalCount
        """

        result = orders_query.execute(variables=variables, return_fields=return_fields)

        return result

    def get_order(self, order_id: str) -> CustomerOrderType:
        order_query = OrderQuery(self.graphql_client)

        variables = {"id": order_id}

        result = order_query.execute(variables=variables, return_fields=ORDER_FRAGMENT)

        return result

    def change_order_status(self, payload: InputChangeOrderStatusType) -> bool:
        change_order_status_mutation = ChangeOrderStatusMutation(self.graphql_client)

        variables = {"command": payload}

        result = change_order_status_mutation.execute(variables=variables)

        return result
