from tokenize import TokenError
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    gender = serializers.CharField(required=True)
    affiliation = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Parollar mos emas"})

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email allaqachon ro'yxatdan o'tgan"})
        if User.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError({"phone": "Telefon raqam allaqachon ro'yxatdan o'tgan"})

        return attrs

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            gender=validated_data['gender'],
            affiliation=validated_data['affiliation']
        )
        user.set_password(validated_data['password'])
        user.save()

        refresh = RefreshToken.for_user(user)
        return {
            'id': user.id,
            'guid': user.guid,
            'phone': user.phone,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    guid = serializers.CharField(read_only=True)
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        # user = User.objects.filter(username=username).first()
        user = authenticate(phone=phone, password=password)
        if not user:
            raise serializers.ValidationError("User not found")
        refresh = RefreshToken.for_user(user)
        return {
            'id': user.id,
            'guid': user.guid,
            'phone': user.phone,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        print(self.token)
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad token')


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    conf_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('conf_password'):
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect password")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class AdminChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    conf_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('conf_password'):
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
