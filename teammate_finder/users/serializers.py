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
    user = serializers.SerializerMethodField()

    class Meta:
        model = Subscribers
        fields = ('user',)

    def get_user(self, obj):
        request_user_id = self.context['request'].user.id
        if obj.user1_id.id == request_user_id:
            user_obj = obj.user2_id
        else:
            user_obj = obj.user1_id

        return {
            'username': user_obj.username,
            'user_id': user_obj.id,
            'first_name': user_obj.first_name,
            'last_name': user_obj.last_name,
            'city': user_obj.city,
            'gender': user_obj.gender,
            'about_me': user_obj.about_me,
            'age': get_age_global(user_obj.birthday)
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
