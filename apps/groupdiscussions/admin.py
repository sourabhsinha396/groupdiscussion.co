from django.contrib import admin
from .models import GroupDiscussion
from mptt.admin import DraggableMPTTAdmin

class GroupDiscussionAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    )
    list_display_links = (
        'indented_title',
    )

admin.site.register(GroupDiscussion, GroupDiscussionAdmin)
