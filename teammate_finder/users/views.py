from django.shortcuts import render
from rest_framework import generics
from django.core.paginator import Paginator
from .models import Users
from .serializers import TeammatesSerializer


# Create your views here.
class TeammatesViews(generics.ListAPIView):
    # queryset = Paginator(Users.objects.all(), 50)
    queryset = Users.objects.all()
    serializer_class = TeammatesSerializer
