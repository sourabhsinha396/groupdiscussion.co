from django.contrib import admin
from .models import PaymentAttempt, CouponCode, Payment, Referral, Credit


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payee', 'group_discussion', 'status', 'created_at')
    search_fields = ('payee__email', 'group_discussion__title', 'status')
    list_filter = ('status', 'created_at', 'updated_at')


class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'group_discussion', 'message', 'updated_at')
    search_fields = ('user__email', 'group_discussion__title', 'message')
    list_filter = ('message', 'created_at', 'updated_at')


class CouponCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'expires', 'is_active', 'created_at', 'updated_at')
    search_fields = ('code', 'discount', 'expires')
    list_filter = ('is_active', 'created_at', 'updated_at')


class ReferralAdmin(admin.ModelAdmin):
    list_display = ('payment', 'referer', 'created_at', 'updated_at')
    search_fields = ('payment__payee__email', 'referer__email')
    list_filter = ('created_at', 'updated_at')


class CreditAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'amount', 'reason', 'created_at', 'updated_at')
    search_fields = ('user__email', 'payment__payee__email', 'reason')
    list_filter = ('created_at', 'updated_at')


admin.site.register(PaymentAttempt, PaymentAttemptAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(CouponCode, CouponCodeAdmin)
admin.site.register(Referral, ReferralAdmin)
admin.site.register(Credit, CreditAdmin)