from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from api.users.serializers import UsersSerializers, UsersCreateSerializers, UserDetailSerializers, UsersShortSerializers

User = get_user_model()


class UsersCreateAPIView(CreateAPIView):
    serializer_class = UsersCreateSerializers


class UsersAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializers
    #permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializers
    lookup_field = 'guid'


class UsersUpdateAPIView(UsersAPIView):
    queryset = User.objects.all()
    serializer_class = UsersCreateSerializers
    lookup_field = 'guid'
    #permission_classes = (IsAuthenticated,)


class UsersDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsersCreateSerializers
    lookup_field = 'guid'
    #permission_classes = (IsAuthenticated,)


class UsersAPIViewSwt(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return UsersSerializers
        if hasattr(self, 'action') and self.action == 'retrieve':
            return UserDetailSerializers
        return UsersCreateSerializers
