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

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    ##
    def check_user(self, clean_data):
        user = authenticate(username=clean_data['email'], password=clean_data['password'])
        if not user:
            raise ValidationError('user not found')
        return user
