from jsonfield import JSONField
from django.db import models
from django.conf import settings


class Payment(models.Model):
    status_choice = (("paid","paid"),("failed","failed"),("pending","pending"),("refunded","refunded"))
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mentor_payments", help_text="Mentor or Moderator")
    payee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mentee_payments", help_text="User who paid")
    group_discussion = models.ForeignKey('groupdiscussions.GroupDiscussion',on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=status_choice)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    coupon = models.ForeignKey('payments.CouponCode',on_delete=models.SET_NULL, related_name="payments", null=True, blank=True)
    extra = JSONField(null=True, blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural="Payments"

    def __str__(self):
        return self.payee.email + " - " + self.group_discussion.title


class PaymentAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group_discussion = models.ForeignKey('groupdiscussions.GroupDiscussion',on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="Payment Attempts"
    
    def __str__(self):
        return self.user.email + " - " + self.group_discussion.title
    

class CouponCode(models.Model):
    code = models.CharField(max_length=50)
    discount = models.IntegerField()
    expires = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code + ' - ' + str(self.discount) + '%'
    

class Referral(models.Model):
    payment = models.OneToOneField('payments.Payment',on_delete=models.CASCADE, related_name="referral")
    referer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referrals")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="Referrals"
    
    def __str__(self):
        return self.referer.email + " - " + self.payment.payee.email + " - " + self.payment.group_discussion.title


class Credit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="credits")
    payment = models.OneToOneField('payments.Payment',on_delete=models.SET_NULL, related_name="credits", blank=True, null=True)
    amount = models.IntegerField()
    reason = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="Credits"
    
    def __str__(self):
        return self.user.email + " - " + self.reason
