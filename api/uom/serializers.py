from rest_framework import serializers
from decimal import Decimal
from common.uom.model import Uom, UomGroup


class UomGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = UomGroup
        fields = ['id', 'guid', 'title']


class UomSerializers(serializers.ModelSerializer):
    uomGrop = serializers.PrimaryKeyRelatedField(queryset=UomGroup.objects.all(), required=True)

    def validate_baseQuantity(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError('Quantity must be greater than 0')
        return round(Decimal(value), 6)

    def validate_quantity(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError('Quantity must be greater than 0')
        return round(Decimal(value), 6)

    class Meta:
        model = Uom
        fields = ['id', 'guid', 'title', 'uomGrop', 'baseQuantity', 'quantity']


class UomListSerializers(serializers.ModelSerializer):
    uomGrop = UomGroupSerializers()

    class Meta:
        model = Uom
        fields = ['id', 'guid', 'title', 'uomGrop', 'baseQuantity', 'quantity']


class UomShortSerializers(serializers.ModelSerializer):
    class Meta:
        model = Uom
        fields = ['id', 'guid', 'title', 'baseQuantity', 'quantity']
