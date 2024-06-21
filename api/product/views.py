from rest_framework import viewsets, status
from rest_framework.response import Response

from api.product.serializers import (ProductSerializers, CategorySerializer, WarehouseProductSerializers,
                                     ProductPriceHistorySerializers, ProductListSerializers,
                                     ProductDetailSerializers, WarehouseProductListSerializers)
from common.product.model import Product, ProductPriceHistory, WarehouseProduct, BackupWarehouseProduct, Category


class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'guid'


class ProductAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("uom")
    serializer_class = ProductSerializers

    def list(self, request, *args, **kwargs):
        self.serializer_class = ProductListSerializers
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

    def create(self, request, *args, **kwargs):
        priceProducts = request.data.get('priceProducts')
        createWarehouseProduct, validate_message = [], []

        if priceProducts is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        price = serializer.save()

        for priceProduct in priceProducts:
            productPrice = ProductPriceHistory.objects.filter(id=priceProduct.get('productPrice')).first()
            if productPrice is None:
                validate_message.append(f"product price {priceProduct.get('productPrice')} not fount")
            continue
            priceHistory = priceProduct.get('priceHistory')
            if priceHistory is None:
                validate_message.append(f"Price history {priceProduct.get('priceHistory')} not fount")
            priceHistory['price'] = price.id
            priceHistory['newPrice'] = productPrice.newPrice
            priceHistory['oldPrice'] = productPrice.oldPrice

            serializer = ProductPriceHistorySerializers(data=priceProduct)
            if not serializer.is_valid():
                validate_message.append(serializer.errors)
                continue
            priceProduct = ProductPriceHistory(**serializer.validated_data)
            createWarehouseProduct.append(priceProduct)

        if validate_message:
            price.delete()
            return Response(validate_message, status=status.HTTP_400_BAD_REQUEST)

        if createWarehouseProduct:
            ProductPriceHistory.objects.bulk_create(createWarehouseProduct)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # class BackupWarehouseProductAPIView(viewsets.ModelViewSet):
#     queryset = BackupWarehouseProduct.objects.select_related("product")
#     serializer_class = BackupWarehouseProductSerializers
#     lookup_field = 'guid'
#
#     def list(self, request, *args, **kwargs):
#         self.serializer_class = BackupWarehouseProductListSerializers
#         return super().list(request, *args, **kwargs)
