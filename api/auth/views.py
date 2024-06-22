from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.auth.serializers import LoginSerializer, LogoutSerializer, ChangePasswordSerializer, \
    AdminChangePasswordSerializer, SignupSerializer

User = get_user_model()


class SignupAPIView(CreateAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = self.create(request, *args, **kwargs)
        return Response(user_data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User(
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            email=serializer.validated_data['email'],
            phone=serializer.validated_data['phone'],
            gender=serializer.validated_data['gender'],
            affiliation=serializer.validated_data['affiliation']
        )
        user.set_password(serializer.validated_data['password'])
        user.save()

        refresh = RefreshToken.for_user(user)

        return {
            'id': user.id,
            'guid': user.guid,
            'phone': user.phone,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(username=serializer.data.get('username')).first()
        if user:
            refresh = RefreshToken.for_user(user)

            return Response({
                'id': user.id,
                'guid': user.guid,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"})
        return super().create(request, *args, **kwargs)


class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh = request.data['refresh']
            print(refresh)
            refresh_token = RefreshToken(refresh)
            refresh_token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'guid'

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return AdminChangePasswordSerializer
        return ChangePasswordSerializer
