from django.conf import settings


def common_context(request):
    return {
        "base_domain_url": settings.BASE_DOMAIN_URL,
    }