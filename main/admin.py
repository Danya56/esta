from django.contrib import admin
from .models import Slide, Sertificate, CallbackRequest, Company

admin.site.site_header = 'Панель управления сайтом ЭСТА'
admin.site.index_title = 'Добро пожаловать в админ-панель'
admin.site.site_title = 'Эста'

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
    list_editable = ("is_active",)

@admin.register(Sertificate)
class SertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
    list_editable = ("is_active",)

@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "is_processed", "email", "comment", "created_at")
    list_filter = ("is_processed", "name",)
    list_editable = ("is_processed",)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name",);

