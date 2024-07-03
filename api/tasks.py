from celery import shared_task

from common.product.model import Product, ProductPriceHistory, BackupWarehouseProduct


@shared_task()
def product_celery_task(product_id, new_price):
    try:
        product = Product.objects.get(id=product_id)
        old_price = product.price

        if old_price != new_price:
            ProductPriceHistory.objects.create(
                product=product,
                recorder=product.recorder,
                newPrice=new_price,
                oldPrice=old_price
            )
        BackupWarehouseProduct.objects.create(
            product=product,
            quantity=0,
            unitPrice=new_price
        )
        return product.title
    except Product.DoesNotExist:
        return f"Product with id {product_id} does not exist."
