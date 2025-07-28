from django.contrib import admin
from .models import Page
# Register your models here.


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
