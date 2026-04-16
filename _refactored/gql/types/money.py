from decimal import Decimal

from gql.types.base import GqlModel


class Money(GqlModel):
    amount: Decimal
    formatted_amount: str
