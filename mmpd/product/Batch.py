from __future__ import annotations
from typing import TYPE_CHECKING, cast
from mmpd.ProductionObject import ProductionObject

if TYPE_CHECKING:
    from mmpd.product.Product import Product
    from Model import Model

class Batch(ProductionObject):
    _REF_PRODUCTS = 'PRODUCTS'

    _uuid_products: list[str]

    def __init__(self, uuid: str, model: Model) -> None:
        super().__init__(uuid, model)
        self._uuid_products = []

    @property
    def products(self) -> list[Product | None]:
        return [cast(Product | None, self._model.get_object(reading)) for reading in self._uuid_products]
    def add_product(self, product: Product) -> None:
        self._uuid_products.append(product.uuid)
        self._add_reference(self._REF_PRODUCTS, product)
