from django.urls import path

from . import views
app_name = "blogs"

urlpatterns = [
    path("group-discussion-topics/", views.blog_list, name="blog_list"),
    path("blogs/submit-a-blog/", views.submit_a_blog, name="submit_a_blog"),
    path("group-discussion/<slug:slug>/", views.blog_detail, name="blog_detail"),
]