from django.contrib import admin
from .models import Hit


class HitAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address', 'utm_source', 'utm_medium', 'referer_site', 'created_at', 'updated_at')
    list_filter = ('utm_source', 'utm_medium', 'created_at', 'updated_at')
    search_fields = ('utm_source', 'utm_medium', 'referer_site')

admin.site.register(Hit, HitAdmin)