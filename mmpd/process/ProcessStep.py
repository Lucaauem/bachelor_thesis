from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.process.Operator import Operator
    from mmpd.process.ProcessFlow import ProcessFlow
    from mmpd.product.PreProduct import PreProduct
    from mmpd.product.Product import Product

class ProcessStep:
    __index: int
    __process_flow: ProcessFlow
    __operator: Operator
    __pre_product: PreProduct
    __product: Product
    __next: ProcessStep

    def __init__(self, process: ProcessFlow, index: int) -> None:
        self.__index = index
        self.__process_flow = process

    @property
    def index(self) -> int:
        return self.__index

    @property
    def operator(self) -> Operator:
        return self.__operator
    
    @property
    def pre_product(self) -> PreProduct:
        return self.__pre_product
    
    @property
    def process_flow(self) -> ProcessFlow:
        return self.__process_flow
    
    @property
    def product(self) -> Product:
        return self.__product
    
    @property
    def next(self) -> ProcessStep:
        return self.__next

    @next.setter
    def next(self, next: ProcessStep) -> None:
        self.__next = next
    
    @operator.setter
    def operator(self, operator: Operator) -> None:
        self.__operator = operator
        operator.add_to_step(self)

    @pre_product.setter
    def pre_product(self, pre_procut: PreProduct) -> None:
        self.__pre_product = pre_procut
        pre_procut.add_to_step(self)

    @product.setter
    def product(self, product: Product) -> None:
        self.__product = product
        product.process_step = self