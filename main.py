from mmpd.process.ProcessFlow import ProcessFlow
from mmpd.product.Product import Product
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

    print(batch.products)

if __name__ == '__main__':
    main()