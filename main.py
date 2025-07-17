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

def main():
    with open('./soil_dummy.json') as f:
        dummy_sr = f.read()

    p_1 = Product('P_1')
    p_2 = Product('P_2')

    batch = Batch('BATCH')
    batch.add_product(p_1)
    batch.add_product(p_2)

    psp = ProductSpecification('PSP')
    p_1.specification = psp
    p_2.specification = psp

    pp_1 = PreProduct('PP_1')
    pss_1 = ProcessStepSpecification('PSS_1')
    ps_1 = ProcessStep('PS_1')
    ps_1.specification = pss_1
    ps_1.pre_product = pp_1

    pp_2 = PreProduct('PP_2')
    pss_2 = ProcessStepSpecification('PSS_2')
    ps_2 = ProcessStep('PS_2')
    ps_2.specification = pss_2
    ps_2.pre_product = pp_2

    ps_1.next_step = ps_2

    operator = Operator('OPERATOR')
    ps_1.operator = operator
    ps_2.operator = operator

    tool_1 = Sensor('TOOL_1', SensorType.TOOL)
    tool_2 = Sensor('TOOL_2', SensorType.TOOL)
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

    printer_1 = Machine('PRINTER_1')
    printer_1.add_tool(tool_1)
    printer_1.add_tool(tool_2)
    printer_1.add_sensor(s_acc_nozzle)
    printer_1.add_sensor(s_diameter)
    ps_1.machine = printer_1
    ps_2.machine = printer_1

    shop_floor = ShopFloor('SHOP_FLOOR')
    shop_floor.add_machine(printer_1)

    p_1.add_reference('product', p_2)

    model = Model()
    model.add(p_1)
    model.add(p_2)
    ref = list(p_1.references['product'])[0]
    print(model.get_object(ref))

if __name__ == '__main__':
    main()