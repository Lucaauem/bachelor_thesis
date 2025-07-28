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

def create_component(path: str, type: ComponentType, model: Model) -> Component:
    with open(path) as f:
        data = f.read()
    
    return Component(data, type, model=model)

def create_model() -> Model:
    model = Model()

    # Machines, Components, ...
    shopfloor_0 = ShopFloor('SHOP_FLOOR_1', model)
    shopfloor_1 = ShopFloor('SHOP_FLOOR_2', model)

    machine_0 = Machine('MACHINE_1', model)
    machine_0.set_attributes(age=15, usages=673)
    machine_1 = Machine('MACHINE_2', model)
    machine_1.set_attributes(age=5, usages=902)
    machine_2 = Machine('MACHINE_3', model)
    machine_2.set_attributes(age=2, usages=157)

    machine_0.add_sensor(create_component('./demo/components/sensors/sensor_0.json', ComponentType.REAL, model))
    machine_0.add_tool(create_component('./demo/components/tools/tool_0.json', ComponentType.TOOL, model))
    machine_1.add_sensor(create_component('./demo/components/sensors/sensor_1.json', ComponentType.REAL, model))
    machine_1.add_tool(create_component('./demo/components/tools/tool_1.json', ComponentType.TOOL, model))
    machine_2.add_sensor(create_component('./demo/components/sensors/sensor_2.json', ComponentType.REAL, model))
    machine_2.add_tool(create_component('./demo/components/tools/tool_2.json', ComponentType.TOOL, model))

    shopfloor_0.add_machine(machine_0)
    shopfloor_0.add_machine(machine_1)
    shopfloor_1.add_machine(machine_2)

    # Products, etc.
    pre_product_0 = PreProduct('PP_1', model)
    pre_product_0.set_attributes(name='Copper', cost=10, ammount=2)
    pre_product_specification_0 = ProductSpecification('PSP_P1', model)
    pre_product_specification_0.set_attributes(weight=0.01)
    pre_product_specification_0.add_to_pre_product(pre_product_0)

    product_0 = Product('P_1', model)
    product_0.set_attributes(name='Wire', quality=0.5)
    product_specification_0 = ProductSpecification('PSP_1', model)
    product_specification_0.set_attributes(weight=0.01)
    product_specification_0.add_to_product(product_0)


    pre_product_1 = PreProduct('PP_2', model)
    pre_product_1.set_attributes(name='Wire', cost=20, ammount=6)
    pre_product_specification_1 = ProductSpecification('PSP_P2', model)
    pre_product_specification_1.set_attributes(weight=0.015)
    pre_product_specification_1.add_to_pre_product(pre_product_1)
    
    product_1 = Product('P_2', model)
    product_1.set_attributes(name='Spoil', cost=40, quality=0.84)
    product_specification_1 = ProductSpecification('PSP_2', model)
    product_specification_1.set_attributes(weight=0.015)
    product_specification_1.add_to_product(product_1)


    pre_product_2 = PreProduct('PP_3', model)
    pre_product_2.set_attributes(name='Spoil', cost=20, ammount=6)
    pre_product_specification_2 = ProductSpecification('PSP_P3', model)
    pre_product_specification_2.set_attributes(weight=0.0175)
    pre_product_specification_2.add_to_pre_product(pre_product_2)

    product_2 = Product('P_3', model)
    product_2.set_attributes(name='Circuit', cost=75, quality=0.92)
    specification_2 = ProductSpecification('PSP_3', model)
    specification_2.set_attributes(weight=0.0175)
    specification_2.add_to_product(product_2)

    batch = Batch('B', model)
    batch.set_attributes(cost=150, max_weight=0.25)
    batch.add_product(product_0)
    batch.add_product(product_1)
    batch.add_product(product_2)


    # Production steps
    operator = Operator('O', model)

    process_step_0 = ProcessStep('PS_1', model)
    process_step_specification_0 = ProcessStepSpecification('PSP_1', model)
    process_step_specification_0.set_attributes(duration=60)
    process_step_specification_0.add_to_step(process_step_0)

    operator.add_to_step(process_step_0)
    pre_product_0.add_to_step(process_step_0)
    product_0.add_to_step(process_step_0)
    process_step_0.machine = machine_0


    process_step_1 = ProcessStep('PS_2', model)
    process_step_specification_1 = ProcessStepSpecification('PSP_2', model)
    process_step_specification_1.set_attributes(duration=30)
    process_step_specification_1.add_to_step(process_step_1)

    operator.add_to_step(process_step_1)
    pre_product_1.add_to_step(process_step_1)
    product_1.add_to_step(process_step_1)
    process_step_1.machine = machine_1

    process_step_2 = ProcessStep('PS_3', model)
    process_step_specification_2 = ProcessStepSpecification('PSP_3', model)
    process_step_specification_2.set_attributes(duration=360)
    process_step_specification_2.add_to_step(process_step_2)

    operator.add_to_step(process_step_2)
    pre_product_2.add_to_step(process_step_2)
    product_2.add_to_step(process_step_2)
    process_step_2.machine = machine_2

    process_step_0.next_step = process_step_1
    process_step_1.next_step = process_step_2

    return model
