from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.product.Product import Product

class Batch:
    __products: list[Product]

    def __init__(self) -> None:
        self.__products = []

    @property
    def products(self) -> list[Product]:
        return self.__products

    def add_product(self, product: Product) -> None:
        if product in self.__products:
            raise ValueError('Product already in this batch')
        
        if product.batch is not None:
            product.batch.remove_product(product)
        
        self.__products.append(product)

    def remove_product(self, product: Product) -> None:
        if product not in self.__products:
            raise ValueError('Product not in this batch')
        
        self.__products = [ item for item in self.__products if item != product ]

    def clear(self) -> None:
        self.__products = []