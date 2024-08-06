from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chats, Messages
from .serializers import ChatsSerializer


class ChatsViews(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatsSerializer

    def get(self, request):
        """Выдаёт все чаты конкретного пользователя"""
        user_id = request.user.id
        chats = Chats.objects.filter(Q(user1_id=user_id) | Q(user2_id=user_id))
        serialized_data = ChatsSerializer(chats, many=True, context={"request": request})
        return Response(serialized_data.data)

    def delete(self, request):
        """ Удаляет чат;
            Требуется id чата
        """
        chat = Chats.objects.get(id=request.data['id'])
        chat.delete()
        return Response({'answer': 'чат успешно удалён'}, status=status.HTTP_200_OK)
