from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlogsSitemap,StaticViewSitemap,HighPrioritySitemaps


# handler404 = 'apps.common.views.custom_page_not_found'
# handler500 = 'apps.common.views.custom_500_error'

sitemaps = {'static': StaticViewSitemap, 'group-discussion-blogs': BlogsSitemap,'important':HighPrioritySitemaps}


urlpatterns = [
    path('adminra/', admin.site.urls),
    path("", include("apps.common.urls")),
    path("", include("apps.blogs.urls")),
    path("", include("apps.groupdiscussions.urls")),
    path("", include("apps.payments.urls")),
    path("", include("apps.authentication.urls")),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
