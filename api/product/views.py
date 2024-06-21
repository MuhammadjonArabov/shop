from rest_framework import viewsets
from api.product.serializers import (ProductSerializers, CategorySerializer, WarehouseProductSerializers,
                                     ProductPriceHistorySerializers, BackupWarehouseProductSerializers,
                                     ProductListSerializers, ProductPriceHistoryListSerializers,
                                     ProductDetailSerializers, WarehouseProductListSerializers,
                                     BackupWarehouseProductListSerializers, ProductPriceHistoryDetailSerializers)
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


class ProductPriceHistoryAPIView(viewsets.ModelViewSet):
    queryset = ProductPriceHistory.objects.select_related("product")
    serializer_class = ProductPriceHistorySerializers
    lookup_field = 'guid'

    def list(self, request, *args, **kwargs):
        self.serializer_class = ProductPriceHistoryListSerializers
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ProductPriceHistoryDetailSerializers
        return super().retrieve(request, *args, **kwargs)


class WarehouseProductAPIView(viewsets.ModelViewSet):
    queryset = WarehouseProduct.objects.select_related("product")
    serializer_class = WarehouseProductSerializers # ProductPriceHistoryAPIView
    lookup_field = 'guid'

    def list(self, request, *args, **kwargs):
        self.serializer_class = WarehouseProductListSerializers
        return super().list(request, *args, **kwargs)


# class BackupWarehouseProductAPIView(viewsets.ModelViewSet):
#     queryset = BackupWarehouseProduct.objects.select_related("product")
#     serializer_class = BackupWarehouseProductSerializers
#     lookup_field = 'guid'
#
#     def list(self, request, *args, **kwargs):
#         self.serializer_class = BackupWarehouseProductListSerializers
#         return super().list(request, *args, **kwargs)
