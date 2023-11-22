from django.contrib import admin
from .models import GroupDiscussion


class GroupDiscussionModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'mentor', 'start_datetime', 'is_active', 'is_free', 'is_private', 'created_at', 'updated_at')
    list_filter = ('mentor', 'is_active', 'is_free', 'is_private', 'created_at', 'updated_at')
    search_fields = ('title', 'mentor__username', 'mentor__email', 'mentor__first_name', 'mentor__last_name', 'start_datetime', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('mentor', 'title', 'slug', 'small_description', 'description', 'start_datetime', 'max_students', 'enrolled_students', 'price', 'is_active', 'is_free', 'is_private')
        }),
        ('System Info', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('start_datetime',)


admin.site.register(GroupDiscussion, GroupDiscussionModelAdmin)