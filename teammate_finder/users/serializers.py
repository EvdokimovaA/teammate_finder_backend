import datetime

from rest_framework import serializers
from django.utils import timezone

from .models import Users


class TeammatesSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    def get_age(self, instance):
        today = datetime.date.today()
        age = today.year - instance.birthday.year - (
                    (today.month, today.day) < (instance.birthday.month, instance.birthday.day))
        return age

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'city', 'age')
