from django.db import migrations, models


def copy_conversations_to_langs(apps, schema_editor):
    BlogSampleConversation = apps.get_model("sampleconversations", "BlogSampleConversation")
    for convo in BlogSampleConversation.objects.all():
        data = convo.conversations
        en_val = []
        tr_val = []

        if isinstance(data, dict):
            en_val = data.get("en") or data.get("en-us") or data.get("en-gb") or data.get("default") or []
            tr_val = data.get("tr") or []
            # If dict but missing any language, fall back to default list if present
            if not en_val and isinstance(data.get("items"), list):
                en_val = data.get("items")
            if not tr_val and en_val:
                tr_val = en_val
        elif isinstance(data, list):
            en_val = data
            tr_val = data

        convo.conversations_en = en_val or []
        convo.conversations_tr = tr_val or []
        convo.save(update_fields=["conversations_en", "conversations_tr"])


def noop_reverse(apps, schema_editor):
    pass


def add_missing_json_fields(apps, schema_editor):
    """
    Add conversations_en/conversations_tr if they are missing (handles pre-existing columns).
    """
    BlogSampleConversation = apps.get_model("sampleconversations", "BlogSampleConversation")
    table_name = BlogSampleConversation._meta.db_table
    existing = {col.name for col in schema_editor.connection.introspection.get_table_description(schema_editor.connection.cursor(), table_name)}

    for field_name in ("conversations_en", "conversations_tr"):
        if field_name in existing:
            continue
        field = BlogSampleConversation._meta.get_field(field_name)
        schema_editor.add_field(BlogSampleConversation, field)


class Migration(migrations.Migration):
    dependencies = [
        ("sampleconversations", "0002_blogsampleconversation_subtitle_en_and_more"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name="blogsampleconversation",
                    name="conversations_en",
                    field=models.JSONField(blank=True, default=list),
                ),
                migrations.AddField(
                    model_name="blogsampleconversation",
                    name="conversations_tr",
                    field=models.JSONField(blank=True, default=list),
                ),
            ],
            database_operations=[
                migrations.RunPython(add_missing_json_fields, noop_reverse),
            ],
        ),
        migrations.RunPython(copy_conversations_to_langs, noop_reverse),
    ]
