from django.db.models.functions import ExtractYear
from rest_framework import generics, status
from django.db.models import Value, Q
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import authenticate

from .models import Users, Subscribers
from .serializers import UsersSerializer, RegistrationSerializer, SubscribersSerializer


# Create your views here.
class UsersViews(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Users.objects.annotate(age=ExtractYear(Value(timezone.now())) - ExtractYear('birthday'))
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'answer': 'успешно'
            },
            status=status.HTTP_201_CREATED)


class SubscribersAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SubscribersSerializer

    def get(self, request, user_id):
        subscribers = Subscribers.objects.filter(
            Q(user1_id=user_id, is_subscribed2=True) | Q(user2_id=user_id, is_subscribed1=True)
        ).select_related('user1_id', 'user2_id')
        serialized_data = SubscribersSerializer(subscribers, many=True)
        return Response(serialized_data.data)

# class LoginAPIView(APIView):
#     permission_classes = [AllowAny]
# serializer_class = LoginSerializer

# def post(self, request):
#     serializer = self.serializer_class(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     return Response(serializer.data, status=status.HTTP_200_OK)
# def post(self, request):
# serializer = LoginSerializer(data=request.data)
# serializer.is_valid(raise_exception=True)
# email = serializer.data.get('email')
# password = serializer.data.get('password')
# user = authenticate(email=email, password=password)
# if user is not None:
#     access_token = AccessToken.for_user(user)
#     refresh_token = RefreshToken.for_user(user)
#     return Response({
#         'access_token': str(access_token),
#         'refresh_token': str(refresh_token),
#         'msg': 'Login Success'
#     }, status=status.HTTP_200_OK)
# else:
#     return Response({'errors': 'Email or Password is not Valid'},
#                     status=status.HTTP_404_NOT_FOUND)
#
# email = request.data['email']
# password = request.data['password']
#
# user = Users.objects.filter(email=email).first()
#
# if user is None:
#     raise AuthenticationFailed('User not found!')
#
# if not user.check_password(password):
#     raise AuthenticationFailed('Incorrect password!')
#
# access_token = AccessToken.for_user(user)
# refresh_token = RefreshToken.for_user(user)
#
# return Response(
#     {
#         'access_token': access_token,
#         'refresh_token': refresh_token,
#     },
#     status=status.HTTP_200_OK)
