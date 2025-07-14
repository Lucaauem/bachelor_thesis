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

    psp = ProductSpecification()
    p_1.specification = psp
    p_2.specification = psp

    print(batch.products)

if __name__ == '__main__':
    main()