import datetime
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Users, Subscribers


def get_age_global(birthday):
    today = datetime.date.today()
    age = today.year - birthday.year - (
            (today.month, today.day) < (birthday.month, birthday.day))
    return age

class UsersSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    def get_age(self, instance):
        return get_age_global(instance.birthday)

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'city', 'age', 'gender', 'birthday', 'about_me')



class SubscribersSerializer(serializers.ModelSerializer):
    user1 = serializers.SerializerMethodField()
    user2 = serializers.SerializerMethodField()

    class Meta:
        model = Subscribers
        fields = ('user1', 'user2')

    def get_user1(self, obj):
        return {
            'username': obj.user1_id.username,
            'user_id': obj.user1_id.id,
            'first_name': obj.user1_id.first_name,
            'last_name': obj.user1_id.last_name,
            'city': obj.user1_id.city,
            'gender': obj.user1_id.gender,
            'about_me': obj.user1_id.about_me,
            'age': get_age_global(obj.user1_id.birthday)

        }

    def get_user2(self, obj):
        return {
            'username': obj.user2_id.username,
            'user_id': obj.user2_id.id,
            'first_name': obj.user2_id.first_name,
            'last_name': obj.user2_id.last_name,
            'city': obj.user2_id.city,
            'gender': obj.user2_id.gender,
            'about_me': obj.user2_id.about_me,
            'age': get_age_global(obj.user2_id.birthday)
        }


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'gender', 'birthday', 'email', 'password', 'city')

    def create(self, validated_data):
        city = validated_data.get('city')
        new_user = Users.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            gender=validated_data['gender'],
            birthday=validated_data['birthday'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        if city is not None:
            new_user.city = city
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
