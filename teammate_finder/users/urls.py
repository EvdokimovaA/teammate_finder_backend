from django.urls import path
from . import views

urlpatterns = [
    path('', views.UsersViews.as_view()),
    path('subscribers/', views.SubscribersAPIView.as_view()),
    path('friends/', views.FriendsAPIView.as_view()),
    path('registration/', views.RegistrationAPIView.as_view(), name='registration'),
]
