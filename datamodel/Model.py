from __future__ import annotations
from typing import TYPE_CHECKING

from datamodel.mmpd.process.Operator import Operator
from datamodel.mmpd.process.ProcessStep import ProcessStep
from datamodel.mmpd.process.ProcessStepSpecification import ProcessStepSpecification
from datamodel.mmpd.product.Batch import Batch
from datamodel.mmpd.product.PreProduct import PreProduct
from datamodel.mmpd.product.Product import Product
from datamodel.mmpd.product.ProductSpecification import ProductSpecification
from datamodel.mmpd.resource.Machine import Machine
from datamodel.mmpd.resource.ShopFloor import ShopFloor
from datamodel.soil.Component import Component
from datamodel.soil.ComponentType import ComponentType
from datamodel.soil.SensorReading import SensorReading
import json

if TYPE_CHECKING:
    from datamodel.mmpd.ProductionObject import ProductionObject
    from datamodel.soil.Component import Component
    from datamodel.soil.SensorReading import SensorReading

PARSE_CONVERSION = {
    'MMPD:OPERATOR' : lambda: Operator,
    'MMPD:PROCESSSTEP' : lambda: ProcessStep,
    'MMPD:PROCESSSTEPSPECIFICATION' : lambda:ProcessStepSpecification,
    'MMPD:BATCH' : lambda:Batch,
    'MMPD:PREPRODUCT' : lambda:PreProduct,
    'MMPD:PRODUCT' : lambda:Product,
    'MMPD:PRODUCTSPECIFICATION' : lambda:ProductSpecification,
    'MMPD:MACHINE' : lambda:Machine,
    'MMPD:SHOPFLOOR' : lambda:ShopFloor,
}

class Model:
    _objects: set[ProductionObject | Component | SensorReading]

    def __init__(self):
        self._objects = set()

    def serialize(self) -> list[dict]:
        return [obj.serialize() for obj in self._objects]

    def add(self, object: ProductionObject | Component | SensorReading) -> None:
        self._objects.add(object)

    def get_object(self, uuid: str) -> ProductionObject | Component | SensorReading | None:
        for obj in self._objects:
            if obj.uuid == uuid:
                return obj
        return None
    
    @property
    def objects(self) -> set[ProductionObject | Component | SensorReading]:
        return self._objects

    @staticmethod
    def parse(data: list[dict]) -> Model:
        datamodel = Model()

        for obj in data:
            obj_type = obj['object_type']

            if obj_type == 'SOIL:COMPONENT' :
                Component(json.dumps(obj['data']), ComponentType[obj['component_type']], datamodel)
            else:
                cls = PARSE_CONVERSION[obj_type]()
                instance: ProductionObject = cls(obj['uuid'], datamodel)
                instance.add_attr_raw(obj['attributes'])
                instance.add_ref_raw(obj['references'])

        for mea in data:
            if mea['object_type'] != 'SOIL:SENSOR_READING':
                continue
            
            sensor = datamodel.get_object(mea['sensor'])
            assert isinstance(sensor, Component)

            reading = SensorReading(json.dumps(mea['data']))
            reading.sensor = sensor
            reading.model = datamodel
            datamodel.add(reading)

        return datamodel