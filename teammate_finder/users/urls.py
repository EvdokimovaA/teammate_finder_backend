from django.urls import path
from . import views

urlpatterns = [
    path('', views.UsersViews.as_view()),
    path('registration/', views.RegistrationAPIView.as_view(), name='registration'),
    # path('login/', views.LoginAPIView.as_view(), name='login')
]
