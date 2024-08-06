from rest_framework import serializers

from .models import Chats


class ChatsSerializer(serializers.ModelSerializer):
    chat_name = serializers.SerializerMethodField()

    def get_chat_name(self, obj):
        request = self.context.get('request')
        if request:
            request_user_id = request.user.id
            if obj.user1_id.id == request_user_id:
                chat_name = obj.user2_id.first_name + ' ' + obj.user2_id.last_name
            else:
                chat_name = obj.user1_id.first_name + ' ' + obj.user1_id.last_name
            return chat_name

    class Meta:
        model = Chats
        fields = ('chat_name',)
