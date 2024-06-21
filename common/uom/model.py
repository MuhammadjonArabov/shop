from django.db import models

from common.base import BaseModel


class UomGroup(BaseModel):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Uom(BaseModel):
    title = models.CharField(max_length=150)
    uomGrop = models.ForeignKey(UomGroup, related_name='uomGropUom', on_delete=models.CASCADE, null=True, blank=True)
    baseQuantity = models.DecimalField(max_digits=50, decimal_places=6)
    quantity = models.DecimalField(max_digits=50, decimal_places=6, default=0)

    def __str__(self):
        return self.title
