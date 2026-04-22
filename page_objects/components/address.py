from .component import Component


class Address(Component):
    @property
    def postal_code(self) -> str | None:
        return self._root.get_attribute("data-postal-code")

    @property
    def country_name(self) -> str | None:
        return self._root.get_attribute("data-country")

    @property
    def region_name(self) -> str | None:
        return self._root.get_attribute("data-region")

    @property
    def city(self) -> str | None:
        return self._root.get_attribute("data-city")

    @property
    def address_line_1(self) -> str | None:
        return self._root.get_attribute("data-address-line-1")
