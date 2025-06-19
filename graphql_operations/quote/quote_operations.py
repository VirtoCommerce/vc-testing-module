from gql import Client
from graphql_client.mutations.change_quote_comment import ChangeQuoteCommentMutation
from graphql_client.mutations.change_quote_item_quantity import ChangeQuoteItemQuantityMutation
from graphql_client.mutations.create_quote_from_cart import CreateQuoteFromCartMutation
from graphql_client.mutations.remove_quote_item import RemoveQuoteItemMutation
from graphql_client.mutations.submit_quote_request import SubmitQuoteRequestMutation
from graphql_client.mutations.update_quote_addresses import UpdateQuoteAddressesMutation
from graphql_client.types.change_quote_comment_command_type import ChangeQuoteCommentCommandType
from graphql_client.types.change_quote_item_quantity_command_type import ChangeQuoteItemQuantityCommandType
from graphql_client.types.create_quote_from_cart_command_type import CreateQuoteFromCartCommandType
from graphql_client.types.quote_type import QuoteType
from graphql_client.types.remove_quote_item_command_type import RemoveQuoteItemCommandType
from graphql_client.types.submit_quote_command_type import SubmitQuoteCommandType
from graphql_client.types.update_quote_addresses_command_type import UpdateQuoteAddressesCommandType
from graphql_client.queries.quote import QuoteQuery
from graphql_operations.quote.fragments.quote_fragment import QUOTE_FRAGMENT


class QuoteOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def create_quote_from_cart(self, payload: CreateQuoteFromCartCommandType) -> QuoteType:
        create_quote_mutation = CreateQuoteFromCartMutation(self.graphql_client)

        variables = {"command": payload}

        result = create_quote_mutation.execute(variables=variables, return_fields=f"{QUOTE_FRAGMENT}")

        return result

    def get_quote(self, store_id: str, user_id: str, id: str, currency_code: str, culture_name: str) -> QuoteType:
        quote_query = QuoteQuery(self.graphql_client)

        variables = {
            "storeId": store_id,
            "userId": user_id,
            "id": id,
            "currencyCode": currency_code,
            "cultureName": culture_name,
        }

        result = quote_query.execute(variables=variables, return_fields=f"{QUOTE_FRAGMENT}")

        return result

    def change_quote_item_quantity(self, payload: ChangeQuoteItemQuantityCommandType) -> QuoteType:
        change_quote_item_quantity_mutation = ChangeQuoteItemQuantityMutation(self.graphql_client)

        variables = {"command": payload}

        result = change_quote_item_quantity_mutation.execute(variables=variables, return_fields=f"{QUOTE_FRAGMENT}")

        return result

    def change_quote_comment(self, payload: ChangeQuoteCommentCommandType) -> QuoteType:
        change_quote_comment_mutation = ChangeQuoteCommentMutation(self.graphql_client)

        variables = {"command": payload}

        result = change_quote_comment_mutation.execute(variables=variables, return_fields=f"{QUOTE_FRAGMENT}")

        return result

    def change_quote_addresses(self, payload: UpdateQuoteAddressesCommandType) -> QuoteType:
        change_quote_addresses_mutation = UpdateQuoteAddressesMutation(self.graphql_client)

        variables = {"command": payload}

        result = change_quote_addresses_mutation.execute(variables=variables, return_fields=f"{QUOTE_FRAGMENT}")

        return result

    def remove_quote_item(self, payload: RemoveQuoteItemCommandType) -> QuoteType:
        remove_quote_item_mutation = RemoveQuoteItemMutation(self.graphql_client)

        variables = {"command": payload}

        result = remove_quote_item_mutation.execute(variables=variables, return_fields=f"{QUOTE_FRAGMENT}")

        return result

    def submit_quote(self, payload: SubmitQuoteCommandType) -> QuoteType:
        submit_quote_mutation = SubmitQuoteRequestMutation(self.graphql_client)

        variables = {"command": payload}

        result = submit_quote_mutation.execute(variables=variables, return_fields=f"{QUOTE_FRAGMENT}")

        return result
