from django.contrib import admin

from common.uom.model import Uom, UomGroup


@admin.register(Uom)
class UomAdmin(admin.ModelAdmin):
    pass


@admin.register(UomGroup)
class BaseUomAdmin(admin.ModelAdmin):
    pass
