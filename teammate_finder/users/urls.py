from django.urls import path
from . import views

urlpatterns = [
    path('', views.UsersViews.as_view()),
    path('subscribers/<int:user_id>', views.SubscribersAPIView.as_view()),
    path('registration/', views.RegistrationAPIView.as_view(), name='registration'),
]
