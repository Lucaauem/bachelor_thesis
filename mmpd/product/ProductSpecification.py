from __future__ import annotations
from typing import TYPE_CHECKING
from mmpd.ProductionObject import ProductionObject

if TYPE_CHECKING:
    from Model import Model

class ProductSpecification(ProductionObject):
    def __init__(self, uuid:str, model: Model) -> None:
        super().__init__(uuid, model)
    
    ...