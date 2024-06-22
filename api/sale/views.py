from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Prefetch, Count, Sum

from common.product.model import Product
from common.sale.model import Sale, SaleProduct
from api.sale.serializers import SaleSerializers, SaleListaSerializers, SaleDetailSerializers, SaleProductSerializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SaleAPIView(viewsets.ModelViewSet):
    queryset = Sale.objects.all().prefetch_related(
        Prefetch(
            'saleSaleProduct', queryset=SaleProduct.objects.select_related('product'),
            to_attr='sale_products',
        )
    )
    serializer_class = SaleSerializers
    lookup_field = 'guid'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.query_params.get('user', None)
        if user:
            queryset = queryset.filter(user_id=user)
        queryset = queryset.annotate(quantity=Count('saleSaleProduct'),
                                     saleProductQuantity=Sum('saleSaleProduct__quantity'))
        return queryset

    def list(self, request, *args, **kwargs):
        self.serializer_class = SaleListaSerializers
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = self.queryset.annotate(product_count=Count('saleSaleProduct'))
        self.serializer_class = SaleDetailSerializers
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        saleProducts = request.data.get('saleProducts')
        validation_messages, createSaleProduct = [], []

        if saleProducts is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        sale = serializer.save()

        for saleProduct in saleProducts:
            product = Product.objects.filter(id=saleProduct.get('product')).first()
            if product is None:
                validation_messages.append(f"Product {saleProduct.get('product')} not found")
                continue

            quantity = saleProduct.get('quantity')
            if quantity is None:
                validation_messages.append(f"Quantity not found for product {saleProduct.get('product')}")
                continue

            saleProduct['sale'] = sale.id
            saleProductSerializer = SaleProductSerializers(data=saleProduct)
            if not saleProductSerializer.is_valid():
                validation_messages.append(saleProductSerializer.errors)
                continue

            saleProductInstance = SaleProduct(**saleProductSerializer.validated_data)
            createSaleProduct.append(saleProductInstance)

        if validation_messages:
            sale.delete()
            return Response(validation_messages, status=status.HTTP_400_BAD_REQUEST)

        if createSaleProduct:
            SaleProduct.objects.bulk_create(createSaleProduct)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        saleProducts = request.data.get('saleProducts')
        validation_messages, createSaleProduct, updateSaleProduct = [], [], []

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if saleProducts is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for saleProduct in saleProducts:
            product = Product.objects.filter(id=saleProduct.get('product')).first()
            if product is None:
                validation_messages.append(f"Product {saleProduct.get('product')} not found")
                continue

            quantity = saleProduct.get('quantity')
            if quantity is None:
                validation_messages.append(f"Quantity not found for product {saleProduct.get('product')}")
                continue

            saleProduct['sale'] = instance.id
            obj = SaleProduct.objects.filter(id=saleProduct.get('id'), guid=saleProduct.get('guid')).first()
            if obj is None:
                sale_product_serializer = SaleProductSerializers(data=saleProduct)
            if not sale_product_serializer.is_valid():
                validation_messages.append(sale_product_serializer.errors)
                continue

            saleProduct = SaleProduct(**sale_product_serializer.validated_data)
            createSaleProduct.append(saleProduct)
            # continue
        else:
            sale_product_serializer = SaleProductSerializers(instance=obj, data=saleProduct, partial=True)
            if not sale_product_serializer.is_valid():
                validation_messages.append(sale_product_serializer.errors)

            saleProduct = sale_product_serializer.save()
            updateSaleProduct.append(saleProduct)


def update(self, request, *args, **kwargs):
    instance = self.get_object()
    saleProducts = request.data.get('saleProducts', [])
    createSaleProducts = []
    updateSaleProducts = []
    validation_messages = []

    for saleProduct in saleProducts:
        quantity = saleProduct.get('quantity')
        if quantity is None:
            validation_messages.append(f'Quantity {saleProduct.get("product")} not found')
            continue

        saleProduct['order'] = instance.id

        obj = SaleProduct.objects.filter(id=saleProduct.get('id'), guid=saleProduct.get('guid')).first()
        if obj is None:
            sale_product_serializer = SaleProductSerializers(data=saleProduct)
            if not sale_product_serializer.is_valid():
                validation_messages.append(sale_product_serializer.errors)
                continue

            saleProduct = SaleProduct(**sale_product_serializer.validated_data)
            createSaleProducts.append(saleProduct)
        # continue
        else:
            sale_product_serializer = SaleProductSerializers(instance=obj, data=saleProduct, partial=True)
            if not sale_product_serializer.is_valid():
                validation_messages.append(sale_product_serializer.errors)
                continue

        saleProduct = sale_product_serializer.save()
        updateSaleProducts.append(saleProduct)

    if validation_messages:
        return Response(validation_messages, status=status.HTTP_400_BAD_REQUEST)

    serializer = self.get_serializer(instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    if updateSaleProducts:
        SaleProduct.objects.bulk_update(updateSaleProducts, ['quantity'])
    if createSaleProducts:
        SaleProduct.objects.bulk_create(createSaleProducts)

    return Response(serializer.data, status=status.HTTP_200_OK)
