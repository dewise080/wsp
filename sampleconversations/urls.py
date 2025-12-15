from django.urls import path

from . import views

urlpatterns = [
    path("sample-conversations/", views.sample_conversation_page, name="sample_conversation_page"),
    path(
        "api/blog-sample-conversations/",
        views.BlogSampleConversationAPIView.as_view(),
        name="blog_sample_conversation_api",
    ),
]
