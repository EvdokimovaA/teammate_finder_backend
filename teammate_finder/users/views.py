from django.db.models.functions import ExtractYear
from django.shortcuts import render
from rest_framework import generics
from django.db.models import Value
from django.utils import timezone
from .models import Users
from .serializers import TeammatesSerializer


# Create your views here.
class TeammatesViews(generics.ListAPIView):
    queryset = Users.objects.annotate(age=ExtractYear(Value(timezone.now())) - ExtractYear('birthday'))
    serializer_class = TeammatesSerializer

