import sys
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image
from io import BytesIO

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.files.uploadedfile import InMemoryUploadedFile


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
    
    class MPTTMeta:
        order_insertion_by = ['name']


class Exam(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
    
    class MPTTMeta:
        order_insertion_by = ['name']


class Blog(MPTTModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ManyToManyField(Category, blank=True)
    exam = models.ManyToManyField(Exam, blank=True)
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content = RichTextUploadingField(blank=True, null=True, config_name='default')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:blog_detail', kwargs={'slug': self.slug})

    def get_active_previous_sibling(self):
        return self.get_previous_sibling(is_active=True)
    
    def get_active_next_sibling(self):
        return self.get_next_sibling(is_active=True)
    

def compress_image(uploaded_image):
    image_temporary = Image.open(uploaded_image)
    output_io_stream = BytesIO()
    image_temporary.save(output_io_stream, format='JPEG', quality=60)
    output_io_stream.seek(0)
    uploaded_image = InMemoryUploadedFile(output_io_stream, 'ImageField', "%s.jpg" % uploaded_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output_io_stream), None)
    return uploaded_image


@receiver(pre_save, sender=Blog)
def blog_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.image:
        instance.image = compress_image(instance.image)
    

@receiver(models.signals.post_delete, sender=Blog)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
