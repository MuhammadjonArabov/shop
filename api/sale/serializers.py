from decimal import Decimal, InvalidOperation

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.product.serializers import ProductShortSerializers
from common.sale.model import Sale, SaleProduct, SalePayment


class SaleSerializers(serializers.ModelSerializer):
    from decimal import Decimal, InvalidOperation

    def to_internal_value(self, data):
        total_amount = data.get('totalAmount')
        try:
            if total_amount is None:
                raise ValueError("totalAmount is None")
            total_amount = Decimal(total_amount)
        except (ValueError, InvalidOperation) as e:
            raise ValidationError({'totalAmount': f"Invalid total amount: {total_amount}. Error: {str(e)}"})

        data['totalAmount'] = round(total_amount, 6)
        return data

    class Meta:
        model = Sale
        fields = ['id', 'guid', 'sale_id', 'code', 'totalAmount', 'status', 'recorder']


class SaleShortSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'guid', 'sale_id', 'code', 'recorder']


class SaleListaSerializers(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()

    def get_quantity(self, obj):
        if hasattr(obj, 'quantity'):
            return obj.quantity
        return 0

    class Meta:
        model = Sale
        fields = ['id', 'guid', 'sale_id', 'code', 'totalAmount', 'status', 'recorder', 'quantity']


class SaleProductSerializers(serializers.ModelSerializer):
    def validate_quantity(self, value):
        if value is None or value < 0:
            raise serializers.ValidationError("Quantitiy must be greater than 0")
        return value

    def to_internal_value(self, data):
        data = data.copy()
        decimal_fields = ['quantity', 'unitPrice']
        for field in decimal_fields:
            if data.get(field) is not None and data.get(field) != 'null' and data.get(field) != "":
                data[field] = round(Decimal(data[field]), 6)
        return super().to_internal_value(data)

    class Meta:
        model = SaleProduct
        fields = ['id', 'guid', 'sale', 'product', 'quantity', 'unitPrice', 'status']


class SaleProductListSerializers(serializers.ModelSerializer):
    class Meta:
        model = SaleProduct
        fields = ['id', 'guid', 'sale', 'product', 'quantity', 'unitPrice', 'status']


class SaleDetailSerializers(serializers.ModelSerializer):
    saleProduct = SaleProductListSerializers(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'guid', 'sale_id', 'code', 'totalAmount', 'status', 'recorder', 'saleProduct']


class SalePaymentSerializers(serializers.ModelSerializer):
    def to_internal_value(self, data):
        data = data.copy()
        total_amount = data.get('amount')

        if total_amount is not None and total_amount != 'null' and total_amount != "":
            data['amount'] = round(Decimal(total_amount), 6)

        return super().to_internal_value(data)

    class Meta:
        model = SalePayment
        fields = ['id', 'guid', 'sale', 'code', 'amount', 'paymentType']

