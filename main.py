from mmpd.process.ProcessFlow import ProcessFlow
from mmpd.process.ProcessStepSpecification import ProcessStepSpecification
from mmpd.product.ProductSpecification import ProductSpecification
from mmpd.process.Operator import Operator
from mmpd.product.Product import Product
from mmpd.product.PreProduct import PreProduct
from mmpd.product.Batch import Batch
from soil.SensorReading import SensorReading

def main():
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

    print(batch.products)

if __name__ == '__main__':
    with open('./soil_dummy.json') as f:
        d = f.read()

    reading = SensorReading(d)
    print(reading.id)
    #main()