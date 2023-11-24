from django.contrib.sitemaps import Sitemap
from django.contrib import sitemaps
from django.urls import reverse

from apps.blogs.models import Blog


class BlogsSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Blog.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'yearly'

    def items(self):
        return ['common:contact_us','common:privacy_policy','common:terms_and_conditions']

    def location(self, item):
        return reverse(item)


class HighPrioritySitemaps(sitemaps.Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return ['common:home','groupdiscussions:list_group_discussions']

    def location(self, item):
        return reverse(item)