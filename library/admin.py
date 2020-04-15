from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Image


def get_picture_preview(obj):
    if obj.pk:
        src = obj.image.url
        title = obj.title
        return mark_safe(
            f'<a href="{src}" target="_blank"><img src="{src}"\
            alt="{title}" style="max-width: 200px; max-height: 200px;"></a>'
        )
    return "(выберите картинку и сохраните для предпросмотра)"


get_picture_preview.short_description = "Предпросмотр"


def get_picture_thumb(obj):
    if obj.pk:
        src = obj.image.url
        title = obj.title
        return mark_safe(
            f'<a href="{src}" target="_blank"><img src="{src}"\
             alt="{title}" style="max-width: 60px; max-height: 60px;" /></a>'
        )

    return "(выберите картинку и сохраните для предпросмотра)"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = [
        "title",
        "description",
        "alt_text",
        "image",
        "created",
        get_picture_preview,
    ]
    readonly_fields = ["created", get_picture_preview]
    list_display = ["id", get_picture_thumb, "title", "created"]
    list_filter = ["created"]
