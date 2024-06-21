from api.uom.serializers import UomGroupSerializers, UomSerializers, UomListSerializers
from common.uom.model import Uom, UomGroup
from rest_framework import viewsets


class UomGroupAPIView(viewsets.ModelViewSet):
    queryset = UomGroup.objects.all()
    serializer_class = UomGroupSerializers
    lookup_field = 'guid'


class UomAPIView(viewsets.ModelViewSet):
    queryset = Uom.objects.select_related('uomGrop')
    serializer_class = UomSerializers
    lookup_field = 'guid'

    def list(self, request, *args, **kwargs):
        self.serializer_class = UomListSerializers
        return super(UomAPIView, self).list(request, *args, **kwargs)
