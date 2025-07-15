from mmpd.process.ProcessFlow import ProcessFlow
from mmpd.process.ProcessStepSpecification import ProcessStepSpecification
from mmpd.product.ProductSpecification import ProductSpecification
from mmpd.process.Operator import Operator
from mmpd.product.Product import Product
from mmpd.product.PreProduct import PreProduct
from mmpd.product.Batch import Batch
from soil.SensorReading import SensorReading
from soil.Sensor import Sensor
from soil.SensorType import SensorType
from mmpd.resource.Machine import Machine
from mmpd.resource.ShopFloor import ShopFloor

def main():
    with open('./soil_dummy.json') as f:
        dummy_sr = f.read()

    process = ProcessFlow('Test Process')

    p_1 = Product()
    p_2 = Product()

    batch = Batch()
    batch.add_product(p_1)
    batch.add_product(p_2)

    psp = ProductSpecification()
    p_1.specification = psp
    p_2.specification = psp

    pp_1 = PreProduct()
    pss_1 = ProcessStepSpecification()
    ps_1 = process.add_step()
    ps_1.specification = pss_1
    ps_1.pre_product = pp_1

    pp_2 = PreProduct()
    pss_2 = ProcessStepSpecification()
    ps_2 = process.add_step()
    ps_2.specification = pss_2
    ps_2.pre_product = pp_2

    operator = Operator()
    ps_1.operator = operator
    ps_2.operator = operator

    tool_1 = Sensor('', SensorType.TOOL)
    tool_2 = Sensor('', SensorType.TOOL)
    ps_1.tool = tool_2
    ps_2.tool = tool_1

    s_acc_nozzle = Sensor('', SensorType.REAL)
    s_acc_bed = Sensor('', SensorType.REAL)
    s_diameter = Sensor('', SensorType.REAL)

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

    printer_1 = Machine()
    printer_1.add_tool(tool_1)
    printer_1.add_tool(tool_2)
    printer_1.add_sensor(s_acc_nozzle)
    printer_1.add_sensor(s_diameter)
    ps_1.machine = printer_1
    ps_2.machine = printer_1

    shop_floor = ShopFloor()
    shop_floor.add_machine(printer_1)

    for reading in ps_1.all_readings:
        print(reading.raw_data)

if __name__ == '__main__':
    main()