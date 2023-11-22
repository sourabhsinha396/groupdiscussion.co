from mptt.admin import DraggableMPTTAdmin
from django.contrib import admin
from .models import Category, Exam, Blog


class CategoryAdmin(DraggableMPTTAdmin, admin.ModelAdmin):
    list_display = ["tree_actions", "indented_title", "slug"]
    list_display_links = ["indented_title"]
    prepopulated_fields = {'slug': ('name',)}


class ExamAdmin(DraggableMPTTAdmin, admin.ModelAdmin):
    list_display = ["tree_actions", "indented_title", "slug"]
    list_display_links = ["indented_title"]
    prepopulated_fields = {'slug': ('name',)}

    
class BlogAdmin(DraggableMPTTAdmin, admin.ModelAdmin):
    list_display = ["tree_actions", "indented_title", "is_active", "created", "updated"]
    list_display_links = ["indented_title"]
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['is_active', 'created', 'updated']
    search_fields = ['title', 'description', 'content']
    date_hierarchy = 'created'
    ordering = ['is_active', 'created', 'updated']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Blog, BlogAdmin)