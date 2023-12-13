from django.contrib import admin
from .models import Hit, Searches


class HitAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address', 'utm_source', 'utm_medium', 'referer_site', 'created_at', 'updated_at')
    list_filter = ('utm_source', 'utm_medium', 'created_at', 'updated_at')
    search_fields = ('utm_source', 'utm_medium', 'referer_site')


class SearchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'query', 'length_results', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('query',)
    raw_id_fields = ('user',)

admin.site.register(Hit, HitAdmin)
admin.site.register(Searches, SearchesAdmin)