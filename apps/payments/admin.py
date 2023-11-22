from django.contrib import admin
from .models import PaymentAttempt, CouponCode, Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payee', 'group_discussion', 'status', 'created_at')
    search_fields = ('payee__email', 'group_discussion__title', 'status')
    list_filter = ('status', 'created_at', 'updated_at')


class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'group_discussion', 'message', 'updated_at')
    search_fields = ('user__email', 'group_discussion__title', 'message')
    list_filter = ('message', 'created_at', 'updated_at')


admin.site.register(PaymentAttempt, PaymentAttemptAdmin)
admin.site.register(CouponCode)
admin.site.register(Payment, PaymentAdmin)