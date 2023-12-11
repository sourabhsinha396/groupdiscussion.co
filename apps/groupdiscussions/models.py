import requests
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.conf import settings


class GroupDiscussion(models.Model):
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_discussions')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    small_description = models.CharField(max_length=100, blank=True, null=True)
    description = RichTextUploadingField(config_name='default')
    start_datetime = models.DateTimeField()
    max_students = models.IntegerField(null=True, blank=True)
    enrolled_students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrolled_group_discussions', blank=True)
    price = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_free = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('start_datetime',)
        verbose_name = 'Interview'
        verbose_name_plural = 'Interviews'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('group_discussion_detail', args=[self.slug])
    
    def get_booking_url(self):
        return reverse('group_discussion_booking', args=[self.slug])
    

    def save(self, *args, **kwargs):
        if not self.is_free and not self.price:
            raise ValueError('Price is required for paid group discussions')
        
        if self.is_free and self.price:
            raise ValueError('Price is not required for free group discussions')
        
        if self.id and self.max_students:
            if self.enrolled_students.count() >= self.max_students - 2:
                requests.post("https://ntfy.sh/fastapi", data=f"Near Max Enrollment for Group Discussion {self.id}  {self.title}.".encode(encoding='utf-8'))
        super().save(*args, **kwargs)

