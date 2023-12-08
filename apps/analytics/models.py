from django.db import models
from django.conf import settings


class Hit(models.Model):
    ip_address = models.GenericIPAddressField(help_text="IP Address", blank=True, null=True)
    utm_source = models.CharField(max_length=100, help_text="UTM Source", blank=True, null=True)
    utm_medium = models.CharField(max_length=100, help_text="UTM Medium", blank=True, null=True)
    referer_site = models.CharField(max_length=255, help_text="Referrer Website URL", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="Hits"

    def __str__(self):
        return str(self.id)