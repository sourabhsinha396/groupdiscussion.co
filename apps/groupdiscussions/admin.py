from django.contrib import admin
from .models import GroupDiscussion
from mptt.admin import DraggableMPTTAdmin

class GroupDiscussionAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'is_active', 'is_private', 'max_students', 'start_datetime', 'created_at', 'updated_at')
    list_display_links = ('indented_title',)
    list_editable = ('is_active', 'max_students',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description', 'long_description')
    list_filter = ('is_active', 'is_private', 'start_datetime',)


admin.site.register(GroupDiscussion, GroupDiscussionAdmin)
