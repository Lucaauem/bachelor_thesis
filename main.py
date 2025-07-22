from datamodel.mmpd.process.ProcessStepSpecification import ProcessStepSpecification
from datamodel.mmpd.product.ProductSpecification import ProductSpecification
from datamodel.mmpd.process.Operator import Operator
from datamodel.mmpd.product.Product import Product
from datamodel.mmpd.product.PreProduct import PreProduct
from datamodel.mmpd.product.Batch import Batch
from datamodel.soil.SensorReading import SensorReading
from datamodel.soil.Component import Component
from datamodel.soil.ComponentType import ComponentType
from datamodel.mmpd.process.ProcessStep import ProcessStep
from datamodel.mmpd.resource.Machine import Machine
from datamodel.mmpd.resource.ShopFloor import ShopFloor
from datamodel.Model import Model
from database.DBFramework import DBFramework
import os
import json

DUMMIES_DIR = './dummies'
OUTPUT_DIR = './output'

def main():
    model = create_dummy_model()

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(f'{OUTPUT_DIR}/output.json', 'a') as f:
        json.dump(model.serialize(), f)

def create_dummy_model() -> Model:
    with open(f'{DUMMIES_DIR}/soil_dummy_mea.json') as f:
        dummy_sr = f.read()
    with open(f'{DUMMIES_DIR}/soil_dummy_sensor.json') as f:
        dummy_sensor = f.read()
    with open(f'{DUMMIES_DIR}/soil_dummy_sensor_2.json') as f:
        dummy_sensor_2 = f.read()
    with open(f'{DUMMIES_DIR}/soil_dummy_tool.json') as f:
        dummy_tool = f.read()
    with open(f'{DUMMIES_DIR}/soil_dummy_tool_2.json') as f:
        dummy_tool_2 = f.read()

    model = Model()

    p_1 = Product('P_1', model)
    p_2 = Product('P_2', model)

    batch = Batch('BATCH', model)
    batch.add_product(p_1)
    batch.add_product(p_2)

    psp = ProductSpecification('PSP', model)
    p_1.specification = psp
    p_2.specification = psp

    pp_1 = PreProduct('PP_1', model)
    pss_1 = ProcessStepSpecification('PSS_1', model)
    ps_1 = ProcessStep('PS_1', model)
    ps_1.specification = pss_1
    ps_1.pre_product = pp_1
    ps_1.product = p_1

    pp_2 = PreProduct('PP_2', model)
    pss_2 = ProcessStepSpecification('PSS_2', model)
    ps_2 = ProcessStep('PS_2', model)
    ps_2.specification = pss_2
    ps_2.pre_product = pp_2
    ps_2.product = p_2

    ps_1.next_step = ps_2

    operator = Operator('OPERATOR', model)
    ps_1.operator = operator
    ps_2.operator = operator

    tool_1 = Component(dummy_tool, ComponentType.TOOL, model)
    tool_2 = Component(dummy_tool_2, ComponentType.TOOL, model)
    ps_1.tool = tool_2
    ps_2.tool = tool_1

    s_acc_nozzle = Component(dummy_sensor, ComponentType.REAL, model)
    s_acc_bed = Component(dummy_sensor, ComponentType.REAL, model)
    s_diameter = Component(dummy_sensor_2, ComponentType.REAL, model)

    sr_acc_nozzle = SensorReading(dummy_sr)
    sr_acc_bed = SensorReading(dummy_sr)
    sr_diameter = SensorReading(dummy_sr)

    """
    s_acc_nozzle.add_reading(sr_acc_nozzle)
    s_acc_bed.add_reading(sr_acc_bed)
    s_diameter.add_reading(sr_diameter)

    ps_1.add_sensor_reading(sr_acc_nozzle)
    ps_1.add_sensor_reading(sr_acc_bed)
    ps_1.add_sensor_reading(sr_diameter)
    ps_2.add_sensor_reading(sr_acc_nozzle)
    ps_2.add_sensor_reading(sr_acc_bed)
    ps_2.add_sensor_reading(sr_diameter)
    """

    printer_1 = Machine('PRINTER_1', model)
    printer_1.add_tool(tool_1)
    printer_1.add_tool(tool_2)
    printer_1.add_sensor(s_acc_nozzle)
    printer_1.add_sensor(s_diameter)
    ps_1.machine = printer_1
    ps_2.machine = printer_1

    shop_floor = ShopFloor('SHOP_FLOOR', model)
    shop_floor.add_machine(printer_1)

    p_1.set_attributes(name='Lamp', costs=100, quality=0.73)

    return model

if __name__ == '__main__':
    main()