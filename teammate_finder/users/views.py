from rest_framework import generics, status
from django.db.models import Q, Model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Users, Subscribers, Friends
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

    def get(self, request):
        user_id = request.user.id
        subscribers = Subscribers.objects.filter(
            Q(user1_id=user_id, is_subscribed2=True) | Q(user2_id=user_id, is_subscribed1=True)
        ).select_related('user1_id', 'user2_id')
        serialized_data = SubscribersSerializer(subscribers, many=True, context={"request": request})
        return Response(serialized_data.data)

    def post(self, request):
        """
        предполагаемый вид входных данных:
        {
            'user_id1': id, # id пользователя, отправившего запрос
            'user_id2': id, # id пользователя, на которого направлено действие
            'is_accept': True/False # True, если у пользователя есть подписчик и надо добавить в друзья
            'subscribe': True/False # True, если надо первым подписаться (создание новой записи в БД)
        }
        is_accept и subscribe всегда должны иметь противоположное значение
        """
        user1 = Users.objects.get(id=request.data['user_id1'])  # тот, кто послал запрос на взаимную подписку
        user2 = Users.objects.get(id=request.data['user_id2'])
        if request.data['is_accept']:
            try:
                subscriber = Subscribers.objects.get(user1_id=user1, user2_id=user2)
                subscriber.delete()
                friend = Friends(friend1_id=user1, friend2_id=user2)
                friend.save()

            except Subscribers.DoesNotExist:
                subscriber = Subscribers.objects.get(user1_id=user2, user2_id=user1)
                subscriber.delete()
                friend = Friends(friend1_id=user2, friend2_id=user1)
                friend.save()
            return Response({'answer': 'успешно добавлен в друзья'}, status=status.HTTP_200_OK)

        if request.data['subscribe']:
            subscriber = Subscribers(user1_id=user1, user2_id=user2, is_subscribed1=True)
            subscriber.save()
            return Response({'answer': 'успешно подписан'}, status=status.HTTP_200_OK)
