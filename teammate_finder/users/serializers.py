import datetime
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Users


class UsersSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    def get_age(self, instance):
        today = datetime.date.today()
        age = today.year - instance.birthday.year - (
                (today.month, today.day) < (instance.birthday.month, instance.birthday.day))
        return age

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'city', 'age', 'gender', 'birthday')


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'gender', 'birthday', 'email', 'password')

    def create(self, validated_data):
        new_user = Users.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            gender=validated_data['gender'],
            birthday=validated_data['birthday'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        new_user.save()
        return new_user


# class LoginSerializer(serializers.Serializer):
#     email = serializers.CharField(max_length=255)
#     username = serializers.CharField(max_length=255, read_only=True)
#     password = serializers.CharField(max_length=128, write_only=True)
#     token = serializers.CharField(max_length=255, read_only=True)
#
#     def validate(self, data):
#         email = data.get('email', None)
#         username = data.get('username', None)
#         password = data.get('password', None)
#
#         if email is None:
#             raise serializers.ValidationError(
#                 'Не указан email'
#             )
#
#         if password is None:
#             raise serializers.ValidationError(
#                 'Не указан пароль'
#             )
#
#         # user = authenticate(email=data['email'], password=data['password'])
#         user = authenticate(username=username, password=password)
#         if not user:
#             raise ValidationError('Неверный email или пароль')


# class LoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length=255)
#
#     class Meta:
#         model = Users
#         fields = ['email', 'password']
