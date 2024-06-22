from django.contrib import admin

from common.product.model import Category, Product, BackupWarehouseProduct, ProductPriceHistory, WarehouseProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(WarehouseProduct)
class WarehouseProductAdmin(admin.ModelAdmin):
    pass
