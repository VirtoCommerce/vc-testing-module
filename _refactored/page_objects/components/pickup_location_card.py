from .component import Component

class PickupLocationCard(Component):
    @property
    def country(self) -> str:
        return self._root.get_attribute("data-country")
    
    @property
    def region(self) -> str:
        return self._root.get_attribute("data-region")

    @property
    def city(self) -> str:
        return self._root.get_attribute("data-city")

    @property
    def line_1(self) -> str:
        return self._root.get_attribute("data-line1")
    
    @property
    def name(self) -> str:
        return self._root.get_attribute("data-pickup-point-name")