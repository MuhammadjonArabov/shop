from django.db import models

from common.base import BaseModel
from common.users.models import User
from common.uom.model import Uom


class Category(BaseModel):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='productImage', null=True, blank=True)
    uom = models.ForeignKey(Uom, related_name='uomProduct', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='categoryProduct', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    recorder = models.ForeignKey(User, related_name='recorderProduct', on_delete=models.SET_NULL, null=True,
                                 blank=True)

    def __str__(self):
        return self.title


class WarehouseProduct(BaseModel):
    product = models.OneToOneField(Product, related_name='productWarehouseProduct', on_delete=models.CASCADE,
                                   null=True, blank=True)
    recorder = models.ForeignKey(User, related_name='recorderWarehouseProduct', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    quantity = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    unitPrice = models.DecimalField(max_digits=20, decimal_places=6, default=0)

    def __str__(self):
        return self.quantity


class ProductPriceHistory(BaseModel):
    product = models.ForeignKey(Product, related_name='productProductPriceHistory', on_delete=models.CASCADE,
                                null=True, blank=True)
    recorder = models.ForeignKey(User, related_name='recorderProductPriceHistory', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    newPrice = models.DecimalField(max_digits=50, decimal_places=6, default=0)
    oldPrice = models.DecimalField(max_digits=50, decimal_places=6, default=0)

    def __str__(self):
        return self.newPrice


class BackupWarehouseProduct(BaseModel):
    product = models.ForeignKey(Product, related_name='productBackupWarehouseProduct', on_delete=models.CASCADE,
                                null=True, blank=True)
    quantity = models.DecimalField(max_digits=50, decimal_places=6, default=0)
    unitPrice = models.DecimalField(max_digits=50, decimal_places=6, default=0)

    def __str__(self):
        return self.quantity
