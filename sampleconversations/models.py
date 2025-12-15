from django.db import models


class BlogSampleConversation(models.Model):
    blog = models.OneToOneField(
        "blog.Blogs",
        on_delete=models.CASCADE,
        related_name="sample_conversation",
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    conversations = models.JSONField(default=list, blank=True)
    conversations_en = models.JSONField(default=list, blank=True)
    conversations_tr = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f"Sample Conversation for {self.blog.title if self.blog else 'Blog'}"
