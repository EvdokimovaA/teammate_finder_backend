from django.urls import path
from . import views

urlpatterns = [
    path('', views.TeammatesViews.as_view()),
]
