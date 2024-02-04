from django.db.models.functions import ExtractYear
from rest_framework import generics, status
from django.db.models import Value
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import Users
from .serializers import UsersSerializer, RegistrationSerializer


# Create your views here.
class UsersViews(generics.ListAPIView):
    queryset = Users.objects.annotate(age=ExtractYear(Value(timezone.now())) - ExtractYear('birthday'))
    serializer_class = UsersSerializer


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        jwt_token = AccessToken.for_user(user)

        return Response(
            {
                'token': str(jwt_token)
            },
            status=status.HTTP_201_CREATED)