import requests
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey

from django.db import models
from django.urls import reverse
from django.conf import settings

from apps.third_party_services.zoom_meetings import create_zoom_meeting


class GroupDiscussion(MPTTModel):
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
    meeting_id = models.CharField(max_length=100, blank=True, null=True)
    meeting_url = models.CharField(max_length=100, blank=True, null=True)
    meeting_password = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        ordering = ('start_datetime',)
        verbose_name = 'Group Discussion'
        verbose_name_plural = 'Group Discussions'

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
            if self.enrolled_students.count() >= self.max_students - 1:
                requests.post("https://ntfy.sh/fastapi", data=f"Near Max Enrollment for Group Discussion {self.id}  {self.title}.".encode(encoding='utf-8'))

        if not self.meeting_id:
            meeting = create_zoom_meeting(self.title, self.start_datetime, 60, self.slug)
            self.meeting_id = meeting['meeting_id']
            self.meeting_url = meeting['meeting_url']
            self.meeting_password = meeting['meeting_password']
        super().save(*args, **kwargs)

