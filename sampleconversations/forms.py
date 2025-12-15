from django import forms

from .models import BlogSampleConversation


class BlogSampleConversationForm(forms.ModelForm):
    class Meta:
        model = BlogSampleConversation
        fields = ["title", "subtitle", "conversations"]
        widgets = {
            "conversations": forms.Textarea(attrs={"rows": 4, "placeholder": '[{"topic": "...", "user_message": "...", "assistant_message": "...", "tone": "..."}]'}),
        }
