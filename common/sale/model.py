import uuid

from django.db import models

from common.base import BaseModel
from common.product.model import Product
from common.users.models import User


class SaleStatus(models.IntegerChoices):
    PENDING = 1, 'PENDING',
    COMPLETED = 2, 'COMPLETED',
    CANCELED = 3, 'CANCELED'


class SaleProductStatus(models.IntegerChoices):
    SOLD = 1, 'SOLD',
    RETURNED = 2, 'RETURNED'


class PaymentTypeStatus(models.IntegerChoices):
    CASH = 1, 'CASH',
    CARD = 2, 'CARD'


class Sale(BaseModel):
    sale_id = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    totalAmount = models.DecimalField(max_digits=50, decimal_places=6, default=0)
    status = models.IntegerField(choices=SaleStatus.choices, default=SaleStatus.PENDING)
    recorder = models.ForeignKey(User, related_name='staffSale', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:
            self.code = "S" + str(self.id)
            self.save()

    def __str__(self):
        return self.code


class SaleProduct(BaseModel):
    sale = models.ForeignKey(Sale, related_name='saleSaleProduct', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='productSaleProduct', on_delete=models.CASCADE, null=True,
                                blank=True)
    quantity = models.DecimalField(max_digits=50, decimal_places=6, default=0)
    unitPrice = models.DecimalField(max_digits=50, decimal_places=6, default=0)
    status = models.IntegerField(choices=SaleProductStatus.choices, default=SaleProductStatus.SOLD)


class SalePayment(BaseModel):
    sale = models.ForeignKey(Sale, related_name='saleSalePayment', on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True, blank=True)
    amount = models.DecimalField(max_digits=50, decimal_places=6, default=0)
    paymentType = models.IntegerField(choices=PaymentTypeStatus.choices, default=PaymentTypeStatus.CASH)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code
