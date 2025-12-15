from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BlogSampleConversation
from .serializers import BlogSampleConversationSerializer
from django.core.management import call_command


def sample_conversation_page(request):
    conversations = [
        {
            "topic": "Product launch prep",
            "user_message": "Draft a launch plan for our new analytics feature that highlights privacy first.",
            "assistant_message": "Here is a concise launch plan with messaging pillars that emphasize privacy by default and compliance readiness.",
            "tone": "Confident",
        },
        {
            "topic": "Website copy refresh",
            "user_message": "Rewrite the hero copy to be bolder but keep the core promise intact.",
            "assistant_message": "I tightened the hero line to focus on the promise while keeping the supportive subhead short and crisp.",
            "tone": "Crisp",
        },
        {
            "topic": "Customer support reply",
            "user_message": "Respond to a customer asking if we support SOC2. Keep it friendly.",
            "assistant_message": "I drafted a friendly response that confirms SOC2 readiness, links to our trust center, and offers a quick call.",
            "tone": "Friendly",
        },
    ]

    return render(
        request,
        "sampleconversations/demo.html",
        {"conversations": conversations},
    )


@method_decorator(csrf_exempt, name="dispatch")
class BlogSampleConversationAPIView(APIView):
    """
    CRUD for blog-specific sample conversations.
    GET: list or retrieve by id/blog
    POST: create
    PUT/PATCH: update
    """

    def get_object(self, request):
        convo_id = request.query_params.get("id")
        blog_id = request.query_params.get("blog")

        if convo_id:
            return BlogSampleConversation.objects.filter(pk=convo_id).first()
        if blog_id:
            return BlogSampleConversation.objects.filter(blog_id=blog_id).first()
        return None

    def get(self, request, *args, **kwargs):
        obj = self.get_object(request)
        if obj:
            serializer = BlogSampleConversationSerializer(obj)
            return Response(serializer.data)

        qs = BlogSampleConversation.objects.all()
        serializer = BlogSampleConversationSerializer(qs, many=True)
        return Response({"count": len(serializer.data), "items": serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = BlogSampleConversationSerializer(data=request.data)
        if serializer.is_valid():
            blog_id = serializer.validated_data.get("blog")
            if BlogSampleConversation.objects.filter(blog=blog_id).exists():
                return Response(
                    {"detail": "Sample conversation already exists for this blog."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            obj = serializer.save()
            translated = self._translate_sync(obj)
            return Response(
                {
                    "success": True,
                    "translation_success": translated,
                    "item": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        obj = self.get_object(request)
        if not obj:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSampleConversationSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            obj = serializer.save()
            translated = self._translate_sync(obj)
            return Response(
                {
                    "success": True,
                    "translation_success": translated,
                    "item": serializer.data,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    patch = put

    def _translate_sync(self, obj):
        try:
            call_command(
                "auto_translate_models",
                model="sampleconversations.blogsampleconversation",
                pks=[str(obj.pk)],
                force=True,
                verbosity=0,
            )
            return True
        except Exception:
            return False
