from rest_framework import serializers

from .models import BlogSampleConversation


class ConversationEntrySerializer(serializers.Serializer):
    topic = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    user_message = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    assistant_message = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tone = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class BlogSampleConversationSerializer(serializers.ModelSerializer):
    MAX_ITEMS = 30

    conversations = ConversationEntrySerializer(many=True, required=False)
    conversations_en = ConversationEntrySerializer(many=True, required=False)
    conversations_tr = ConversationEntrySerializer(many=True, required=False)

    class Meta:
        model = BlogSampleConversation
        fields = [
            "id",
            "blog",
            "title",
            "subtitle",
            "conversations",
            "conversations_en",
            "conversations_tr",
            "created_at",
            "updated_at",
        ]

    def validate_conversations(self, value):
        data = value or []
        if len(data) > self.MAX_ITEMS:
            raise serializers.ValidationError(f"conversations cannot exceed {self.MAX_ITEMS} items.")
        return data

    def validate_conversations_en(self, value):
        data = value or []
        if len(data) > self.MAX_ITEMS:
            raise serializers.ValidationError(f"conversations_en cannot exceed {self.MAX_ITEMS} items.")
        return data

    def validate_conversations_tr(self, value):
        data = value or []
        if len(data) > self.MAX_ITEMS:
            raise serializers.ValidationError(f"conversations_tr cannot exceed {self.MAX_ITEMS} items.")
        return data
