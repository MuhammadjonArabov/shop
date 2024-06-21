from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from decimal import Decimal
from common.product.model import Product, ProductPriceHistory, WarehouseProduct, BackupWarehouseProduct, Category
from config.settings.base import env


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'guid', 'title']


class ProductListSerializers(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        if obj.photo:
            return f"{env.str('BASE_URL')}{obj.photo.url}"
        return ""

    class Meta:
        model = Product
        fields = ['id', 'guid', 'title', 'photo', 'uom', 'category', 'recorder']


class ProductDetailSerializers(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'guid', 'title', 'photo', 'uom', 'category', 'recorder']


class ProductSerializers(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = Product
        fields = ['id', 'guid', 'title', 'photo', 'uom', 'category', 'recorder']


class ProductShortSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'guid', 'title', 'category', 'recorder']


class ProductPriceHistorySerializers(serializers.ModelSerializer):
    def to_internal_value(self, data):
        data = data.copy()
        decimal_fields = ['newPrice', 'oldPrice']
        for field in decimal_fields:
            if data.get(field) is not None and data.get(field) != 'null' and data.get(field) != "":
                data[field] = round(Decimal(data[field]), 6)
        return super().to_internal_value(data)

    class Meta:
        model = ProductPriceHistory
        fields = ['id', 'guid', 'product', 'recorder', 'newPrice', 'oldPrice']


class ProductPriceHistoryListSerializers(serializers.ModelSerializer):
    product = ProductShortSerializers()

    class Meta:
        model = ProductPriceHistory
        fields = ['id', 'guid', 'product', 'recorder', 'newPrice', 'oldPrice']


class ProductPriceHistoryDetailSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProductPriceHistory
        fields = ['id', 'guid', 'product', 'recorder', 'newPrice', 'oldPrice']


class WarehouseProductSerializers(serializers.ModelSerializer):
    def validated_quantity(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError('Quantity must by greater than 0')
        return value

    def to_internal_value(self, data):
        data = data.copy()
        decimal_fields = ['quantity', 'unitPrice']
        for field in decimal_fields:
            if data.get(field) is not None and data.get(field) != 'null' and data.get(field) != "":
                data[field] = round(Decimal(data[field]), 6)
        return super().to_internal_value(data)

    class Meta:
        model = WarehouseProduct
        fields = ['id', 'guid', 'product', 'recorder', 'quantity', 'unitPrice']


class WarehouseProductListSerializers(serializers.ModelSerializer):
    product = ProductShortSerializers()

    class Meta:
        model = WarehouseProduct
        fields = ['id', 'guid', 'product', 'recorder', 'quantity', 'unitPrice']


class BackupWarehouseProductSerializers(serializers.ModelSerializer):
    def validated_quantity(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError('Quantity must by greater than 0')
        return value

    def to_internal_value(self, data):
        data = data.copy()
        decimal_fields = ['quantity', 'unitPrice']
        for field in decimal_fields:
            if data.get(field) is not None and data.get(field) != 'null' and data.get(field) != "":
                data[field] = round(Decimal(data[field]), 6)
        return super().to_internal_value(data)

    class Meta:
        model = BackupWarehouseProduct
        fields = ['id', 'guid', 'product', 'quantity', 'unitPrice']


class BackupWarehouseProductListSerializers(serializers.ModelSerializer):
    product = ProductShortSerializers()

    class Meta:
        model = BackupWarehouseProduct
        fields = ['id', 'guid', 'product', 'quantity', 'unitPrice']


class ProductShortSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'photo', 'uom', 'category', 'recorder']
