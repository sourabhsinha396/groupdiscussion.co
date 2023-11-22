from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('adminra/', admin.site.urls),
    path("", include("apps.common.urls")),
    path("", include("apps.blogs.urls")),
    path("", include("apps.groupdiscussions.urls")),
    path("", include("apps.payments.urls")),
    path("", include("apps.authentication.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
