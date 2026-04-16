import pytest

from core.clients import GraphQLClient
from gql.operations import ProductOperations
from gql.types import ConfigurableProductOptionInput, ConfigurationSectionInput
from tests.context import Context

_PRODUCT_ID = "product-acme-laptop-hp-omnibook-x-flip-16"


@pytest.mark.graphql
def test_product_configurable(graphql_client: GraphQLClient, ctx: Context) -> None:
    product_ops = ProductOperations(client=graphql_client)

    product_configuration = product_ops.get_product_configuration(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        configurable_product_id=_PRODUCT_ID,
    )
    assert product_configuration is not None

    sections = product_configuration.configuration_sections
    assert len(sections) > 0

    selected_sections = []
    for section in sections:
        assert len(section.options) > 0
        option = section.options[0]
        assert option.product is not None
        selected_sections.append(
            ConfigurationSectionInput(
                section_id=section.id,
                type=section.type,
                option=ConfigurableProductOptionInput(
                    product_id=option.product.id,
                    quantity=option.quantity,
                ),
            )
        )

    line_item = product_ops.create_configured_line_item(
        configurable_product_id=_PRODUCT_ID,
        configuration_sections=selected_sections,
        store_id=ctx.store_id,
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
    )

    assert line_item is not None
    assert line_item.quantity == 1
    assert line_item.product is not None
    assert line_item.product.id == _PRODUCT_ID
