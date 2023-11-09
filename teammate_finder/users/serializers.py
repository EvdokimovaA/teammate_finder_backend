from rest_framework import serializers

from .models import Users


class TeammatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'city', )
