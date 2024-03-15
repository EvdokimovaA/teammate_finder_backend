from rest_framework import generics, status
from django.db.models import Q, Model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Users, Subscribers, Friends
from .serializers import UsersSerializer, RegistrationSerializer, SubscribersSerializer, FriendsSerializer


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
        """Выдаёт всех подписчиков конкретного пользователя"""
        user_id = request.user.id
        subscribers = Subscribers.objects.filter(
            Q(user1_id=user_id, is_subscribed2=True) | Q(user2_id=user_id, is_subscribed1=True)
        ).select_related('user1_id', 'user2_id')
        serialized_data = SubscribersSerializer(subscribers, many=True, context={"request": request})
        return Response(serialized_data.data)

    def post(self, request):
        """Осуществляет подписку в первый раз (создаёт новую запись в БД)"""
        user1 = Users.objects.get(id=request.data['user_id1'])  # тот, кто послал запрос на подписку
        user2 = Users.objects.get(id=request.data['user_id2'])
        subscriber = Subscribers(user1_id=user1, user2_id=user2, is_subscribed1=True)
        subscriber.save()
        return Response({'answer': 'успешно подписан'}, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Осуществляет взаимную подписку (удаление из Subscribers, добавление во Friends)
        Предполагаемый вид входных данных:
        {
            'user_id1': id, # id пользователя, отправившего запрос
            'user_id2': id, # id пользователя, которого надо добавить в друзья
        }
        """
        user1 = Users.objects.get(id=request.data['user_id1'])  # тот, кто послал запрос на взаимную подписку
        user2 = Users.objects.get(id=request.data['user_id2'])
        try:
            subscriber = Subscribers.objects.get(user1_id=user1, user2_id=user2)
            subscriber.delete()
            friend = Friends(user1_id=user1, user2_id=user2)
            friend.save()

        except Subscribers.DoesNotExist:
            subscriber = Subscribers.objects.get(user1_id=user2, user2_id=user1)
            subscriber.delete()
            friend = Friends(user1_id=user2, user2_id=user1)
            friend.save()
        return Response({'answer': 'успешно добавлен в друзья'}, status=status.HTTP_200_OK)

    def delete(self, request):
        """Удаляет подписку (запись из БД)"""
        user1 = Users.objects.get(id=request.data['user_id1'])  # тот, кто послал запрос на подписку
        user2 = Users.objects.get(id=request.data['user_id2'])
        subscriber = Subscribers.objects.get(user1_id=user1, user2_id=user2)
        subscriber.delete()
        return Response({'answer': 'подписка успешно отменена'}, status=status.HTTP_200_OK)


class FriendsAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = FriendsSerializer

    def get(self, request):
        """Выдаёт всех друзей конкретного пользователя"""
        user_id = request.user.id
        friends = Friends.objects.filter(user1_id=user_id) | Friends.objects.filter(user2_id=user_id)
        serialized_data = FriendsSerializer(friends, many=True, context={"request": request})
        return Response(serialized_data.data)

    def delete(self, request):
        """
        Осуществляет удаление из друзей (удаление из Friends, добавление в Subscribers)
        Предполагаемый вид входных данных:
        {
            'user_id1': id, # id пользователя, отправившего запрос
            'user_id2': id, # id пользователя, которого надо удалить из друзей
        }
        """
        user1 = Users.objects.get(id=request.data['user_id1'])  # тот, кто послал запрос на удаление
        user2 = Users.objects.get(id=request.data['user_id2'])
        try:
            friend = Friends.objects.get(user1_id=user1, user2_id=user2)
            friend.delete()
            subscriber = Subscribers(user1_id=user1, is_subscribed1=False, user2_id=user2, is_subscribed2=True)
            subscriber.save()

        except Subscribers.DoesNotExist:
            friend = Friends.objects.get(user1_id=user2, user2_id=user1)
            friend.delete()
            subscriber = Subscribers(user1_id=user2, is_subscribed1=True, user2_id=user1, is_subscribed2=False)
            subscriber.save()
        return Response({'answer': 'успешно удалён из друзей'}, status=status.HTTP_200_OK)
