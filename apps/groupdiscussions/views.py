from django.shortcuts import render
from django.db.models import Q
from django.db.models import F
from django.db.models import Count
from datetime import datetime

from .models import GroupDiscussion
from apps.analytics.utils import track_hit


def list_group_discussions(request):
    """List the active or private group discussions also remove the group discussions with number of enrolled students greater than or equal to max students or start_datetime_date greater than today."""
    track_hit(request)
    print("referer is ",request.session.get('referer', None))
    group_discussions = (
    GroupDiscussion.objects
    .filter(Q(is_active=True) | Q(is_private=True))
    .annotate(enrolled_students_count=Count('enrolled_students'))
    .exclude(enrolled_students_count__gte=F('max_students'))
    .exclude(start_datetime__date__lt=datetime.now().date())
    )
    return render(request, 'groupdiscussions/gd_list.html', {'group_discussions': group_discussions})


def group_discussion_detail(request, slug):
    track_hit(request)
    group_discussion = GroupDiscussion.objects.get(slug=slug)
    return render(request, 'groupdiscussions/gd_detail.html', {'group_discussion': group_discussion})


def search_interviews(request):
    track_hit(request)
    query = request.POST.get('interview_search', None)
    group_discussions = []
    if query:
        group_discussions = GroupDiscussion.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'groupdiscussions/gd_list.html', {'group_discussions': group_discussions})