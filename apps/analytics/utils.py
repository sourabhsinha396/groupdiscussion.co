from .models import Hit

def track_hit(request):
    """Track hits on the website"""
    utm_source = request.GET.get('utm_source', None)
    utm_medium = request.GET.get('utm_medium', None)
    referer_site = request.META.get('HTTP_REFERER', None)
    client_ip = get_client_ip(request)
    referer = request.GET.get('referer', None)
    if not request.session.get('referer',None):
        request.session['referer'] = referer

    hits = Hit.objects.filter(
        utm_source=utm_source,
        utm_medium=utm_medium,
        referer_site=referer_site,
        ip_address=client_ip,
    )
    if hits.exists():
        return hits.first()
    
    new_hit = Hit.objects.create(
        utm_source=utm_source,
        utm_medium=utm_medium,
        referer_site=referer_site,
        ip_address=client_ip,
    )
    return new_hit


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip