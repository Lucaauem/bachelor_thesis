from mmpd.process.ProcessFlow import ProcessFlow
from mmpd.product.ProductSpecification import ProductSpecification
from mmpd.product.Product import Product
from mmpd.product.PreProduct import PreProduct
from mmpd.product.Batch import Batch

def main():
    process = ProcessFlow('Test Process')
    step_0 = process.add_step()
    step_1 = process.add_step()
    next = process.step_next_step()

    p_1 = Product()
    p_2 = Product()

    batch = Batch()
    batch.add_product(p_1)
    batch.add_product(p_2)

    pss_1 = PreProduct()
    pp_1 = PreProduct()

    ps_1 = ProductSpecification()
    pss_1.add_specification(ps_1)
    pp_1.add_specification(ps_1)
    p_1.add_specification(ps_1)

    print(batch.products)

if __name__ == '__main__':
    main()