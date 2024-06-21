from django.contrib import admin

from common.sale.model import Sale, SalePayment, SaleProduct


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    pass


@admin.register(SalePayment)
class SalePaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    pass
