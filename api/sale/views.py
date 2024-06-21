from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Prefetch, Count, Sum
from common.sale.model import Sale, SaleProduct, SalePayment
from api.sale.serializers import SaleSerializers, SaleListaSerializers, SaleDetailSerializers, SaleProductSerializers


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
        self.serializer_class = SaleDetailSerializers
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        saleProducts = request.data.get('saleProducts', [])
        createSaleProducts = []
        validation_messages = []

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sale = serializer.save()

        if saleProducts:
            for saleProduct in saleProducts:
                quantity = saleProduct.get('quantity')
                if quantity is None:
                    validation_messages.append(f'Quantity {saleProduct.get("product")} not found')
                    continue

                saleProduct['order'] = sale.id
                saleProductSerializer = SaleProductSerializers(data=saleProduct)
                if not saleProductSerializer.is_valid():
                    validation_messages.append(saleProductSerializer.errors)
                    continue

                orderProduct = SaleProduct(**saleProductSerializer.validated_data)
                createSaleProducts.append(orderProduct)

        if validation_messages:
            sale.delete()
            return Response(validation_messages, status=status.HTTP_400_BAD_REQUEST)

        if createSaleProducts:
            SaleProduct.objects.bulk_create(createSaleProducts)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
                saleProductSerializer = SaleProductSerializers(data=saleProduct)
            else:
                saleProductSerializer = SaleProductSerializers(instance=obj, data=saleProduct, partial=True)

            if not saleProductSerializer.is_valid():
                validation_messages.append(saleProductSerializer.errors)
                continue

            if obj is None:
                saleProduct = SaleProduct(**saleProductSerializer.validated_data)
                createSaleProducts.append(saleProduct)
            else:
                saleProduct = SaleProduct(id=obj.id, **saleProductSerializer.validated_data)
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
