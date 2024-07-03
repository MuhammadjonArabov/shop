from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from api.tasks import product_celery_task

from api.product.serializers import (ProductSerializers, CategorySerializer, WarehouseProductSerializers,
                                     ProductPriceHistorySerializers, ProductListSerializers,
                                     ProductDetailSerializers, WarehouseProductListSerializers,
                                     WarehouseProductDetailtSerializers)
from common.product.model import Product, ProductPriceHistory, WarehouseProduct, BackupWarehouseProduct, Category


class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'guid'


class ProductAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("uom")
    serializer_class = ProductSerializers

    def perform_create(self, serializer):
        product = serializer.save()
        new_price = product.price
        product_celery_task.apply_async([product.id, new_price])

    def list(self, request, *args, **kwargs):
        self.serializer_class = ProductListSerializers  # apply_async
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ProductDetailSerializers
        return super().retrieve(request, *args, **kwargs)


class WarehouseProductAPIView(viewsets.ModelViewSet):
    queryset = WarehouseProduct.objects.select_related("product")
    serializer_class = WarehouseProductSerializers  # ProductPriceHistoryAPIView
    lookup_field = 'guid'

    def list(self, request, *args, **kwargs):
        self.serializer_class = WarehouseProductListSerializers
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = WarehouseProductDetailtSerializers
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        priceProducts = request.data.get('priceProducts')
        createWarehouseProduct, validate_message = [], []

        if priceProducts is None:
            return Response({"detail": "priceProducts field is required."}, status=status.HTTP_400_BAD_REQUEST)

        warehouse_product_serializer = self.serializer_class(data=request.data)
        warehouse_product_serializer.is_valid(raise_exception=True)
        warehouse_product = warehouse_product_serializer.save()

        for priceProduct in priceProducts:
            product_price_history = priceProduct.get('productPrice')
            productPrice = ProductPriceHistory.objects.filter(id=product_price_history).first()
            if productPrice is None:
                validate_message.append(f"Product price {product_price_history} not found")
                continue

            priceHistory = priceProduct.get('priceHistory')
            if priceHistory is None:
                validate_message.append(f"Price history for product price {product_price_history} not found")
                continue

            priceHistory['product'] = warehouse_product.product.id
            priceHistory['recorder'] = request.user.id

            price_history_serializer = ProductPriceHistorySerializers(data=priceHistory)
            if not price_history_serializer.is_valid():
                validate_message.append(price_history_serializer.errors)
                continue
            createWarehouseProduct.append(price_history_serializer)

        if validate_message:
            warehouse_product.delete()
            return Response(validate_message, status=status.HTTP_400_BAD_REQUEST)

        if createWarehouseProduct:
            ProductPriceHistory.objects.bulk_create([serializer.save() for serializer in createWarehouseProduct])

        return Response(warehouse_product_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        priceProducts = request.data.get('priceProducts')
        instance = self.get_object()
        validate_messages = []

        if priceProducts is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        warehouse_product_serializer = self.serializer_class(instance, data=request.data, partial=True)
        warehouse_product_serializer.is_valid(raise_exception=True)
        warehouse_product = warehouse_product_serializer.save()

        createWarehouseProduct, updateWarehouseProduct = [], []

        for priceProduct in priceProducts:
            product_price_history = priceProduct.get('productPrice')
            productPrice = ProductPriceHistory.objects.filter(id=product_price_history).first()

            if productPrice is None:
                validate_messages.append(f"Product price {product_price_history} not found")
                continue

            priceHistory = priceProduct.get('priceHistory')
            if priceHistory is None:
                validate_messages.append(f'Price history for product price {product_price_history} not found')
                continue
            priceHistory['product'] = warehouse_product.product.id
            priceHistory['recorder'] = request.user.id

            if productPrice:
                price_history_serializer = ProductPriceHistorySerializers(productPrice, data=priceHistory, partial=True)
                if price_history_serializer.is_valid():
                    updateWarehouseProduct.append(price_history_serializer)
                else:
                    validate_messages.append(price_history_serializer.errors)
            else:
                price_history_serializer = ProductPriceHistorySerializers(data=priceHistory)
                if price_history_serializer.is_valid():
                    createWarehouseProduct.append(price_history_serializer)
                else:
                    validate_messages.append(price_history_serializer)
        if validate_messages:
            return Response(validate_messages, status=status.HTTP_400_BAD_REQUEST)
        if createWarehouseProduct:
            ProductPriceHistory.objects.bulk_create([serializer.save() for serializer in createWarehouseProduct])
        if updateWarehouseProduct:
            ProductPriceHistory.objects.bulk_update([serializer.save() for serializer in updateWarehouseProduct],
                                                    fields=['newPrice', 'oldPrice', 'product', 'recorder'])
        return Response(warehouse_product_serializer.data, status=status.HTTP_200_OK)
