from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.process.Operator import Operator
    from mmpd.product.PreProduct import PreProduct
    from mmpd.product.Product import Product

class ProcessStep:
    __operator: Operator
    __pre_product: PreProduct
    __product: Product

    @property
    def operator(self) -> Operator:
        return self.__operator
    
    @property
    def pre_product(self) -> PreProduct:
        return self.__pre_product
    
    @property
    def product(self) -> Product:
        return self.__product
    
    def set_operator(self, operator: Operator) -> None:
        self.__operator = operator
        operator.add_to_step(self)

    def set_pre_product(self, pre_procut: PreProduct) -> None:
        self.__pre_product = pre_procut
        pre_procut.add_to_step(self)

    def set_product(self, product: Product) -> None:
        self.__product = product
        product.add_to_step(self)