from __future__ import annotations
from typing import TYPE_CHECKING
from datamodel.mmpd.ProductionObject import ProductionObject

if TYPE_CHECKING:
    from datamodel.Model import Model
    from datamodel.mmpd.product.Product import Product
    from datamodel.mmpd.product.PreProduct import PreProduct

class ProductSpecification(ProductionObject):
    _REF_PRODUCT = 'PRODUCTS'
    _REF_PRE_PRODUCT = 'PRE_PRODUCT'

    def __init__(self, uuid:str, model: Model) -> None:
        super().__init__(uuid, model)
    
    def add_to_product(self, product: Product) -> None:
        self._add_reference(self._REF_PRODUCT, product)

    def add_to_pre_product(self, pre_product: PreProduct) -> None:
        self._add_reference(self._REF_PRE_PRODUCT, pre_product)
