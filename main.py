from mmpd.process.ProcessStepSpecification import ProcessStepSpecification
from mmpd.product.ProductSpecification import ProductSpecification
from mmpd.process.Operator import Operator
from mmpd.product.Product import Product
from mmpd.product.PreProduct import PreProduct
from mmpd.product.Batch import Batch
from soil.SensorReading import SensorReading
from soil.Sensor import Sensor
from soil.SensorType import SensorType
from mmpd.process.ProcessStep import ProcessStep
from mmpd.resource.Machine import Machine
from mmpd.resource.ShopFloor import ShopFloor
from Model import Model
import json

def main():
    with open('./soil_dummy.json') as f:
        dummy_sr = f.read()

    with open('./soil_dummy_sensor.json') as f:
        dummy_sensor = f.read()

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

    pp_2 = PreProduct('PP_2', model)
    pss_2 = ProcessStepSpecification('PSS_2', model)
    ps_2 = ProcessStep('PS_2', model)
    ps_2.specification = pss_2
    ps_2.pre_product = pp_2

    ps_1.next_step = ps_2

    operator = Operator('OPERATOR', model)
    ps_1.operator = operator
    ps_2.operator = operator

    tool_1 = Sensor(dummy_sensor, SensorType.TOOL, model)
    tool_2 = Sensor(dummy_sensor, SensorType.TOOL, model)
    ps_1.tool = tool_2
    ps_2.tool = tool_1

    s_acc_nozzle = Sensor(dummy_sensor, SensorType.REAL, model)
    s_acc_bed = Sensor(dummy_sensor, SensorType.REAL, model)
    s_diameter = Sensor(dummy_sensor, SensorType.REAL, model)

    sr_acc_nozzle = SensorReading(dummy_sr)
    sr_acc_bed = SensorReading(dummy_sr)
    sr_diameter = SensorReading(dummy_sr)

    s_acc_nozzle.add_reading(sr_acc_nozzle)
    s_acc_bed.add_reading(sr_acc_bed)
    s_diameter.add_reading(sr_diameter)

    ps_1.add_sensor_reading(sr_acc_nozzle)
    ps_1.add_sensor_reading(sr_acc_bed)
    ps_1.add_sensor_reading(sr_diameter)
    ps_2.add_sensor_reading(sr_acc_nozzle)
    ps_2.add_sensor_reading(sr_acc_bed)
    ps_2.add_sensor_reading(sr_diameter)

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


    with open('./a.json', 'a') as f:
        json.dump(model.serialize(), f)


if __name__ == '__main__':
    main()