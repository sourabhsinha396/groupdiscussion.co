from django.shortcuts import render
from .models import GroupDiscussion
from django.db.models import Q
from django.db.models import F
from django.db.models import Count


def list_group_discussions(request):
    """List the active or private group discussions also remove the group discussions with number of enrolled students greater than or equal to max students."""
    group_discussions = (
    GroupDiscussion.objects
    .filter(Q(is_active=True) | Q(is_private=True))
    .annotate(enrolled_students_count=Count('enrolled_students'))
    .exclude(enrolled_students_count__gte=F('max_students'))
    )
    return render(request, 'groupdiscussions/gd_list.html', {'group_discussions': group_discussions})


def group_discussion_detail(request, slug):
    group_discussion = GroupDiscussion.objects.get(slug=slug)
    return render(request, 'groupdiscussions/gd_detail.html', {'group_discussion': group_discussion})
