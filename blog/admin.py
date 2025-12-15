from django.contrib import admin

from blog.models import Blogs, blogCategory, blogPageSEO
from sampleconversations.models import BlogSampleConversation


class BlogSampleConversationInline(admin.StackedInline):
    model = BlogSampleConversation
    extra = 0
    max_num = 1
    can_delete = True
    fieldsets = (
        (None, {"fields": ("title", "subtitle", "conversations")}),
    )


@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "created_at")
    search_fields = ("title", "author", "description")
    list_filter = ("category",)
    inlines = [BlogSampleConversationInline]


admin.site.register(blogCategory)
admin.site.register(blogPageSEO)
