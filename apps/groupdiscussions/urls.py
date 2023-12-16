from django.urls import path

from . import views

app_name = 'groupdiscussions'

urlpatterns = [
    path('schedule-group-discussion/', views.list_group_discussions, name='list_group_discussions'),
    path('interview/search/', views.search_interviews, name='search_interviews'),
    path('online-group-discussion/<slug:slug>/', views.group_discussion_detail, name='group_discussion_detail'),
]