from django.contrib import admin
from .models import Post, Category, Location
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
# Register your models here.

admin.site.unregister(Group)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author', 'location', 'category',
                    'is_published')
    list_editable = ('is_published',)
    search_fields = ('title', 'text')
    list_filter = ('category', 'location', 'is_published', 'pub_date')
    date_hierarchy = 'pub_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'text')
        }),
        (_('Дополнительные параметры'), {
            'fields': ('pub_date', 'author', 'location', 'category',
                       'is_published'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title', 'description')
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)
