from gql.types.quote import Quote

from .base_operations import BaseOperations, gql


class QuoteOperations(BaseOperations):
    def create_quote(
        self,
        store_id: str,
        user_id: str,
        currency_code: str,
        culture_name: str,
    ) -> Quote:
        # fmt: off
        mutation = gql("""
            mutation CreateQuote($command: CreateQuoteCommandType!) {
              createQuote(command: $command) {
                ...QuoteFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "storeId": store_id,
                    "userId": user_id,
                    "currencyCode": currency_code,
                    "cultureName": culture_name,
                }
            },
        )
        return Quote.model_validate(result["data"]["createQuote"])

    def create_quote_from_cart(self, cart_id: str, comment: str = "") -> Quote:
        # fmt: off
        mutation = gql("""
            mutation CreateQuoteFromCart($command: CreateQuoteFromCartCommandType!) {
              createQuoteFromCart(command: $command) {
                ...QuoteFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"cartId": cart_id, "comment": comment}},
        )
        return Quote.model_validate(result["data"]["createQuoteFromCart"])

    def change_quote_comment(self, quote_id: str, comment: str) -> Quote:
        # fmt: off
        mutation = gql("""
            mutation ChangeQuoteComment($command: ChangeQuoteCommentCommandType!) {
              changeQuoteComment(command: $command) {
                ...QuoteFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"quoteId": quote_id, "comment": comment}},
        )
        return Quote.model_validate(result["data"]["changeQuoteComment"])

    def change_quote_item_quantity(self, quote_id: str, line_item_id: str, quantity: int) -> Quote:
        # fmt: off
        mutation = gql("""
            mutation ChangeQuoteItemQuantity($command: ChangeQuoteItemQuantityCommandType!) {
              changeQuoteItemQuantity(command: $command) {
                ...QuoteFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "quoteId": quote_id,
                    "lineItemId": line_item_id,
                    "quantity": quantity,
                }
            },
        )
        return Quote.model_validate(result["data"]["changeQuoteItemQuantity"])

    def cancel_quote(self, quote_id: str, comment: str = "") -> Quote:
        # fmt: off
        mutation = gql("""
            mutation CancelQuoteRequest($command: CancelQuoteCommandType!) {
              cancelQuoteRequest(command: $command) {
                ...QuoteFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"quoteId": quote_id, "comment": comment}},
        )
        return Quote.model_validate(result["data"]["cancelQuoteRequest"])
