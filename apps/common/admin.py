from django.contrib import admin
from .models import ContactUs


admin.site.site_header = 'Swabhyaas Admin'
admin.site.site_title = 'Swabhyaas Admin Portal'
admin.site.index_title = 'Welcome to Swabhyaas Admin Portal'

class ContactUsModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'message', 'high_priority', 'resolved', 'created_at']
    list_filter = ['high_priority', 'resolved', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    list_editable = ['high_priority', 'resolved']

admin.site.register(ContactUs, ContactUsModelAdmin)
