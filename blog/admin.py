from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Tag, Article


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")

@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ("title", "is_active")

    readonly_fields = ("slug", )
    


    summernote_fields = "text"
